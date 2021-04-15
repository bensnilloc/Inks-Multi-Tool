class obsidian_quarry:
    def __init__(self, wrapper, functions, username):
        self.wrapper = wrapper
        self.functions = functions()
        self.username = username

    def visit_obsidian_quarry(self):
        response = self.wrapper.get("magma/quarry.phtml", referer="https://thedailyneopets.com/dailies")
        if self.functions.contains(response.text, "has been added to your"):
            print(f"[{self.username}] Obsidian Quarry: Shiny Obsidian has been added to your inventory!")
            return True
        print(f"[{self.username}] Obsidian Quarry: It's too soon to take a Shiny Obsidian..")
        return False
