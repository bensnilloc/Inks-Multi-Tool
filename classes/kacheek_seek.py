import time
import random

class kacheekseek:
    def __init__(self, wrapper, functions, username):
        self.wrapper = wrapper
        self.functions = functions()
        self.username = username

    def seek(self, seek = True):
        neopoints_won = 0
        finding_places = [1, 2, 3, 4, 5]
        response = self.wrapper.get("games/hidenseek.phtml", referer="https://thedailyneopets.com/dailies")
        self.wrapper.get("games/hidenseek/0.phtml?xfn=", referer=response.url)
        while seek:
            if not self.functions.ensure_login(response.text):
                self.wrapper.login()
            random.shuffle(finding_places)
            for data in finding_places:
                response = self.wrapper.get(f"games/process_hideandseek.phtml?p={data}&game=0", referer="http://www.neopets.com/games/hidenseek/0.phtml?xfn=")
                if self.functions.contains(response.text, "Oh... you found me"):
                    game_prize = self.functions.get_between(response.text, "You win <b>", "</b> Neopoints!!!")
                    neopoints_won += int(game_prize)
                    delay = random.uniform(5, 15)
                    print(f"[{self.username}] Kacheek Seek: You won {game_prize} NP - sleeping for {int(delay)} seconds..")
                    time.sleep(delay)
                    break
                if self.functions.contains(response.text, "Im SO BORED"):
                    print(f"[{self.username}] Kacheek Seek: Pet is bored, task stopped")
                    seek = False
                    break