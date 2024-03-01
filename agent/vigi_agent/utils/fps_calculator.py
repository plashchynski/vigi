# This file is used to calculate the FPS of the system to ensure that the video
# metadata is accurate. The FPS is calculated by measuring the time it takes to
# process a frame and then averaging the time over a number of frames.

from collections import deque
import time

class FPSCalculator():
    def __init__(self, max_history_size=100, min_history_size=20):
        """
        the max_history_size is the number of frames to keep in the history used to calculate the FPS,
        the higher the number, the more accurate the FPS will be, but it will also be slower to react to changes
        """
        self.min_history_size = min_history_size
        self.time_history = deque(maxlen=max_history_size)
        self.old_time = time.time()

    def update(self):
        """
        Tic the FPS calculator, this should be called once per frame
        """
        new_time = time.time()
        self.time_history.append(new_time - self.old_time)
        self.old_time = new_time

    def current_fps(self) -> int:
        """
        Returns the current FPS of the system
        """
        if len(self.time_history) < self.min_history_size:
            return None

        return int(1 / (sum(self.time_history) / len(self.time_history)))
