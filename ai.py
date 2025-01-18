class AI:
        

    def simple_ai(game,valid_moves,player,dice_roll):
        """
        Simple AI: Prioritize moving tokens that are:
        1. In yard when rolling 6
        2. Close to entering home run
        3. Already on the board

        returns:
            - best_move(int) : the best token to move
        """

        for i in valid_moves:
            pos = game.board.tokens[player][i]
            if pos == -1 and dice_roll == 6:
                return i
                
        # Try to move token closest to home run
        best_move = valid_moves[0]
        max_progress = -1
        for i in valid_moves:
            pos = game.board.tokens[player][i]
            if isinstance(pos, tuple):  # Already in home run
                progress = 52 + pos[1]
            elif pos != -1:  # On main track
                if player == 'Red':
                    progress = pos if pos <= 51 else pos - 52
                else:
                    progress = pos if pos <= 25 else pos - 52
                if progress > max_progress:
                    max_progress = progress
                    best_move = i
        return best_move            
