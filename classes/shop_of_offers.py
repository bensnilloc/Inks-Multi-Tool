class shop_of_offers:
    def __init__(self, wrapper, username):
        self.wrapper = wrapper
        self.username = username

    def visit_shop_of_offers(self):
        self.wrapper.get("shop_of_offers.phtml?slorg_payout=yes", referer="https://thedailyneopets.com/dailies")
