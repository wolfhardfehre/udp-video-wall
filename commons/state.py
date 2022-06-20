import time
from dataclasses import dataclass


@dataclass
class State:
    frames_per_second: int
    current_time: float
    frames_to_count: int
    count: int

    def update(self):
        if self.count == self.frames_to_count:
            now = time.time()
            time_difference = now - self.current_time
            self.frames_per_second = round(self.frames_to_count / time_difference)
            self.current_time = now
            self.count = 0
        self.count += 1
