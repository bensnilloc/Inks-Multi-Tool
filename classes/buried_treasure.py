import random

class buried_treasure:
    def __init__(self, wrapper, functions, username):
        self.wrapper = wrapper
        self.functions = functions()
        self.username = username

    def play_buried_treasure(self):
        response = self.wrapper.get("pirates/buriedtreasure/buriedtreasure.phtml", referer="https://thedailyneopets.com/dailies")
        if not self.functions.contains(response.text, "Your account must be at least <b>24</b> hours old to play"):
            if not self.functions.contains(response.text, "you have to wait another"):
                x, y = random.randint(25, 450), random.randint(45, 460)
                response = self.wrapper.get(f"pirates/buriedtreasure/buriedtreasure.phtml?{x},{y}", referer=response.url)
                game_prize = self.functions.get_between(response.text, "<b><center>", "</center></b>")
                if self.functions.contains(response.text, "are now eligible to use"):
                    print(f"[{self.username}] Buried Treasure: {game_prize} - You also won the avatar!")
                    return True
                else:
                    print(f"[{self.username}] Buried Treasure: {game_prize}")
            else:
                print(f"[{self.username}] Buried Treasure: You have to wait before playing again..")
        else:
            print(f"[{self.username}] Buried Treasure: Your account is too young to play..")
        return False