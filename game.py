import random
from typing import List, Dict, Optional
from board import Board
from ai import AI

class LudoGame:
    def __init__(self):
        self.players = ['Red', 'Blue']
        self.board = Board()

    def roll_dice(self) -> int:
        return random.randint(1, 6)

    def is_valid_move(self, player: str, token_index: int, steps: int) -> bool:
        current_pos = self.board.tokens[player][token_index]
        
        # Token in yard needs a 6 to start
        if current_pos == -1:
            return steps == 6
            
        # Check if token is in home run
        if isinstance(current_pos, tuple):
            home_run_pos = current_pos[1]
            new_pos = home_run_pos + steps
            return new_pos < 6  # Must land exactly in finishing square
            
        # Calculate new position on main track
        new_pos = (current_pos + steps) % 52
        
        # Check if token should enter home run
        if player == 'Red' and current_pos <= 51 and current_pos + steps > 51:
            home_run_steps = (current_pos + steps) - 51 - 1
            return home_run_steps < 6
        elif player == 'Blue' and current_pos <= 25 and current_pos + steps > 25:
            home_run_steps = (current_pos + steps) - 25 - 1
            return home_run_steps < 6
            
        return True

    def move_token(self, player: str, token_index: int, steps: int) -> bool:
        if not self.is_valid_move(player, token_index, steps):
            return False
            
        current_pos = self.board.tokens[player][token_index]
        
        # Moving from yard to start position
        if current_pos == -1:
            if steps == 6:
                start_pos = self.board.start_positions[player]
                if self.board.board[start_pos] is None or self.board.board[start_pos] == player:
                    self.board.board[start_pos] = player
                    self.board.tokens[player][token_index] = start_pos
                    return True
            return False
            
        # Moving in home run
        if isinstance(current_pos, tuple):
            home_run_pos = current_pos[1]
            new_pos = home_run_pos + steps
            if new_pos < 6:
                self.board.home_runs[player][home_run_pos] = None
                self.board.home_runs[player][new_pos] = player
                self.board.tokens[player][token_index] = (player, new_pos)
                return True
            return False
            
        # Clear current position on main track
        self.board.board[current_pos] = None
        
        # Calculate new position
        new_pos = (current_pos + steps) % 52
        
        # Check if token should enter home run
        if (player == 'Red' and current_pos <= 51 and current_pos + steps > 51) or \
           (player == 'Blue' and current_pos <= 25 and current_pos + steps > 25):
            entry_point = self.board.home_run_entries[player]
            home_run_steps = (current_pos + steps - entry_point - 1) % 52
            if home_run_steps < 6:
                self.board.home_runs[player][home_run_steps] = player
                self.board.tokens[player][token_index] = (player, home_run_steps)
                return True
            return False
            
        # Handle capture
        if self.board.board[new_pos] is not None and \
           self.board.board[new_pos] != player and \
           new_pos not in self.board.safe_positions['main'] and \
           new_pos != self.board.safe_positions[self.board.board[new_pos]]:
            self.board.send_token_home(self.board.board[new_pos], new_pos)
            
        # Update board and token position
        self.board.board[new_pos] = player
        self.board.tokens[player][token_index] = new_pos
        return True

    def get_valid_moves(self, player: str, dice_roll: int) -> List[int]:
        valid_moves = []
        for i in range(4):
            if self.is_valid_move(player, i, dice_roll):
                valid_moves.append(i)
        return valid_moves

    def play_turn(self, player: str) -> bool:
        dice_roll = self.roll_dice()
        print(f"\n{player} rolled a {dice_roll}")
        
        valid_moves = self.get_valid_moves(player, dice_roll)
        
        if not valid_moves:
            print(f"No valid moves for {player}")
            return False
        
        best_move = AI.simple_ai(game=self, valid_moves = valid_moves, player=player, dice_roll=dice_roll)           
        self.move_token(player, best_move, dice_roll)
        return True

    def check_winner(self) -> Optional[str]:
        for player in self.players:
            tokens_home = 0
            for pos in self.board.tokens[player]:
                if isinstance(pos, tuple) and pos[1] == 5:  # Reached end of home run
                    tokens_home += 1
            if tokens_home == 4:
                return player
        return None

    def play_game(self) -> None:
        turn = 0
        while True:
            current_player = self.players[turn % 2]
            self.board.display_board()
            self.play_turn(current_player)
            
            winner = self.check_winner()
            if winner:
                print(f"\n{winner} wins the game!")
                break 
            turn += 1