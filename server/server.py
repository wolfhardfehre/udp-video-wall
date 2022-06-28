import base64

import cv2
import imutils
import numpy as np

from client_listener import ClientListener
from commons.logger import logger
from commons.socket_entity import SocketEntity


class Server(SocketEntity):
    _TITLE_: str = 'server'
    _WEBCAM_: int = 1

    def __init__(self):
        super().__init__()
        self._clients = []
        self._cache = {}
        self._listener = ClientListener(self, self._clients)
        self._socket.bind((self.host_ip, self._PORT_))

    def start(self) -> None:
        self._listener.start()
        video = cv2.VideoCapture(self._WEBCAM_)
        while video.isOpened():
            message = self._process_video(video=video)
            self._send_to_clients(message=message)
            if self._frames_switch():
                self._frames_on = not self._frames_on
            if self._interrupted():
                self._close_socket()
                video.release()
                break

    def _process_video(self, video: cv2.VideoCapture) -> bytes:
        frame = video.read()[1]
        frame = self._crop_roi(frame=frame)
        frame = imutils.resize(frame, width=600)
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        message = base64.b64encode(buffer)
        logger.debug('message: %s bytes', len(message) * 0.75)
        # self._display(frame=frame)    # uncomment for debugging
        return message

    def _send_to_clients(self, message: bytes) -> None:
        for client_address in self._clients:
            self._socket.sendto(message, client_address)

    def _crop_roi(self, frame: np.ndarray) -> np.ndarray:
        if 'width' not in self._cache:
            self._cache['height'] = frame.shape[1]
            self._cache['width'] = frame.shape[1] // 4 * 3
            self._cache['padding'] = (self._cache['width'] - frame.shape[0]) // 2
        return frame[
           0:self._cache['height'],
           self._cache['padding']:self._cache['width'] + self._cache['padding']
        ]


if __name__ == '__main__':
    try:
        server = Server()
        server.start()
    except KeyboardInterrupt as interrupt:
        logger.info('shutting server down')
