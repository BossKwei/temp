import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self, a, b):
        # a, b = self.get_argument('a'), self.get_argument('b')
        # c = int(a) + int(b)
        self.write('{0} {1}'.format(a, b))

    def data_received(self, chunk):
        raise NotImplementedError


def make_app():
    return tornado.web.Application([
        (r"/a=([^/]+)&b=([^/]+)", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
