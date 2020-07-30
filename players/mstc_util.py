import numpy as np
import random
import time
from copy import deepcopy
from engine.player import Player
from engine.gameplay import MainBoardCoords, SubBoardCoords


# coors to integer hash value
# coors: (main_board_coor, sub_board_coor)
def coor_hash(coors):
    f = lambda x : x.row*3+x.col
    return f(coors[0])*9+f(coors[1])

# integer hash value to coors, (main_board_coor, sub_board_coor)
def hash_to_coors(v):
    f = lambda x: (x//3, x%3)
    return (MainBoardCoords(*f(v//9)), SubBoardCoords(*f(v%9)))

class MSTCAlgo:
    # t_limit: in seconds
    def __init__(self, p, t_limit=0.5):
        self.player = p
        self.root = None
        self.timer_limit = t_limit
    
    def get_next(self, main_board):
        # TODO record root, for future usage
        # TODO move root to match main_board

        if self.root == None:
            self.root = MSNode(main_board, Player.ME, None, 10)
        else:
            print("reuse root")
        # if there is still time remain for this round, we keep selecting to more statistical data
        total_time, count = 0, 0
        while True:
            count += 1
            start = time.time()
            self.root.select()
            total_time += time.time() - start
            if total_time > self.timer_limit:
                break
        print("total time: {}s, # of trial: {}, trial averge time: {:.2f}s".format(total_time, count, total_time / count))
        
        # select the best child and return the move
        best_power, best_move, best_node = -100, None, None
        for move, node in self.root.child.items():
            t_power = node.power(1.414)
            # coor = hash_to_coors(move)
            # print("move:{}, {}, power:{}".format(coor[0], coor[1], t_power), node.win, node.trial)
            if t_power > best_power:
                best_power = t_power
                best_move = move
                best_node = node
        coors = hash_to_coors(best_move)
        # print("choose move:{}, {}, power:{:.2f}, trial averge time: {:.2f}s, win:{}, tie:{}, trial:{}".format(coor[0], coor[1], best_power, total_time / count, best_node.win, best_node.tie, best_node.trial))

        # move root to its child
        self.update_root(coors)
        return coors
    
    def update_root(self, coors):
        if self.root == None: 
            return
        if coors == None:
            self.root = None
            return
        hash_v = coor_hash(coors)
        if hash_v in self.root.child:
            self.root = self.root.child[hash_v]
        else:
            self.root = None

class MSNode:
    def __init__(self, board, p_side, parent=None, limit = 1):
        self.parent = parent
        self.child = {}
        self.win, self.tie, self.trial= 0, 0, 0
        self.main_board = board
        self.side = p_side          # Player.Me, or Player.OPPONENT
        self.expand_limit = limit   # used in select, meaning how many times we could do_child
        # all available for current board state. The value is cached for performance consideration
        self.avail_coors = self.get_available_coors(self.main_board)
    
    def select(self):
        if self.main_board.is_finished:
            win = 0
            if self.main_board.winner == Player.OPPONENT: win = -1
            elif self.main_board.winner == Player.ME: win = 1
            self.backpropagate(win)
            return
        
        # If this node cannot do_child, stop creating child node and call simulaion to get the result
        if self.expand_limit <= 0:
            self.simulate()
            return

        # If expand limit is bigger than the number of children, do each child once    
        # else we select expand_limit number of children randomly
        if self.expand_limit > len(self.avail_coors):
            for coor in self.avail_coors:
                self.do_child(coor)
        else:
            for _ in range(self.expand_limit):
                self.do_child(random.choice(self.avail_coors))

    # Self-simulate the game by randomly choosing move and back-propagate the result
    def simulate(self):
        # copy the board because we will modify it in the following simulation
        board = deepcopy(self.main_board)

        s = self.side
        while not board.is_finished:
            avail_coors = self.get_available_coors(board)
            if s == Player.ME:
                board.add_my_move_inplace(*random.choice(avail_coors))
                s = Player.OPPONENT
            else:
                board.add_opponent_move_inplace(*random.choice(avail_coors))
                s = Player.ME

        win = 0
        if board.winner == Player.OPPONENT: win = -1
        elif board.winner == Player.ME: win = 1
        self.backpropagate(win)

    # return: a list of available coors [(main_board_coor, sub_board_coor), ...]
    def get_available_coors(self, main_board):
        if main_board.sub_board_next_player_must_play:
            avail_main_coors = [main_board.sub_board_next_player_must_play]
        else:
            avail_main_coors = main_board.get_playable_coords()
        
        avail_coors = []
        for main_coor in avail_main_coors:
            sub_board = main_board.get_sub_board(main_coor)
            for coor in sub_board.get_playable_coords():
                avail_coors.append((main_coor, coor))
        return avail_coors

    # do child with coor as coordinate
    def do_child(self, coor):
        # print("\t", coor[0], coor[1], hash(coor))
        
        hash_v = coor_hash(coor)
        # If we already have a node for this coor, call it directly. Otherwise, we create a new MSNode.
        if hash_v not in self.child:
            if self.side == Player.ME:
                new_board = self.main_board.add_my_move(coor[0], coor[1])
                new_side = Player.OPPONENT
            else:
                new_board = self.main_board.add_opponent_move(coor[0], coor[1])
                new_side = Player.ME
            
            self.child[hash_v] = MSNode(new_board, new_side, self, int(self.expand_limit * 0.6)-1)

        self.child[hash_v].select()

    def backpropagate(self, score):
        # print("back prop ", score)
        self.trial += 1
        self.win += max(score, 0)
        if score == 0: self.tie += 1
        if self.parent:
            self.parent.backpropagate(-score) # flip win

    # Evaluate how good a node is. The formula refers to MCTS wiki.
    def power(self, c):
        if self.parent == None:
            t = 0
        else:
            t = c*np.sqrt(np.log(self.parent.trial) / (self.trial+1e-6))
        return self.win/(self.trial+1e-6) + t
    

