import numpy as np
import itertools
import random


class TicTacToeEnv:

    players = [1, 2]

    def __init__(self, game_array_size):
        self.game_array_size = game_array_size
        self.game_array = np.zeros((game_array_size, game_array_size), dtype=int)
        self.action_space = list(itertools.product(range(0, self.game_array_size), repeat=2))
        self.done = False

        # size of row to win
        self.win = game_array_size

    def reset(self, game_array_size=None):
        if game_array_size:
            self.game_array_size = game_array_size
        self.__init__(self.game_array_size)

    def step(self, action, player_int):
        assert player_int in self.players
        try:
            assert self.game_array[action[0], action[1]] == 0
        except AssertionError:
            reward_val = -10
        else:
            self.game_array[action[0], action[1]] = player_int
            reward_val = -1
        if self.check_win():
            reward_val = 10

        return reward_val

    def check_win(self):
        row = False
        col = False

        # Check rows
        for r in self.game_array:
            if len(set(r)) == 1 and r[0] != 0:
                row = True
        # Checks columns
        for r in self.game_array.transpose():
            if len(set(r)) == 1 and r[0] != 0:
                col = True

        ldiag = len(set(self.game_array.diagonal(0))) == 1 and self.game_array[0, 0] != 0
        rdiag = len(set(np.fliplr(self.game_array).diagonal(0))) == 1 \
                and self.game_array[0, self.game_array_size-1] != 0

        if row or col or ldiag or rdiag:
            return True
        else:
            return False

    def check_draw(self):
        if 0 not in self.game_array:
            return True
        else:
            return False

    def __str__(self):
        return str(self.game_array)


t = TicTacToeEnv(4)
reward = 0
i = 0
pod = False
while reward != 10 and pod is not True:
    if t.check_draw():
        print('Noone wins in {} steps.'.format(i))
        i = 0
        print(t)
        # t.reset()
        break
    for player in [1, 2]:
        x = random.randint(0, t.game_array_size-1)
        y = random.randint(0, t.game_array_size-1)
        reward = t.step((x, y), player)
        i += 1
        if reward == 10:
            print('{} wins in {} steps'.format(player, i))
            print(t)
            pod = True
            break
