import re
import random

class stock_buyer:
    def __init__(self, wrapper, functions, username):
        self.wrapper = wrapper
        self.functions = functions()
        self.username = username

    def buy_stocks(self):
        data, try_again = 15, 15
        response = self.wrapper.get("stockmarket.phtml?type=list&full=true", referer="http://www.neopets.com/stockmarket.phtml?type=buy")
        for _ in range(3):
            stocks = list(set(re.findall(rf"<b>(\w+?) {data} [-\+]\d+?<\/b>", response.text)))
            if not stocks:
                try_again += 1
                print(f"[{self.username}] Stock Buyer: No stocks found for {data}NP. checking for {try_again}NP..")
                data +=1
            if stocks:
                if len(stocks) > 1:
                    stocks = random.choice(stocks)
                else:
                    stocks = stocks[0]
                response = self.wrapper.get("stockmarket.phtml?type=buy", referer="http://www.neopets.com/stockmarket.phtml?type=list&full=true")
                stock_hash = self.functions.get_between(response.text, "&_ref_ck=", "';")
                response = self.wrapper.post("process_stockmarket.phtml", data={"_ref_ck": stock_hash, "type": "buy", "ticker_symbol": stocks, "amount_shares": "1000"}, referer="http://www.neopets.com/stockmarket.phtml?type=buy")
                if self.functions.contains(response.text, "purchase limit of 1000"):
                    print(f"[{self.username}] Stock Buyer: You can't buy more than 1,000 shares per day..")
                elif self.functions.contains(response.text, "You cannot afford"):
                    print(f"[{self.username}] Stock Buyer: You don't have enough neopoints..")
                else:
                    print(f"[{self.username}] Stock Buyer: Purchased 1,000 shares of {stocks} for {data}NP!")
            break