import tkinter as tk
import random

# Classe principale du jeu
class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Game")
        self.colors = ["red", "blue", "green", "yellow"]
        self.sequence = []
        self.player_sequence = []
        self.is_player_turn = False
        self.is_game_over = False

        self.create_widgets()  # Crée les éléments graphiques de l'interface

    # Crée les éléments graphiques de l'interface
    def create_widgets(self):
        self.color_buttons_frame = tk.Frame(self.root)
        self.color_buttons_frame.pack()

        self.color_buttons = []
        for color in self.colors:
            button = tk.Button(self.color_buttons_frame, bg="white", width=10, height=3, command=lambda c=color: self.player_input(c), state=tk.DISABLED)
            button.pack(side=tk.LEFT)
            self.color_buttons.append(button)

        self.score_label = tk.Label(self.root, text="Score: 0")
        self.score_label.pack()

        self.message_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.message_label.pack()

        self.start_button = tk.Button(self.root, text="Start", command=self.start_game)
        self.start_button.pack()

    # Démarre le jeu
    def start_game(self):
        if self.is_game_over:
            self.message_label.config(text="")
            self.start_button.config(text="Start", state=tk.NORMAL)
            self.is_game_over = False
        else:
            self.sequence = []
            self.player_sequence = []
            self.is_player_turn = False
            self.score = 0
            self.update_score()
            self.start_button.config(text="Restart", state=tk.DISABLED)
            self.play_sequence()

    # Joue la séquence de couleurs à mémoriser
    def play_sequence(self):
        self.is_player_turn = False
        self.disable_buttons()
        self.sequence.append(random.choice(self.colors))
        self.show_sequence(0)

    # Affiche la séquence de couleurs
    def show_sequence(self, index):
        if index < len(self.sequence):
            color = self.sequence[index]
            button_index = self.colors.index(color)
            button = self.color_buttons[button_index]
            button.config(bg=color)
            self.root.update_idletasks()
            self.root.after(400, lambda: self.reset_button_color(button))
            self.root.after(600, lambda: self.show_sequence(index + 1))
        else:
            self.is_player_turn = True
            self.enable_buttons()

    # Réinitialise la couleur du bouton
    def reset_button_color(self, button):
        button.config(bg="white")
        self.root.update_idletasks()

    # Gère la sélection du joueur
    def player_input(self, color):
        if self.is_player_turn:
            self.player_sequence.append(color)
            button_index = self.colors.index(color)
            button = self.color_buttons[button_index]
            button.config(bg=color)
            self.root.update_idletasks()
            self.root.after(300, lambda: self.reset_button_color(button))
            if self.player_sequence == self.sequence:
                self.score += 1
                self.update_score()
                self.player_sequence = []
                self.is_player_turn = False
                self.disable_buttons()
                self.root.after(800, self.play_sequence)
            elif not self.check_sequence():
                self.end_game()

    # Vérifie si la séquence du joueur est correcte
    def check_sequence(self):
        return self.player_sequence == self.sequence[:len(self.player_sequence)]

    # Désactive les boutons
    def disable_buttons(self):
        for button in self.color_buttons:
            button.config(state=tk.DISABLED)

    # Active les boutons
    def enable_buttons(self):
        for button in self.color_buttons:
            button.config(state=tk.NORMAL)

    # Met à jour l'affichage du score
    def update_score(self):
        self.score_label.config(text="Score: {}".format(self.score))

    # Termine le jeu
    def end_game(self):
        self.is_game_over = True
        self.disable_buttons()
        self.start_button.config(text="Restart", state=tk.NORMAL)
        self.message_label.config(text="You lost! Your score: {}".format(self.score))

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
