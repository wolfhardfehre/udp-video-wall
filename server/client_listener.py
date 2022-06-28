from threading import Thread
from typing import List

from commons.logger import logger
from commons.socket_entity import SocketEntity


class ClientListener(Thread):
    def __init__(self, server: SocketEntity, clients: List[str]):
        self._server = server
        self._clients = clients
        super().__init__()

    def run(self) -> None:
        while True:
            message, client_address = self._server.receive()
            logger.info('Client with Address(ip=%s port=%s) is connected!', *client_address)
            self._clients.append(client_address)
