import sys
try:
    import gevent
except ImportError:
    print 'gevent not found, install it by \'pip install gevent\''
    exit(1)
from gevent import socket

class client(object):
    """docstring for client."""
    def __init__(self, config):
        self.config = config
        self.server = None

class server(object):
    """docstring for server."""
    def __init__(self, config):
        self.config = config
        self.clients = []


def get_config():

    return config

def run_server(config):

    return True

def run_client(config):

    return True


def main(args):
    tasks = []
    tasks.append(gevent.spawn(run_server))
    tasks.append(gevent.spawn(run_client))
    gevent.joinall(tasks)
    print args

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: pythonIM.py [ip port] (username)'
    main(sys.argv[1:])
