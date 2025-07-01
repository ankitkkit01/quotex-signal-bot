class Quotex:
    def __init__(self):
        self.email = "arhimanshya@gmail.com"
        self.password = "12345678an"
        # Simulate login (or real API login code here)
        print(f"[Quotex] Logged in as {self.email}")

    def place_trade(self, pair, direction, amount, duration):
        print(f"[Quotex] Placing {direction.upper()} trade on {pair} for ${amount} / {duration}s")
        return "trade_id_12345"  # Simulated trade ID

    def check_result(self, pair, trade_id):
        print(f"[Quotex] Checking result for {pair} with trade ID: {trade_id}")
        # Simulated result: always win
        return True, 8.75
