import cv2
from vidgear.gears import NetGear

from commons.logger import logger


class Server:
    _TITLE_: str = 'server'
    _WEBCAM_: int = 1

    def __init__(self):
        super().__init__()
        options = {"multiclient_mode": True}
        self._server = NetGear(
            address="127.0.0.1",
            port=(9999,),
            protocol="tcp",
            pattern=2,
            logging=True,
            **options
        )

    def start(self) -> None:
        video = cv2.VideoCapture(self._WEBCAM_)
        data_dict = {}
        while video.isOpened():
            try:
                (grabbed, frame) = video.read()
                if not grabbed:
                    break
                recv_data = self._server.send(frame)

                if not (recv_data is None):
                    unique_address, data = recv_data
                    data_dict[unique_address] = data
            except KeyboardInterrupt:
                break
        logger.info('shutting server down')
        video.release()
        self._server.close()


if __name__ == '__main__':
    server = Server()
    server.start()
