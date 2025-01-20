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
<<<<<<< HEAD
        return best_move

=======
        return best_move            


    @staticmethod
    def expectimax(board, dice_roll, depth, is_maximizing_player, is_chance_node,players):
        """
        Implements the Expectimax algorithm

        Parameters:
        ----------
        board : Board
            The current state of the game represented as a Board object.
        dice_roll : int
            The result of the dice roll for the current turn (1-6).
        depth : int
            The depth of the search tree. When depth reaches 0, the algorithm evaluates the board.
        is_maximizing_player : bool
            True if the current player is the maximizing player; False otherwise.
        is_chance_node : bool
            True if the current node represents a chance event (e.g., rolling a dice).
        players : list
            A list of players in the game, typically containing identifiers for each player (e.g., 'Blue' and 'Red').

        Returns:
        -------
        tuple
            A tuple containing:
            - float: The evaluated score of the board state based on the game's evaluation function.
            - Board or None: The best move as a Board object for the current player, or None if the node is a chance node.

        Notes:
        -----
        - If the depth reaches 0 or there is a terminal state (a winner is determined), the method returns the evaluated score.
        - The algorithm distinguishes between three types of nodes:
            1. Chance nodes: Evaluate the expected value based on possible dice rolls.
            2. Maximizing nodes: The AI chooses the best move to maximize the score.
            3. Minimizing nodes: The opponent chooses the move to minimize the score.

        Example:
        --------
        result, best_move = AI.expectimax(current_board, 4, 3, True, False, ['Blue', 'Red'])
        """
        if depth == 0 or board.check_winner(players) is not None:  # Terminal condition
            return board.evaluate(), board

        if is_chance_node:  # Chance node: Expectation over dice rolls
            expected_value = 0
            possible_dice_rolls = range(1, 7)  # Standard dice: rolls from 1 to 6
            for roll in possible_dice_rolls:
                probability = 1 / len(possible_dice_rolls)  # Uniform probability
                for new_board in board.get_possible_boards('Blue' if is_maximizing_player else 'Red', roll):
                    eval, _ = AI.expectimax(board, roll, depth - 1, is_maximizing_player, False,players)
                    expected_value += probability * eval
            return expected_value, None

        if is_maximizing_player:  # Maximizing player's turn
            max_eval = float('-inf')
            best_move = None
            for new_board in board.get_possible_boards('Blue', dice_roll):  
                eval, _ = AI.expectimax(board, dice_roll, depth - 1, False, True,players)
                if eval > max_eval:
                    max_eval = eval
                    best_move = new_board
            return max_eval, best_move

        else:  # Minimizing player's turn
            min_eval = float('inf')
            best_move = None
            for new_board in board.get_possible_boards('Red', dice_roll):
                eval, _ = AI.expectimax(board, dice_roll, depth - 1, True, True,players)
                if eval < min_eval:
                    min_eval = eval
                    best_move = new_board
            return min_eval, best_move
>>>>>>> e19bc451e4062e56f7f3cd822603e0b52e296ad7
