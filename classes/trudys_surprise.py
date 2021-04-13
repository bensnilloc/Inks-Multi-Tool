import urllib.parse
import time
import random
from classes.functions import functions

class trudys_surprise:
    def __init__(self, wrapper):
        self.wrapper = wrapper
        self.functions = functions()

    def play_trudys_surprise(self):
        response = self.wrapper.get("trudys_surprise.phtml", referer="https://thedailyneopets.com/dailies")
        if self.functions.contains(response.text, "&slt=1"):
            trudy_daily = self.functions.get_between(response.text, "src=\"/trudydaily/", "\" name")
            response = self.wrapper.get(f"trudydaily/{trudy_daily}", referer=response.url)
            key = urllib.parse.unquote(self.functions.get_between(response.text, "'key': '", "'};"))
            self.wrapper.post("trudydaily/ajax/claimprize.php", data={"action": "getslotstate", "key": key}, referer="http://www.neopets.com/trudys_surprise.phtml")
            self.wrapper.post("trudydaily/ajax/claimprize.php", data={"action": "beginroll"}, referer="http://www.neopets.com/trudys_surprise.phtml")
            self.wrapper.post("trudydaily/ajax/claimprize.php", data={"action": "prizeclaimed"}, referer="http://www.neopets.com/trudys_surprise.phtml")
