import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
import random

class Word(toga.App):

    valid_alphabet = set("abcdefghijklmnopqrstuvwxyz")  # Define a set with all the alphabets
    file_path = "english_words.txt"
    with open(file_path, "r") as file:
        all_words = [line.strip() for line in file]

    # Styles
    title_style1 = Pack(text_align="center", font_size=24, font_weight="bold", color="white", padding=10, background_color="brown")
    title_style2 = Pack(text_align="center", font_size=24, font_weight="bold", color="white", padding=10)
    button_style = Pack(padding=10, font_size=14, text_align="center", background_color="black", color="white", width=200)
    title_style = Pack(padding=10, font_size=20, text_align="center", font_weight="bold", color="white")
    secret_word_style = Pack(padding=10, font_size=25, text_align="center", font_weight="bold", color="white")
    box_style = Pack(direction=COLUMN, alignment=CENTER, background_color="skyblue")

    def startup(self):
        self.secret_word = ""

        label1 = toga.Label("Word Game", style=Word.title_style1)
        button1 = toga.Button("Play Word Game", style=Word.button_style, on_press=self.start_new_game)
        button2 = toga.Button("Start game with own word", style=Word.button_style, on_press=self.enter_own_word)

        main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, padding=20, background_color="skyblue"))
        main_box.add(label1)
        main_box.add(button1)
        main_box.add(button2)

        self.main_window = toga.MainWindow(title="Simple Window")
        self.main_window.content = main_box
        self.main_window.show()

    def get_word(self):
        random_item = random.choice(Word.all_words)
        return random_item

    def start_new_game(self, widget):
        if widget.text == "Play Word Game" or widget.text == "Start a New Game":
            self.secret_word = self.get_word()  # Get a random word

        print(self.secret_word)

        self.secret_letters = set(self.secret_word.lower())
        self.used_letters = []
        self.lives = 7
        self.correct_letters = set()
        self.revealed_word = ["_"] * len(self.secret_word)
        self.game_state()

    def game_state(self):
        box = toga.Box(style=Word.box_style)

        # Heading
        box.add(toga.Label("Guess a Letter!", style=Word.title_style))
        box.add(toga.Label("Word: " + " ".join(self.revealed_word), style=Word.title_style))

        # Adding a text input and validating the input
        input_txt = toga.TextInput(placeholder="Enter Your Word Here", on_change=self.process_letter)
        box.add(input_txt)

        # Used letters + lives
        box.add(toga.Label("Used Letters: " + " ".join(self.used_letters), style=Word.title_style))
        box.add(toga.Label("Lives: " + str(self.lives), style=Word.title_style))

        # Buttons
        box.add(toga.Button("Start a New Game", style=Word.button_style, on_press=self.start_new_game))
        box.add(toga.Button("Start game with own word", style=Word.button_style, on_press=self.enter_own_word))

        self.main_window.content = box
        input_txt.focus()

    def process_letter(self, widget):  # Function to check if only letters are entered
        lowercase = widget.value.lower()  # Convert all the letters to lowercase
        if lowercase in Word.valid_alphabet:  # If it is present in the alphabet list defined by user
            if lowercase in self.secret_letters:  # If secret_letter is in word, replace underscore with letter
                self.correct_letters = self.correct_letters.union(widget.value)
                for i in range(len(self.secret_word)):  # Iterates through each character in secret word
                    if self.secret_word[i].upper() in self.correct_letters or self.secret_word[i].lower() in self.correct_letters:  # Checks if a letter is already guessed by user
                        self.revealed_word[i] = self.secret_word[i]  # If yes, then underscore is replaced with letter

            elif lowercase not in self.used_letters:
                self.lives = self.lives - 1  # Decrease lives by 1
                self.used_letters.append(lowercase)  # Adding the letter user has entered
            else:
                print('Already Used, type another letter')

        else:
            print('Not a valid alphabet')

        if self.lives == 0:  # Check if game is over
            self.end_game(victory=False)  # Call the function with victory set to false which means user has not won
        elif "_" not in self.revealed_word:  # If there is no _
            self.end_game(victory=True)  # Call the function with victory set to true
        else:
            self.game_state()

    def end_game(self, victory):  # Define function to end the game
        box = toga.Box(style=Word.box_style)  # Create a new box

        if victory:  # If user has won
            box.add(toga.Label("You won! :)", style=Word.title_style1))
            img_path = "happy.PNG"
        else:  # If user has lost
            box.add(toga.Label("You lost! :(", style=Word.title_style2))
            img_path = "sad.PNG"

        box.add(toga.Label("The word was: " + self.secret_word, style=Word.secret_word_style))
        box.add(toga.Button("Start a New Game", style=Word.button_style, on_press=self.start_new_game))
        box.add(toga.Button("Start game with own word", style=Word.button_style, on_press=self.enter_own_word))
        box.add(toga.ImageView(image=img_path))

        self.main_window.content = box
        self.main_window.show()

    def enter_own_word(self, widget):  # Define function to allow user to enter the word
        box = toga.Box(style=Word.box_style)
        box.add(toga.Label("Enter your secret word:", style=Word.title_style))
        input_txt2 = toga.TextInput(placeholder="Enter Your Word Here", on_change=self.update_secret_word_handler)
        box.add(input_txt2)
        box.add(toga.Button("Start Game", style=Word.button_style, on_press=self.start_new_game))
        self.main_window.content = box
        self.main_window.show()
        input_txt2.focus()

    def update_secret_word_handler(self, widget):  # Define function to update the secret_word
        self.secret_word = widget.value

app = Word('Simple Toga App', 'org.example.simpletoga')
app.main_loop()

