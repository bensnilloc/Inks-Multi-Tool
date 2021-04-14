import re
import time
import random

class potato_counter:
    def __init__(self, wrapper, functions, username):
        self.wrapper = wrapper
        self.functions = functions()
        self.username = username

    def play_potato_counter(self):
        response = self.wrapper.get("medieval/potatocounter.phtml", referer="https://thedailyneopets.com/dailies")
        while "me potatoes three times a day" not in response.text:
            response = self.wrapper.get("medieval/potatocounter.phtml", referer="https://thedailyneopets.com/dailies")
            potatos = self.functions.get_between(response.text, "potato_think.gif", "form action='potatocounter")
            total_potatos = len(re.findall(r"potato\d.gif", potatos))
            if total_potatos > 0:
                if total_potatos <= 100:
                    delay = random.uniform(10, 20)
                else:
                    delay = random.uniform(150, 350)
                print(f"[{self.username}] Potato Counter: There are {total_potatos} potatos - sleeping for {int(delay)} seconds before guessing..")
                time.sleep(delay)
                response = self.wrapper.post("medieval/potatocounter.phtml", data={"type": "guess", "guess": total_potatos}, referer=response.url)
                if int(delay) <= 100:
                    print(f"[{self.username}] Potato Counter: You won 75 neopoints!")
                else:
                    print(f"[{self.username}] Potato Counter: You won 50 neopoints!")