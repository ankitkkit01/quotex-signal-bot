from quotexpy.new import Quotex

class QuotexAPIHandler:
    def __init__(self):
        self.client = None
        self.connected = False

    async def connect(self, email: str, password: str) -> bool:
        self.client = Quotex(email=email, password=password)
        status, reason = await self.client.connect()
        self.connected = status
        return status

    async def change_account(self, account_type="PRACTICE"):
        if self.connected:
            await self.client.change_account(account_type)

    async def place_trade(self, asset: str, direction: str, amount: float, expiry: int):
        if not self.connected:
            raise Exception("❌ Not connected to Quotex.")
        success, trade_data = await self.client.trade(direction, amount, asset, expiry)
        if success:
            return trade_data[asset]["id"]
        return None

    async def check_result(self, asset: str, trade_id: str) -> tuple:
        if not self.connected:
            raise Exception("❌ Not connected to Quotex.")
        is_win = await self.client.check_win(asset, trade_id)
        profit = self.client.get_profit() if is_win else -self.client.last_amount
        return is_win, profit
