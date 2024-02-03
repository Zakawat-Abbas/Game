import sys


class RedBlueNim:
    def __init__(
        self, num_red, num_blue, version="standard", first_player="computer", depth=3
    ):
        self.num_red = num_red
        self.num_blue = num_blue
        self.version = version
        self.first_player = first_player
        self.depth = depth
        self.is_misere = version == "misère"
        self.current_state = [num_red, num_blue]

    def evaluate_state(self, red, blue):
        return red * 2 + blue * 3

    def min_max(self, state, depth, alpha, beta, is_maximizing, is_misere):
        if depth == 0 or state[0] == 0 or state[1] == 0:
            return self.evaluate_state(state[0], state[1])

        if is_maximizing:
            max_eval = float("-inf")
            for pile, count in enumerate(state):
                if count > 0:
                    new_state = state[:]
                    new_state[pile] -= 1
                    eval = self.min_max(
                        new_state, depth - 1, alpha, beta, False, is_misere
                    )
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float("inf")
            for pile, count in enumerate(state):
                if count > 0:
                    new_state = state[:]
                    new_state[pile] -= 1
                    eval = self.min_max(
                        new_state, depth - 1, alpha, beta, True, is_misere
                    )
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def find_best_move(self):
        best_move = None
        best_eval = float("-inf") if self.is_misere else float("inf")
        for pile, count in enumerate(self.current_state):
            if count > 0:
                new_state = self.current_state[:]
                new_state[pile] -= 1
                eval = self.min_max(
                    new_state,
                    self.depth,
                    float("-inf"),
                    float("inf"),
                    False,
                    self.is_misere,
                )
                if self.is_misere:
                    if eval > best_eval:
                        best_eval = eval
                        best_move = (pile, 1)
                else:
                    if eval < best_eval:
                        best_eval = eval
                        best_move = (1, pile)
        return best_move

    def play_game(self):
        while not (self.current_state[0] == 0 or self.current_state[1] == 0):
            if self.first_player == "computer":
                pile, marbles = self.find_best_move()
                print(
                    f"Computer pick 1 marble from {('Red' if pile == 0 else 'Blue')} pile."
                )
                self.current_state[pile] -= 1
            else:
                print(
                    "Red Pile: ",
                    self.current_state[0],
                    ", Blue Pile: ",
                    self.current_state[1],
                )
                pile = int(input("Pick a pile (0 for Red OR 1 for Blue): "))
                self.current_state[pile] -= 1

            self.first_player = "computer" if self.first_player == "human" else "human"

        final_score = self.evaluate_state(self.current_state[0], self.current_state[1])
        if self.current_state[0] == 0 or self.current_state[1] == 0:
            print(self.first_player.capitalize(), "wins and score is", final_score)


if __name__ == "__main__":
    num_red = int(sys.argv[1])
    num_blue = int(sys.argv[2])
    version = sys.argv[3] if len(sys.argv) > 3 else "standard"
    first_player = sys.argv[4] if len(sys.argv) > 4 else "computers"
    depth = int(sys.argv[5]) if len(sys.argv) > 5 else 3

    is_misere = version == "misère"

    current_state = [num_red, num_blue]

    game = RedBlueNim(num_red, num_blue, version, first_player, depth)
    game.play_game()
