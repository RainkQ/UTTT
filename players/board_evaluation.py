from engine import MainBoardCoords, SubBoardCoords, SubBoard, Player
from engine.main_board import MainBoard


class UniformEvaluator:
    def __init__(self):
        pass

    # evaluate how good a board with the move added
    # return a scalar value: F(board+move)
    def evaluate(self, board: MainBoard, move: (MainBoardCoords, SubBoardCoords)):
        return 1


def line_others(m):
    result = {
        0: [(1, 2), (3, 6), (4, 8)],
        1: [(0, 2), (4, 7)],
        2: [(0, 1), (4, 6), (5, 8)],
        3: [(0, 6), (4, 5)],
        4: [(0, 8), (1, 7), (2, 6), (3, 5)],
        5: [(3, 4), (2, 8)],
        6: [(0, 3), (2, 4), (7, 8)],
        7: [(1, 4), (6, 8)],
        8: [(0, 4), (2, 5), (6, 7)],
    }
    return result.get(m)


def hash_list(board_int):
    total = 0
    for t in range(9):
        total += (board_int[t] + 2) * (10 ** t)
    return total


class WiningProbEvaluator(UniformEvaluator):
    APPROXIMATE_WIN_SCORE = 7
    BIG_BOARD_WEIGHT = 23
    WIN_SCORE = 10 ** 6
    POSSIBLE_WIN_SEQUENCES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

    def __init__(self):
        super().__init__()
        self.dic = {}
        board_int = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for it in range(3 ** 9):
            k = it
            for j in range(9):
                board_int[j] = int(k % 3 - 1)
                k -= k % 3
                k = k / 3
            board_score_template = [3, 2, 3,
                                    2, 4, 2,
                                    3, 2, 3]
            board_score = [0, 0, 0,
                           0, 0, 0,
                           0, 0, 0]
            for i in range(9):
                if board_int[i] == 1:
                    board_score[i] = board_score_template[i]
                    others = line_others(i)
                    for other_prob in others:
                        for place in other_prob:
                            if board_int[place] == -1:
                                board_score[i] = board_score[i] - 1
                                continue
                elif board_int[i] == -1:
                    board_score[i] = - board_score_template[i]
                    others = line_others(i)
                    for other_prob in others:
                        for place in other_prob:
                            if board_int[place] == 1:
                                board_score[i] = board_score[i] + 1
                                continue
            self.dic[hash_list(board_int)] = board_score

    def evaluate(self, board: MainBoard, move: (MainBoardCoords, SubBoardCoords)):
        if board.is_finished:
            winner = board.winner
            if winner == Player.ME:
                return self.WIN_SCORE
            elif winner == Player.OPPONENT:
                return -self.WIN_SCORE
            else:
                print("something is wrong" + winner)
                return 0
        board_as_mini = self.main2sub(board)
        ret = self.assess_board(board_as_mini) * self.BIG_BOARD_WEIGHT
        for i in range(9):
            miniB = board.get_sub_board(MainBoardCoords(int(i / 3), int(i % 3)))
            ret += self.assess_board(miniB)
        return ret

    def main2sub(self, main_board: MainBoard):
        sub_boards = SubBoard(3)
        for i in range(3):
            for j in range(3):
                sub = main_board.get_sub_board(MainBoardCoords(i, j))
                winner = sub.winner
                if winner == Player.ME:
                    sub_boards.add_move_inplace(SubBoardCoords(i, j), Player.Me)
                elif winner == Player.OPPONENT:
                    sub_boards.add_move_inplace(SubBoardCoords(i, j), Player.OPPONENT)
        return sub_boards

    def assess_board(self, board: SubBoard):
        board_str = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(9):
            place = board.__getitem__(int(i / 3)).__getitem__(int(i % 3))
            if place == Player.NONE:
                board_str[i] = 0
            elif place == Player.ME:
                board_str[i] = 1
            elif place == Player.OPPONENT:
                board_str[i] = -1
        return self.dic[hash_list(board_str)]
