import json
import time
import random
import threading
from classes.wrapper import wrapper
from classes.functions import functions
from classes.ghoul_catchers import GhoulCatchers
from classes.shop_of_offers import shop_of_offers
from classes.trudys_surprise import trudys_surprise
from classes.giant_jelly import giant_jelly

class client:
    def __init__(self, username, password, proxy, pin):
        self.wrapper = wrapper(username, password, proxy)
        self.ghoul_catchers = GhoulCatchers(username, password, proxy)
        self.shop_of_offers = shop_of_offers(self.wrapper, username)
        self.trudys_surprise = trudys_surprise(self.wrapper)
        self.giant_jelly = giant_jelly(self.wrapper)
        self.functions = functions()
        self.username = username

    def play_ghoul_catchers(self):
        if int(time.time()) - self.functions.get_last_run(self.username, "ghoul catchers") >= 86400:
            neopoints_before = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            self.ghoul_catchers.login_parent()
            self.ghoul_catchers.login_child()
            self.ghoul_catchers.apply_payout()
            neopoints_after = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            neopoints_earned = neopoints_after - neopoints_before
            self.functions.update_neopoints_gained(self.username, "ghoul catchers", neopoints_earned)
            self.functions.update_last_run(self.username, "ghoul catchers")

    def visit_shop_of_offers(self):
        if int(time.time()) - self.functions.get_last_run(self.username, "shop of offers") >= 86400:
            self.ensure_login()
            neopoints_before = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            self.shop_of_offers.visit_shop_of_offers()
            neopoints_after = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            neopoints_earned = neopoints_after - neopoints_before
            self.functions.update_neopoints_gained(self.username, "shop of offers", neopoints_earned)
            self.functions.update_last_run(self.username, "shop of offers")

    def play_trudys_surprise(self):
        if int(time.time()) - self.functions.get_last_run(self.username, "trudys surprise") >= 86400:
            self.ensure_login()
            neopoints_before = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            self.trudys_surprise.play_trudys_surprise()
            neopoints_after = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            neopoints_earned = neopoints_after - neopoints_before
            self.functions.update_neopoints_gained(self.username, "trudys surprise", neopoints_earned)
            self.functions.update_last_run(self.username, "trudys surprise")

    def visit_giant_jelly(self):
        if int(time.time()) - self.functions.get_last_run(self.username, "giant jelly") >= 86400:
            self.ensure_login()
            jelly = self.giant_jelly.grab_jelly()
            if jelly:
                self.functions.update_items_gained(self.username, "giant jelly", jelly)
                self.functions.update_last_run(self.username, "giant jelly")
            else:
                self.functions.update_last_run(self.username, "giant jelly")

    def ensure_login(self):
        return self.wrapper.login()

    def initiate_program(self):
        self.wrapper.login()
        while True:
            with open("tasks/tasks.json", "r") as f:
                tasks = json.load(f)
            for task in tasks:
                if tasks[task]["status"] == "on":
                    exec(f"self.{tasks[task]['code']}()")
            time.sleep(random.uniform(60, 300))

if __name__ == "__main__":
    account = functions().get_account_total()
    threads = []
    for i in range(len(account)):
        username, password, proxy, pin = functions().pull_account(account[i])
        thread = threading.Thread(target=client(username, password, proxy, pin).initiate_program)
        thread.daemon = True
        threads.append(thread)
    for i in range(len(account)):
        threads[i].start()
    for i in range(len(account)):
        threads[i].join()
