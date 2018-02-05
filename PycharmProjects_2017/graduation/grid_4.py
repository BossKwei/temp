import random
import numpy as np


class GridEnv:
    STRIDE = 3

    def __init__(self):
        self._maze = np.loadtxt('maze_1.csv')
        self._height, self._width = self._maze.shape
        self._wall, self._route = np.max(self._maze), 0
        self._wall_threshold = (self._wall + self._route) / 2
        self._position = None

    def reset(self):
        while True:
            position = (random.randrange(self._width), random.randrange(self._height))
            if self._is_position_valid(position):
                self._position = position
                break

    def step(self, action):
        assert 0 <= action < 4
        # apply action
        action = ((0, -self.STRIDE), (0, self.STRIDE), (-self.STRIDE, 0), (0, self.STRIDE))[action]
        position_ = self._position + action
        done = False if self._is_position_valid(position_) else True
        self._position = position_
        # get reward
        reward = -1.0 if done else 1.0
        #
        return position_, reward, done, None

    def render(self):
        pass

    def sliding_window(self, pt, window_size=(64, 64)):
        x, y = pt
        h_slide, w_slide = window_size
        # expected rect
        top, bottom, left, right = y - h_slide // 2, y + h_slide // 2, x - w_slide // 2, x + w_slide // 2
        # valid rect
        v_top, v_bottom, v_left, v_right = max(top, 0), min(bottom, self._height), max(left, 0), min(right,
                                                                                                     self._width)
        # generate slide window
        sw = np.ones([h_slide, w_slide], dtype=np.uint8) * self._wall
        sw[v_top - top:h_slide - bottom + v_bottom, v_left - left:w_slide - right + v_right] = \
            self._maze[v_top:v_bottom, v_left:v_right]
        return sw, v_top, v_bottom, v_left, v_right

    def _is_position_valid(self, position):
        x, y = position
        if 0 < x < (self._width - 1) and 0 < y < (self._height - 1):
            value = np.sum(self._maze[y - 1:y + 2, x - 1:x + 2]) * 2 / 3  # 6 / 9 of cells
            if value > self._wall_threshold:
                return False
            else:
                return True
        else:
            return False


def main():
    env = GridEnv()
    env.reset()
    for i in range(100):
        state_, reward, done, info = env.step(random.randrange(4))
        env.render()


if __name__ == '__main__':
    main()