import requests
import json
import time
import random
import os
from classes.functions import functions

class wrapper:
    def __init__(self, username, password, proxy):
        self.session = requests.Session()
        self.functions = functions()
        self.base = "http://www.neopets.com/"
        self.minimum_delay = self.functions.parse_settings()[0]
        self.maximum_delay = self.functions.parse_settings()[1]
        self.user_agent = self.functions.parse_settings()[2]
        self.username = username
        self.password = password
        if self.functions.contains(proxy, ":"):
            self.set_proxy(proxy)

    def set_proxy(self, proxy):
        self.session.proxies.update({"http": f"http://{proxy}", "https": f"https://{proxy}"})

    def url(self, path):
        return f"{self.base}{path}"

    def get(self, path, referer = None):
        self.functions.delay(self.minimum_delay, self.maximum_delay)
        accept, accept_encoding, accept_language = self.functions.pull_header("accept"), self.functions.pull_header("accept-encoding"), self.functions.pull_header("accept-language")
        response = self.session.get(self.url(path), headers={"Accept": accept, "Accept-Encoding": accept_encoding, "Accept-Language": accept_language, "Referer": referer, "User-Agent": self.user_agent})
        self.save_cookies()
        return response

    def post(self, path, data = None, referer = None):
        self.functions.delay(self.minimum_delay, self.maximum_delay)
        accept, accept_encoding, accept_language = self.functions.pull_header("accept"), self.functions.pull_header("accept-encoding"), self.functions.pull_header("accept-language")
        if data:
            response = self.session.post(self.url(path), data=data, headers={"Accept": accept, "Accept-Encoding": accept_encoding, "Accept-Language": accept_language, "Referer": referer, "User-Agent": self.user_agent})
        else:
            response = self.session.post(self.url(path), headers={"Accept": accept, "Accept-Encoding": accept_encoding, "Accept-Language": accept_language, "Referer": referer, "User-Agent": self.user_agent})
        self.save_cookies()
        return response

    def login(self):
        if self.cookie_login():
            print(f"[+] Cookies are valid, logged in as {self.username}")
            return True
        response = self.post("login.phtml", data={"destination": "", "return_format": "1", "username": self.username, "password": self.password})
        if not self.functions.contains(response.text, "npanchor"):
            print(f"[-] Unable to login as {self.username}. Check your username/password?")
            return False
        print(f"[+] Logged in as {self.username}")
        return True

    def save_cookies(self):
        with open(f"cookies/{self.username}.json", "w") as f:
            json.dump(self.session.cookies.get_dict(), f, indent=4)

    def parse_cookies(self):
        with open(f"cookies/{self.username}.json", "r") as f:
            return json.load(f)

    def cookie_login(self):
        if not os.path.exists(f"cookies/{self.username}.json"):
            return False
        self.session.cookies.update(self.parse_cookies())
        if self.functions.contains(self.get("inventory.phtml").text, "npanchor"):
            return True
        return False
