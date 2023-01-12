

class Difficulty:
    def __init__(self):
        self.difficulty_level = 1
        self.number_of_turns = 3
        self.unlocked_level = 1

    def unlock_level(self):
        self.unlocked_level += 1

    def choose_difficulty(self, new_difficulty):
        self.difficulty_level = int(new_difficulty)
        if self.difficulty_level > 1:
            self.number_of_turns = 2 * self.difficulty_level

        else:
            self.number_of_turns = 3
