import random
from typing import List, Dict, Optional
from copy import deepcopy
from board import Board
from ai import AI

class LudoGame:
    def __init__(self):
        self.players = ['Red', 'Blue']
        self.board = Board()

    def roll_dice(self) -> int:
        return random.randint(1, 6)
  
    def play_turn(self, player: str,dice_roll) -> bool:
        print(f"\n{player} rolled a {dice_roll}")
        
        valid_moves = self.board.get_valid_moves(player, dice_roll)
        
        if not valid_moves:
            print(f"No valid moves for {player}")
            return False
        if player == 'Red':
            best_move = AI.expectimax(self.board, dice_roll, 1, False, False,self.players) 
        if player == 'Blue':
            best_move = AI.expectimax(self.board, dice_roll, 1, True, False,self.players)

        boards = self.board.get_possible_boards(player,dice_roll)
        print('---------------------\nposssible boards:')
        for i in range(len(boards)):
            print (f'* possible board {i + 1} :')
            boards[i].display_board()
        print ('------------------------')
        _,self.board= best_move
        # move = AI.simple_ai(self,valid_moves,player,dice_roll)

        # self.board.move_token(player,move,dice_roll)
        return True

    def play_game(self) -> None:
        turn = 0
        while True:
            current_player = self.players[turn % 2]
            self.board.display_board()
            dice_roll = self.roll_dice()
            self.play_turn(current_player , dice_roll)
            if dice_roll != 6:
                turn +=1
            winner = self.board.check_winner(self.players)
            if winner:
                print(f"\n{winner} wins the game!")
                break