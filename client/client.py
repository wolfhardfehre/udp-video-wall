import base64
import os
import sys
from typing import Dict, Tuple

import cv2
import numpy as np
import typer
from vidgear.gears import NetGear

from commons.config import GRID
from commons.logger import logger
from commons.state import State

cli = typer.Typer()


class Client:
    _TITLE_ = 'client'

    def __init__(self, ip: str, screen: int):
        self._ip = ip
        self._screen = screen
        self._cache = {}
        self._frames_on = False
        self._state = State(0, 0, 20, 0)
        options = {"multiclient_mode": True}
        self._client = NetGear(
            address="127.0.0.1",
            port="9999",
            protocol="tcp",
            pattern=2,
            receive_mode=True,
            logging=True,
            **options,
        )

    def start(self) -> None:
        while True:
            cv2.namedWindow(winname=self._TITLE_, flags=cv2.WINDOW_FULLSCREEN)
            cv2.setWindowProperty(
                winname=self._TITLE_,
                prop_id=cv2.WND_PROP_FULLSCREEN,
                prop_value=cv2.WINDOW_FULLSCREEN
            )
            frame = self._client.recv()
            if frame is None:
                break
            cropped = self._cropped_frame(frame)
            self._display(frame=cropped)
            if self._frames_switch():
                self._frames_on = not self._frames_on
            if self._interrupted():
                break
        cv2.destroyAllWindows()
        self._client.close()

    def _display(self, frame: np.ndarray) -> None:
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

    def _cropped_frame(self, frame: np.ndarray) -> np.ndarray:
        return self._crop(frame=frame, screen=self._screen)

    def _crop(self, frame: np.ndarray, screen: int = 0) -> np.ndarray:
        start_x, start_y, end_x, end_y = self.crop_areas(frame)[screen]
        return frame[start_y:end_y, start_x:end_x]

    def crop_areas(self, frame: np.ndarray) -> Dict[int, Tuple[int, int, int, int]]:
        if not self._cache:
            self._cache = {screen: self._crop_area(frame, screen) for screen in range(GRID[0] * GRID[1])}
        return self._cache

    @staticmethod
    def _crop_area(frame: np.ndarray, screen: int) -> Tuple[int, int, int, int]:
        width = frame.shape[1] // GRID[0]
        height = frame.shape[0] // GRID[1]
        position = width * screen
        start_x = position % frame.shape[1]
        start_y = height * (position // frame.shape[1])
        return start_x, start_y, start_x + width, start_y + height


@cli.command()
def start(ip: str, screen: int = 0) -> None:
    try:
        client = Client(ip, screen=screen)
        client.start()
    except KeyboardInterrupt:
        logger.info('shutting client down')
        sys.exit(os.EX_OK)


if __name__ == '__main__':
    cli()
