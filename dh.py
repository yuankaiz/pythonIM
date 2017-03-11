class DH(object):
    def __init__(self, s):
        self.s = s
        self.g = 2
        self.p = 0x00cc81ea8157352a9e9a318aac4e33ffba80fc8da3373fb44895109e4c3ff6cedcc55c02228fccbd551a504feb4346d2aef47053311ceaba95f6c540b967b9409e9f0502e598cfc71327c5a455e2e807bede1e0b7d23fbea054b951ca964eaecae7ba842ba1fc6818c453bf19eb9c5c86e723e69a210d4b72561cab97b3fb3060b
        self.secret = random.randint(1, self.p-1)
        # self.secret = 2
        self.tosend = pow(self.g, self.secret, self.p)
        self.recved = None

    def calc(self):
        if not self.recved:
            print 'have not received anything yet'
            exit(1)
        k = pow(self.recved, self.secret, self.p)
        print k

    def exchange(self):
        self.s.send(str(self.tosend))
        self.recved = int(self.s.recv(1024))

class Client(DH):
    def run(self, hostname):
        port = 9999
        self.s.connect((hostname, port))
        self.exchange()
        self.calc()

class Server(DH):
    def run(self):
        port = 9999
        self.s.bind(('', port))
        self.s.listen(1)
        new_s, addr = self.s.accept()
        self.s = new_s
        self.exchange()
        self.calc()

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
    import random

    parser = argparse.ArgumentParser(description='dh.py --s|--c hostname')
    parser.add_argument('--s', dest='server', action='store_true')
    parser.add_argument('--c', dest='hostname')
    args = parser.parse_args()

    main(args)
