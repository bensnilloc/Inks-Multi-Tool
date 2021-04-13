class giant_jelly:
    def __init__(self, wrapper, functions, username):
        self.wrapper = wrapper
        self.functions = functions()
        self.username = username

    def grab_jelly(self):
        response = self.wrapper.get("jelly/jelly.phtml", referer="https://thedailyneopets.com/dailies")
        if not self.functions.ensure_login(response.text):
            self.wrapper.login()
        response = self.wrapper.post("jelly/jelly.phtml", data={"type": "get_jelly"}, referer=response.url)
        if self.functions.contains(response.text, "You take some"):
            jelly_taken = self.functions.get_between(response.text, "You take some <strong>", "</strong>")
            print(f"[{self.username}] Giant Jelly: Grabbed {jelly_taken}")
            return jelly_taken
        print(f"[{self.username}] Giant Jelly: It's too soon to take any jelly..")
        return False