import urllib.parse
import time
import random

class trudys_surprise:
    def __init__(self, wrapper, functions, username):
        self.wrapper = wrapper
        self.functions = functions()
        self.username = username

    def play_trudys_surprise(self):
        response = self.wrapper.get("trudys_surprise.phtml", referer="https://thedailyneopets.com/dailies")
        if not self.functions.ensure_login(response.text):
            self.wrapper.login()
        if self.functions.contains(response.text, "&slt=1"):
            trudy_daily = self.functions.get_between(response.text, "src=\"/trudydaily/", "\" name")
            response = self.wrapper.get(f"trudydaily/{trudy_daily}", referer=response.url)
            key = urllib.parse.unquote(self.functions.get_between(response.text, "'key': '", "'};"))
            self.wrapper.post("trudydaily/ajax/claimprize.php", data={"action": "getslotstate", "key": key}, referer="http://www.neopets.com/trudys_surprise.phtml")
            time.sleep(random.uniform(10, 35))
            self.wrapper.post("trudydaily/ajax/claimprize.php", data={"action": "beginroll"}, referer="http://www.neopets.com/trudys_surprise.phtml")
            time.sleep(random.uniform(20, 60))
            self.wrapper.post("trudydaily/ajax/claimprize.php", data={"action": "prizeclaimed"}, referer="http://www.neopets.com/trudys_surprise.phtml")
