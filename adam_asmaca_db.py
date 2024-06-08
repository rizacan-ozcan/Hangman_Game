import sqlite3


class Word:
    def __init__(self, word, word_group):
        self.word = word
        self.word_group = word_group

    def show_info(self):
        print(f"""
        Word: {self.word}
        Word Group: {self.word_group}
        """)

    def update_word(self):
        new_word = input("Enter the new word (if you enter blank, it will remain same): ")
        new_word_group = input("Enter the word group (if you enter blank, it will remain same): ")
        if new_word:
            self.word = new_word
        if new_word_group:
            self.word_group = new_word_group
        print("The word has been successfully updated.")


class WORDGROUPS:
    def __init__(self, word_group, difficulty):
        self.word_group = word_group
        self.difficulty = difficulty

    def show_info(self):
        print(f"""
        Word Group: {self.word_group}
        Difficulty: {self.difficulty}
        """)

    def update_word_group(self):
        new_word_group = input("Enter the word group (if you enter blank, it will remain same): ")
        new_difficulty = input("Enter the new difficulty (if you enter blank, it will remain same): ")
        if new_word_group:
            self.word_group = new_word_group
        if new_difficulty:
            self.difficulty = new_difficulty
        print("The word group has been successfully updated.")


class Enter_Word:
    def __init__(self):
        self.connect = sqlite3.connect("hangman.db")
        self.cursor = self.connect.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS WORDS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                WORD VARCHAR(100),
                WORD_GROUP VARCHAR(100),
                FOREIGN KEY (WORD_GROUP) REFERENCES WORD_GROUPS(WORD_GROUP)
            )
            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS WORD_GROUPS(
            WORD_GROUP PRIMARY KEY VARCHAR(100),
            DIFFICULTY INTEGER
            )
            ''')

    def add_word_group(self, word_group):
        self.cursor.execute('INSERT INTO WORD_GROUPS(WORD_GROUP, DIFFICULTY) VALUES(?, ?)',
                            (word_group.word_group, word_group.difficulty))
        self.connect.commit()
        print(f"{word_group.word_group} has been added to the system.")

    def add_words(self, word, word_group):
        row = self.cursor.execute('SELECT * FROM WORD_GROUPS WHERE WORD_GROUP = ?', (word_group,)).fetchone()
        if row:
            self.cursor.execute('INSERT INTO WORDS(WORD, WORD_GROUP) VALUES(?, ?)',
                                (word.word, word.word_group))
            self.connect.commit()
            print(f"{word.word} has been added to the system.")
        else:
            print("You should add the WORD_GROUPS first.")

    def show_words(self):
        rows = self.cursor.execute('SELECT * FROM WORDS').fetchall()
        if len(rows) > 0:
            for row in rows:
                word = Word(row[1], row[2])
                word.show_info()
        else:
            print("You have not added any words to the game.")

    def show_word_groups(self):
        rows = self.cursor.execute('SELECT * FROM WORD_GROUPS').fetchall()
        if len(rows) > 0:
            for row in rows:
                word_groups = WORDGROUPS(row[1], row[2])
                word_groups.show_info()
        else:
            print("You have not added any WORD_GROUPS to the game.")

    def delete_word_group(self, word_group):
        self.cursor.execute('DELETE FROM WORD_GROUPS WHERE WORD_GROUP = ?', (word_group,))
        self.connect.commit()
        print(f"{word_group} has been deleted from the game.")

    def delete_word(self, word):
        self.cursor.execute('DELETE FROM WORDS WHERE WORD = ?', (word,))
        self.connect.commit()
        print(f"{word} has been deleted from the game.")

    def update_word_group(self, word_group):
        row = self.cursor.execute('SELECT * FROM WORD_GROUPS WHERE WORD_GROUP = ?', (word_group,)).fetchone()
        if row:
            word_group = WORDGROUPS(row[1], row[2])
            word_group.update_word_group()
            self.cursor.execute('UPDATE WORD_GROUPS SET WORD_GROUP = ?, DIFFICULTY = ?', (word_group.word_group,
                                                                                       word_group.difficulty))
            self.connect.commit()
        else:
            print("WORD_GROUPS could not been found.")

    def update_word(self, word):
        row = self.cursor.execute('SELECT * FROM WORDS WHERE WORD = ?', (word,)).fetchone()
        if row:
            word = Word(row[1], row[2])
            word.update_word()
            self.cursor.execute('UPDATE WORD SET WORD = ?, WORD_GROUP = ?', (word.word,
                                                                             word.word_group))
            self.connect.commit()
        else:
            print("Word could not been found.")
