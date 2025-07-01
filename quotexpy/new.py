class Quotex:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.connected = False
        self.last_amount = 0

    async def connect(self):
        self.connected = True
        return True, "Connected"

    async def change_account(self, account_type):
        pass

    async def trade(self, direction, amount, asset, expiry):
        self.last_amount = amount
        return True, {asset: {"id": "mock_trade_id"}}

    async def check_win(self, asset, trade_id):
        return True

    def get_profit(self):
        return 8.0
