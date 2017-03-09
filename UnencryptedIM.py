
class ChatBase(object):
    def __init__(self, s):
        self.s = s
    def chat(self, s):
        try:
            while True:
                read_list = [s] + [sys.stdin]
                (ready_read, _, _) = select.select(read_list, [], [])
                for sock in ready_read:
                    if sock is s:
                        data = sock.recv(1024)
                        if not data:
                            print 'Bye'
                            exit(1)
                        print data
                    else:
                        m = raw_input()
                        s.send(m)
        except KeyboardInterrupt:
            print 'Bye Bye'
            s.close()
        except EOFError:
            print 'See Ya'
            s.close()
        exit(0)

class Client(ChatBase):
    def run(self, hostname):
        port = 9999
        self.s.connect((hostname, port))
        self.chat(self.s)

class Server(ChatBase):
    def run(self):
        port = 9999
        self.s.bind(('', port))
        self.s.listen(1)
        new_s, addr = self.s.accept()
        self.chat(new_s)

def main(args):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if args.server:
        server = Server(s)
        server.run()
    else:
        client = Client(s)
        client.run(args.hostname)


if __name__ == '__main__':
    import argparse
    import socket
    import select
    import sys

    parser = argparse.ArgumentParser(description='UnencryptedIM.py --s|--c hostname')
    parser.add_argument('--s', dest='server', action='store_true')
    parser.add_argument('--c', dest='hostname')
    args = parser.parse_args()

    main(args)
