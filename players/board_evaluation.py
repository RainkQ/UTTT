from engine import MainBoardCoords, SubBoardCoords, SubBoard
from engine.main_board import MainBoard

class UniformEvaluator:
    def __init__(self):
        pass

    # evaluate how good a board with the move added
    # return a scalar value: F(board+move)
    def evaluate(self, board: MainBoard, move: (MainBoardCoords, SubBoardCoords)):
        return 1


