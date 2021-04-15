import random
import time

class lottery:
    def __init__(self, wrapper, functions, username):
        self.wrapper = wrapper
        self.functions = functions()
        self.username = username

    def play_lottery(self):
        tickets_bought, neopoints_spent = 0, 0
        response = self.wrapper.get("games/lottery.phtml", referer="https://thedailyneopets.com/dailies")
        if self.functions.get_neopoints_on_hand(self.wrapper.get("inventory.phtml").text) >= 2000:
            game_hash = self.functions.get_between(response.text, "_ref_ck' value='", "'>")
            for _ in range(20):
                numbers = [x for x in range(1, 31)]
                random.shuffle(numbers)
                response = self.wrapper.post("games/process_lottery.phtml", data={"_ref_ck": game_hash, "one": numbers[0], "two": numbers[1], "three": numbers[2], "four": numbers[3], "five": numbers[4], "six": numbers[5]}, referer="http://www.neopets.com/games/lottery.phtml")
                if self.functions.contains(response.text, "you cannot buy any more"):
                    print(f"[{self.username}] Lottery: You can't buy anymore lottery tickets")
                    break
                tickets_bought += 1
                neopoints_spent += 100
                delay = random.uniform(5, 35)
                print(f"[{self.username}] Lottery: Bought ticket #{tickets_bought} - {numbers[0]}, {numbers[1]}, {numbers[2]}, {numbers[3]}, {numbers[4]}, {numbers[5]} - sleeping for {int(delay)} seconds..")
                time.sleep(delay)
        return tickets_bought, neopoints_spent
