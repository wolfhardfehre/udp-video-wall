import socket
from functools import cached_property
from typing import Optional, Tuple, Dict

import cv2
import numpy as np

from commons.config import RESOLUTION, GRID
from commons.logger import logger
from commons.state import State


class SocketEntity:
    _TITLE_: Optional[str] = None
    _PORT_ = 9999
    _BUFF_SIZE_ = 65536   # MacOS users need to: sudo sysctl -w net.inet.udp.maxdgram=65535

    def __init__(self):
        self._frames_on = False
        self._state = State(0, 0, 20, 0)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self._BUFF_SIZE_)
        logger.info('host_name: %s, host_ip: %s, port: %s', self.host_name, self.host_ip, self._PORT_)

    def receive(self) -> Tuple[bytes, str]:
        return self._socket.recvfrom(self._BUFF_SIZE_)

    def _display(self, frame) -> None:
        if self._frames_on:
            frame = self._add_frames_display(frame=frame, state=self._state)
        cv2.imshow(self._TITLE_, frame)
        self._state.update()

    @staticmethod
    def _add_frames_display(frame: np.ndarray, state: State) -> np.ndarray:
        text = f'FPS: {state.frames_per_second}'
        color = (0, 0, 255)
        return cv2.putText(frame, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    @staticmethod
    def _interrupted() -> bool:
        return cv2.waitKey(1) & 0xFF == ord('q')

    @staticmethod
    def _frames_switch() -> bool:
        return cv2.waitKey(1) & 0xFF == ord('f')

    @cached_property
    def host_name(self) -> str:
        return socket.gethostname()

    @cached_property
    def host_ip(self) -> str:
        return socket.gethostbyname(self.host_name)

    def _close_socket(self) -> None:
        logger.info('closing socket')
        self._socket.close()

    def _crop(self, frame: np.ndarray, screen: int = 0) -> np.ndarray:
        start_x, start_y, end_x, end_y = self.crop_areas[screen]
        return frame[start_y:end_y, start_x:end_x]

    @cached_property
    def crop_areas(self) -> Dict[int, Tuple[int, int, int, int]]:
        return {screen: self._crop_area(screen) for screen in range(GRID[0] * GRID[1])}

    @staticmethod
    def _crop_area(screen: int) -> Tuple[int, int, int, int]:
        width = RESOLUTION[0] // GRID[0]
        height = RESOLUTION[1] // GRID[1]
        position = width * screen
        start_x = position % RESOLUTION[0]
        start_y = height * (position // RESOLUTION[0])
        return start_x, start_y, start_x + width, start_y + height
