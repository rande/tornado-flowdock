import socket
import tornado.iostream
import ssl

class HttpStreamProtocol(object):
    def __init__(self, host, url, port=443, headers=None, logger=None, use_ssl=True, on_message=None):
        self.host = host
        self.port = port
        self.url = url
        self.headers = headers
        self.logger = logger
        self.use_ssl = use_ssl
        self.on_message = on_message

        self.stream = None

    def start(self):
        if self.stream:
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

        if self.use_ssl:
            ssl.wrap_socket(sock, do_handshake_on_connect=True)
            self.stream = tornado.iostream.SSLIOStream(sock)
        else:
            self.stream = tornado.iostream.IOStream(sock)

        self.stream.set_close_callback(self._on_close)
        self.stream.connect((self.host, self.port), self._send_request)

    def _send_request(self):
        self.stream.write(b"GET %s HTTP/1.1\r\n" % self.url)
        self.stream.write(b"Host: %s\r\n" % self.host)

        for name, value in self.headers.iteritems():
            self.stream.write(b"%s: %s\r\n" % (name, value))

        self.stream.write(b"\r\n")

        self.stream.read_until(b"\r\n\r\n", self._read_headers)

    def _read_headers(self, headers):
        if self.logger:
            self.logger.debug("HttpStreamProtocol.read_headers: %s", headers)

        self._start_chunk()

    def _start_chunk(self):
        if self.logger:
            self.logger.debug("HttpStreamProtocol.start_chunk ~ start reading")

        self.stream.read_until(b"\r\n", self._read_chunk_length)

    def _read_chunk_length(self, data):
        if self.logger:
            self.logger.debug("HttpStreamProtocol.read_chunk_length: %s" % data)

        try:
            length = int(data, 16)
        except ValueError:
            length = False

        if length:
            self.stream.read_bytes(length, self._read_chunk_message)
        else:
            self._start_chunk()

    def _read_chunk_message(self, message):
        if self.logger:
            self.logger.debug("HttpStreamProtocol.read_chunk_message: %s" % message)

        if self.on_message:
            self.on_message(message)

        self._start_chunk()

    def _on_close(self, *args, **kwargs):
        if self.logger:
            self.logger.debug("HttpStreamProtocol.on_close: args: %s, kwargs: %s" % (args, kwargs))

    def close(self):
        self.stream.close()
