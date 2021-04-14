import time
import random
import json
import os
import re

class functions:
    def contains(self, data, string):
        return True if string in data else False

    def get_between(self, data, first, last):
        return data.split(first)[1].split(last)[0]

    def delay(self, minimum, maximum):
        return time.sleep(random.uniform(minimum, maximum))

    def parse_settings(self):
        with open("settings/settings.json", "r") as f:
            data = json.load(f)
        return data["delay"]["minimum"], data["delay"]["maximum"], data["user agent"]

    def pull_header(self, header):
        with open("settings/settings.json", "r") as f:
            data = json.load(f)
        return data["headers"][header]

    def pull_account(self, username):
        with open("accounts/accounts.json", "r") as f:
            data = json.load(f)
        for accounts in data:
            if accounts == username:
                return accounts, data[accounts]["password"], data[accounts]["proxy"], data[accounts]["pin"]

    def create_data_file(self, username):
        if not os.path.exists(f"data/{username}.json"):
            with open(f"data/{username}.json", "w") as f:
                json.dump({"ghoul catchers": {"neopoints gained": 0,"last run": 0},"shop of offers": {"neopoints gained": 0,"last run": 0},"trudys surprise": {"neopoints gained": 0,"last run": 0},"giant jelly": {"items gained": "","last run": 0},"kacheek seek": {"neopoints gained": 0,"last run": 0},"potato counter": {"neopoints gained": 0,"last run": 0}}, f, indent=4)

    def update_last_run(self, username, task):
        with open(f"data/{username}.json", "r+") as f:
            data = json.load(f)
            data[task]["last run"] = int(time.time())
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def update_neopoints_gained(self, username, task, neopoints):
        with open(f"data/{username}.json", "r+") as f:
            data = json.load(f)
            current_neopoints_gained = data[task]["neopoints gained"]
            current_neopoints_gained += neopoints
            data[task]["neopoints gained"] = current_neopoints_gained
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def update_items_gained(self, username, task, item):
        with open(f"data/{username}.json", "r+") as f:
            data = json.load(f)
            item_gained = data[task]["items gained"]
            if len(item_gained) > 0:
                item_gained += f", {item}"
            else:
                item_gained += item
            data[task]["items gained"] = item_gained
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def get_neopoints_on_hand(self, response):
        neopoints = self.get_between(response, "npanchor\" class=\"np-text__2020\">", "</span>")
        if self.contains(neopoints, ","):
            neopoints = neopoints.replace(",", "")
        return int(neopoints)

    def get_last_run(self, username, task):
        if not os.path.exists(f"data/{username}.json"):
            self.create_data_file(username)
        with open(f"data/{username}.json", "r") as f:
            data = json.load(f)
        return data[task]["last run"]

    def get_account_total(self):
        accounts = []
        with open("accounts/accounts.json", "r") as f:
            data = json.load(f)
        for account in data:
            accounts.append(account)
        return accounts

    def ensure_login(self, response):
        return False if "login-form" in response else True
