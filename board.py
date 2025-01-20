from typing import List, Dict, Optional
from copy import deepcopy


class Board:
    def __init__(self):
        # Main track positions (0-51)
        self.board = [None] * 52
        
        # Starting positions on main track
        self.start_positions = {'Red': 0, 'Blue': 26}
        
        # Home positions for each player
        self.tokens = {
            'Red': [-1, -1, -1, -1],   # -1 means token is in yard
            'Blue': [-1, -1, -1, -1]
        }
        
        # Home run tracks (6 spaces before finishing)
        self.home_runs = {
            'Red': [None] * 6,
            'Blue': [None] * 6
        }
        
        # Where tokens enter home run
        self.home_run_entries = {'Red': 51, 'Blue': 25}
        
        # Safe spots where tokens cannot be captured
        self.safe_positions = {
            'main': [0, 8, 13, 21, 26, 34, 39, 47],  # Star positions
            'Red': 0,    # Starting positions are safe
            'Blue': 26
        }

    def send_token_home(self, player: str, position: int) -> None:
        for i, pos in enumerate(self.tokens[player]):
            if pos == position:
                self.tokens[player][i] = -1
                break

    def move_token(self, player: str, token_index: int, steps: int) -> bool:
        if not self.is_valid_move(player, token_index, steps):
            return False
        
        current_pos = self.tokens[player][token_index]
        # Moving from yard to start position
        if current_pos == -1:
            if steps == 6:
                start_pos = self.start_positions[player]
                if self.board[start_pos] is None or self.board[start_pos] == player:
                    self.board[start_pos] = player
                    self.tokens[player][token_index] = start_pos
                    return True
            return False
            
        # Moving in home run
        if isinstance(current_pos, tuple):
            home_run_pos = current_pos[1]
            new_pos = home_run_pos + steps
            if new_pos < 6:
                self.home_runs[player][home_run_pos] = None
                self.home_runs[player][new_pos] = player
                self.tokens[player][token_index] = (player, new_pos)
                return True
            return False
            
        # Clear current position on main track
        self.board[current_pos] = None
        
        # Calculate new position
        new_pos = (current_pos + steps) % 52
    
                    
        # Check if token should enter home run
        if (player == 'Red' and current_pos <= 51 and current_pos + steps > 51) or \
           (player == 'Blue' and current_pos <= 25 and current_pos + steps > 25):
            entry_point = self.home_run_entries[player]
            home_run_steps = (current_pos + steps - entry_point - 1) % 52
            if home_run_steps < 6:
                self.home_runs[player][home_run_steps] = player
                self.tokens[player][token_index] = (player, home_run_steps)
                return True
            return False
        
        # Handle capture
        if self.board[new_pos] is not None and \
           self.board[new_pos] != player and \
           new_pos not in self.safe_positions['main'] and \
           new_pos != self.safe_positions[self.board[new_pos]]:
            self.send_token_home(self.board[new_pos], new_pos)
            
        # Update board and token position
        self.board[new_pos] = player
        self.tokens[player][token_index] = new_pos
        return True
    
    def is_valid_move(self, player: str, token_index: int, steps: int) -> bool:
        current_pos = self.tokens[player][token_index]
        
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
        
        opponent = "Red"
        if player == "Red":
            opponent = "Blue"

        # Get positions where opponent has walls
        opponent_walls = self.getWall(opponent)
        for wall_pos, count in opponent_walls.items():
            if count >= 2:  # It's a wall
                print('opponent-wall' , opponent_walls)
                # If wall is between current position and new position
                # and new position is NOT beyond the wall, move is invalid
                if current_pos < wall_pos < new_pos:
                    return False

        # Check if token should enter home run
        if player == 'Red' and current_pos <= 51 and current_pos + steps > 51:
            home_run_steps = (current_pos + steps) - 51 - 1
            return home_run_steps < 6
        elif player == 'Blue' and current_pos <= 25 and current_pos + steps > 25:
            home_run_steps = (current_pos + steps) - 25 - 1
            return home_run_steps < 6
        return True
    
    def get_valid_moves(self, player: str, dice_roll: int) -> List[int]:
        valid_moves = []
        for i in range(4):
            if self.is_valid_move(player, i, dice_roll):
                valid_moves.append(i)
        return valid_moves
  
    def get_possible_boards(self, player, dice_roll):
        boards = []
        moves = self.get_valid_moves(player,dice_roll)
        for move in moves:
            board = deepcopy(self)
            board.move_token(player,move,dice_roll)
            boards.append(board)
        return boards
    
    def check_winner(self,players) -> Optional[str]:
        for player in players:
            tokens_home = 0
            for pos in self.tokens[player]:
                if isinstance(pos, tuple) and pos[1] == 5:  # Reached end of home run
                    tokens_home += 1
            if tokens_home == 4:
                return player
        return None
    
    def distance(self,player):
        distance_sum = 0
        player_tokens = self.tokens[player]
        for token in player_tokens:
            if isinstance(token,tuple) :
                distance = 5 - token[1]
            else:
                distance = self.home_run_entries[player] - token
            distance_sum += distance
        return distance_sum

    def evaluate(self):
        return self.distance('Red') - self.distance('Blue')

    def display_board(self) -> None:
        print("\nBoard State:")
        print("Main Track:", self.board)
        for player in ['Red', 'Blue']:
            print(f"{player} tokens:", self.tokens[player])
            print(f"{player} home run:", self.home_runs[player])