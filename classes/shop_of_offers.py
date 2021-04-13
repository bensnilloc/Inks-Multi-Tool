class shop_of_offers:
    def __init__(self, wrapper, functions, username):
        self.wrapper = wrapper
        self.functions = functions()
        self.username = username

    def visit_shop_of_offers(self):
        response = self.wrapper.get("shop_of_offers.phtml?slorg_payout=yes", referer="https://thedailyneopets.com/dailies")
        if self.functions.contains(response.text, "from what seems to be a very rich Slorg"):
            print(f"[{self.username}] Shop of Offers: Grabbed some free neopoints")
        if not self.functions.ensure_login(response.text):
            if self.wrapper.login():
                return self.visit_shop_of_offers()