from classes.functions import functions

class giant_jelly:
    def __init__(self, wrapper):
        self.wrapper = wrapper
        self.functions = functions()

    def grab_jelly(self):
        response = self.wrapper.get("jelly/jelly.phtml", referer="https://thedailyneopets.com/dailies")
        response = self.wrapper.post("jelly/jelly.phtml", data={"type": "get_jelly"}, referer=response.url)
        if self.functions.contains(response.text, "You take some"):
            return self.functions.get_between(response.text, "You take some <strong>", "</strong>")
        return False