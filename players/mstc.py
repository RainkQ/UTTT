from engine import MainBoardCoords, SubBoardCoords, SubBoard
from players.stdout import StdOutPlayer
from players.mstc_util import *

class MSTCPlayer(StdOutPlayer):
    def __init__(self, reuse_board=False):
        super().__init__()
        self.algo = MSTCAlgo(self, 0.4)
        self.reuse_board = reuse_board

    def get_my_move(self):  # -> Tuple[MainBoardCoords, SubBoardCoords]
        if not self.reuse_board:
            self.algo.update_root(None)    
        else:
            self.algo.update_root(self.last_opponent_move)
        return self.algo.get_next(self.main_board)

    # def pick_next_main_board_coords(self) -> MainBoardCoords:
    #     if self.main_board.sub_board_next_player_must_play is None:
    #         return random.choice(self.main_board.get_playable_coords())
    #     else:
    #         return self.main_board.sub_board_next_player_must_play

    # @staticmethod
    # def pick_random_sub_board_coords(sub_board: SubBoard) -> SubBoardCoords:
    #     return random.choice(sub_board.get_playable_coords())
