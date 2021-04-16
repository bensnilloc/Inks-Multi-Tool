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
from classes.kacheek_seek import kacheekseek
from classes.potato_counter import potato_counter
from classes.obsidian_quarry import obsidian_quarry
from classes.lottery import lottery
from classes.stock_buyer import stock_buyer

class client:
    def __init__(self, username, password, proxy, pin):
        self.wrapper = wrapper(username, password, proxy)
        self.ghoul_catchers = GhoulCatchers(username, password, proxy, functions)
        self.shop_of_offers = shop_of_offers(self.wrapper, functions, username)
        self.trudys_surprise = trudys_surprise(self.wrapper, functions, username)
        self.giant_jelly = giant_jelly(self.wrapper, functions, username)
        self.kacheek_seek = kacheekseek(self.wrapper, functions, username)
        self.potato_counter = potato_counter(self.wrapper, functions, username)
        self.obsidian_quarry = obsidian_quarry(self.wrapper, functions, username)
        self.lottery = lottery(self.wrapper, functions, username)
        self.stock_buyer = stock_buyer(self.wrapper, functions, username)
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
            neopoints_before = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            self.shop_of_offers.visit_shop_of_offers()
            neopoints_after = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            neopoints_earned = neopoints_after - neopoints_before
            self.functions.update_neopoints_gained(self.username, "shop of offers", neopoints_earned)
            self.functions.update_last_run(self.username, "shop of offers")

    def play_trudys_surprise(self):
        if int(time.time()) - self.functions.get_last_run(self.username, "trudys surprise") >= 86400:
            neopoints_before = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            self.trudys_surprise.play_trudys_surprise()
            neopoints_after = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            neopoints_earned = neopoints_after - neopoints_before
            self.functions.update_neopoints_gained(self.username, "trudys surprise", neopoints_earned)
            self.functions.update_last_run(self.username, "trudys surprise")

    def visit_giant_jelly(self):
        if int(time.time()) - self.functions.get_last_run(self.username, "giant jelly") >= 86400:
            jelly = self.giant_jelly.grab_jelly()
            if jelly:
                self.functions.update_items_gained(self.username, "giant jelly", jelly)
                self.functions.update_last_run(self.username, "giant jelly")
            else:
                self.functions.update_last_run(self.username, "giant jelly")

    def play_kacheek_seek(self):
        if int(time.time()) - self.functions.get_last_run(self.username, "kacheek seek") >= 86400:
            neopoints_before = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            self.kacheek_seek.seek()
            neopoints_after = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            neopoints_earned = neopoints_after - neopoints_before
            self.functions.update_neopoints_gained(self.username, "kacheek seek", neopoints_earned)
            self.functions.update_last_run(self.username, "kacheek seek")

    def play_potato_counter(self):
        if int(time.time()) - self.functions.get_last_run(self.username, "potato counter") >= 86400:
            neopoints_before = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            self.potato_counter.play_potato_counter()
            neopoints_after = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            neopoints_earned = neopoints_after - neopoints_before
            self.functions.update_neopoints_gained(self.username, "potato counter", neopoints_earned)
            self.functions.update_last_run(self.username, "potato counter")

    def visit_obsidian_quarry(self):
        if int(time.time()) - self.functions.get_last_run(self.username, "obsidian quarry") >= 86400:
            obsidian_quarry = self.obsidian_quarry.visit_obsidian_quarry()
            if obsidian_quarry:
                self.functions.update_items_gained(self.username, "obsidian quarry", "Shiny Obsidian")
                self.functions.update_last_run(self.username, "obsidian quarry")
            else:
                self.functions.update_last_run(self.username, "obsidian quarry")

    def play_lottery(self):
        if int(time.time()) - self.functions.get_last_run(self.username, "lottery") >= 86400:
            tickets_bought, neopoints_spent = self.lottery.play_lottery()
            self.functions.update_tickets_bought(self.username, "lottery", tickets_bought)
            self.functions.update_neopoints_spent(self.username, "lottery", neopoints_spent)
            self.functions.update_last_run(self.username, "lottery")

    def buy_stocks(self):
        if int(time.time()) - self.functions.get_last_run(self.username, "stocks") >= 86400:
            neopoints_before = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            self.stock_buyer.buy_stocks()
            neopoints_after = self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text)
            neopoints_spent = neopoints_after - neopoints_before
            self.functions.update_stocks_bought(self.username, "stocks")
            self.functions.update_neopoints_spent(self.username, "stocks", neopoints_spent)
            self.functions.update_last_run(self.username, "stocks")

    def initiate_program(self):
        if self.wrapper.login():
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
        threads.append(thread)
    for i in range(len(account)):
        threads[i].start()
    for i in range(len(account)):
        threads[i].join()
