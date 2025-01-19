from typing import List, Dict, Optional

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

    def display_board(self) -> None:
        print("\nBoard State:")
        print("Main Track:", self.board)
        for player in ['Red', 'Blue']:
            print(f"{player} tokens:", self.tokens[player])
            print(f"{player} home run:", self.home_runs[player])
        
    def getWall(self , player):
        """
        1.gets the possible walls for Player
             
        """
        opponent_walls = {}
        for i, pos in enumerate(self.tokens[player]):
            if isinstance(pos, int) and pos >= 0:  # Only consider tokens on main track
                if pos in opponent_walls:
                    opponent_walls[pos] += 1
                else:
                    opponent_walls[pos] = 1
        return opponent_walls
                
                    
                
                
                       


        
    
            
        
        