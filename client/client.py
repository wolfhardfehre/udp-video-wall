import base64

import cv2
import numpy as np
import typer

from commons.logger import logger
from commons.socket_entity import SocketEntity

cli = typer.Typer()


class Client(SocketEntity):
    _TITLE_ = 'client'

    def __init__(self, ip: str, screen: int):
        self._ip = ip
        self._screen = screen
        super().__init__()

    def start(self) -> None:
        self._socket.sendto(b'connect', (self._ip, self._PORT_))
        while True:
            cv2.namedWindow(winname=self._TITLE_, flags=cv2.WINDOW_FULLSCREEN)
            cv2.setWindowProperty(
                winname=self._TITLE_,
                prop_id=cv2.WND_PROP_FULLSCREEN,
                prop_value=cv2.WINDOW_FULLSCREEN
            )
            self._display(frame=self._cropped_frame)
            if self._frames_switch():
                self._frames_on = not self._frames_on
            if self._interrupted():
                self._close_socket()
                break

    @property
    def _cropped_frame(self) -> np.ndarray:
        return self._crop(frame=self._frame, screen=self._screen)

    @property
    def _frame(self) -> np.ndarray:
        return cv2.imdecode(self._to_array(), 1)

    def _to_array(self) -> np.ndarray:
        return np.frombuffer(self._decode(), dtype=np.uint8)

    def _decode(self) -> bytes:
        return base64.b64decode(self.receive()[0], b' /')


@cli.command()
def start(ip: str, screen: int = 0) -> None:
    try:
        client = Client(ip, screen=screen)
        client.start()
    except KeyboardInterrupt:
        logger.info('shutting client down')


if __name__ == '__main__':
    cli()
