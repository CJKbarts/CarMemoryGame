
class Difficulty:
    def __init__(self):
        self.difficulty_level = 1
        self.number_of_turns = int(self.difficulty_level) * 3
        self.unlocked_level = 1
        self.choose_difficulty_succeeded = False

    def unlock_level(self):
        self.unlocked_level += 1

    def choose_difficulty(self, new_difficulty):
        if self.unlocked_level >= new_difficulty:
            self.difficulty_level = new_difficulty
            self.number_of_turns = self.difficulty_level * 2
            self.choose_difficulty_succeeded = True


