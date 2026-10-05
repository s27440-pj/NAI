"""
autorzy: Krystyna Tokarska (s27440), Jakub Gronostaj (s32362)
zasady gry: Mając początkową liczbę gracze dzielą ją kolejno przez dowolny jej dzielnik (mniejszy
niż sama liczba, chyba że taki nie istnieje).
Przegrywa gracz, któremu zostanie do podzielenia 1.
Przykład: początkowa liczba 40
gracz1 dzieli na 2 - zostaje 20
gracz2 dzieli na 2 - zostaje 10
gracz1 dzieli na 2 - zostaje 5
gracz2 dzieli na 5 - zostaje 1
gracz1 został z 1 - przegrywa

aby gra się uruchomiła należy zainstalować pakiet easyAI (pip install easyAI)
"""

from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
import math

def is_prime(n):
    """Checks if the given number is a prime number.

        Parameters:
        n (int): The number to check.

        Returns:
        bool: True if the number is prime, False otherwise.

        """
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

class DivisionGame(TwoPlayerGame):
    """A class representing a division game for two players."""
    def __init__(self, players, starting=30):
        """Initializes a new division game.

        Parameters:
        players (list): A list containing player objects (e.g., Human_Player, AI_Player).
        starting (int): The starting number for the game.

        Returns:
        None: Does not return a value.

        """
        self.players = players
        self.current_number = starting
        self.current_player = 1
        self._stack = []

    def possible_moves(self):
        """Determines all allowed moves (divisors) for the current number.

        Returns:
        list: A list of strings representing the possible divisors of the current number.

        """
        n = self.current_number
        if n <= 1:
            return []
        if is_prime(n):
            return [str(n)]
        else:
            return [str(d) for d in range(2, n) if n % d == 0]

    def make_move(self, move):
        """Executes a player's move by dividing the current number by the chosen divisor.

        Parameters:
        move (str): The chosen divisor passed as a string.

        Returns:
        None: Does not return a value.

        """
        d = int(move)
        if move not in self.possible_moves():
            raise ValueError(f"Unsupported move: {d}")

        self._stack.append(self.current_number)
        self.current_number //= d

    def undo_move(self, move):
        """Undoes the last executed move, restoring the previous number.

        Parameters:
        move (str): The move to be undone.

        Returns:
        None: Does not return a value.

        """
        self.current_number = self._stack.pop()

    def is_over(self):
        """Checks if the game is over (the current number is equal to 1).

        Returns:
        bool: True if the game is over, False otherwise.

        """
        return self.current_number == 1

    def show(self):
        """Displays the current game state and possible moves in the console.

        Returns:
        None: Does not return a value.

        """
        print(f"\nCurrent number: {self.current_number}")
        if not self.is_over():
            dividers = ", ".join(self.possible_moves())
            print(f"Possible divisors: [{dividers}]")

    def scoring(self):
        """Calculates the score for the artificial intelligence (AI) algorithm.

        Returns:
        int: -1 if the game is over (the current player loses), 0 during the game.

        """
        return -1 if self.is_over() else 0


if __name__ == "__main__":
    print("=== Division Game ===")
    try:
        inp = input("Enter the starting number (>=50) [by default 200]: ").strip()
        starting = int(inp) if inp else 200
    except Exception:
        print("Something went wrong! Let's start at 200")
        starting = 200

    if starting < 50:
        print("Number is too small! Let's start at 200")
        starting = 50

    players = [Human_Player(name="Human"), AI_Player(Negamax(6), name="AI")]
    game = DivisionGame(players, starting=starting)

    game.play()

    winner_index = 3 - game.current_player
    winner = game.players[winner_index - 1].name

    print("\n----------------------------------")
    print(f"End of game! Winner: {winner}!")
    print("----------------------------------\n")
