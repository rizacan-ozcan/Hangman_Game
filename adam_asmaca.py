import random
import sqlite3
class Hangman:
    def __init__(self):
        self.connect = sqlite3.connect("hangman.db")
        self.cursor = self.connect.cursor()
        self.words = []
        self.hidden_word = []
        self.remaining_attempts = 10
        self.chosen_word = ""
        self.chosen_category = ""


    def get_words(self, difficulty):
        self.words = self.cursor.execute('''
            SELECT WORDS.WORD, WORDS.WORD_GROUP
            FROM WORDS
            JOIN WORD_GROUPS ON WORDS.WORD_GROUP = WORD_GROUPS.WORD_GROUP
            WHERE WORD_GROUPS.DIFFICULTY = ?       
        ''', (difficulty,)).fetchall()
        return self.words

    def select_difficulty(self):
        difficulty = input("Choose the difficulty level: (1: Easy, 2: Normal, 3: Hard): ")
        self.get_words(difficulty)
        if self.words:
            self.chosen_word, self.chosen_category = random.choice(self.words)
            print("Category hint:", self.chosen_category)
        else:
            print("No words found for the selected difficulty.")

    def hide_word(self):
        self.select_difficulty()
        self.chosen_word = self.chosen_word.lower()
        self.hidden_word = ['_'] * len(self.chosen_word)
        self.guessed_letters = []
        print(self.hidden_word)

    def play_game(self):
        self.remaining_attempts = 10
        self.hide_word()
        while '_' in self.hidden_word and self.remaining_attempts > 0:
            print("Your Word:", ' '.join(self.hidden_word))
            print("Remaining guesses:", self.remaining_attempts)
            guess = input("Guess a letter: ").lower()

            if guess in self.guessed_letters:
                print("You already guessed this letter, try another.")
                self.remaining_attempts -= 1
                continue

            self.guessed_letters.append(guess)

            if guess in self.chosen_word:
                print("Correct guess!")
                for i in range(len(self.chosen_word)):
                    if self.chosen_word[i] == guess:
                        self.hidden_word[i] = guess

            else:
                print("Incorrect guess. Try another.")
                self.remaining_attempts -= 1

        if '_' not in self.hidden_word:
            print("Congratulations! You have found the word:", self.chosen_word)
        else:
            print("You are out of your guesses. The correct word is:", self.chosen_word, "You typed: ", self.hidden_word)


hangman = Hangman()

while True:
    print(20 * "*", "Welcome to the Hangman Game", 20 * "*")
    hangman.play_game()





