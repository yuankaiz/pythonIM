
def Verify(pubkey):
    from Crypto.Signature import PKCS1_v1_5
    from Crypto.Hash import SHA256
    from Crypto.PublicKey import RSA
    from binascii import unhexlify

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('',9998))
    s.listen(1)
    new_s, addr = s.accept()
    s.close()
    mlen = new_s.recv(4, socket.MSG_WAITALL)
    print 'message length:', int(mlen)
    m = new_s.recv(int(mlen), socket.MSG_WAITALL)
    print 'message:', m
    slen = new_s.recv(4, socket.MSG_WAITALL)
    print 'signature length:', int(slen)
    hexsig = new_s.recv(int(slen), socket.MSG_WAITALL)
    print 'signature:', hexsig
    new_s.close()

    key = RSA.importKey(open(pubkey, 'r').read())
    h = SHA256.new(m)
    verifier = PKCS1_v1_5.new(key)
    if verifier.verify(h, unhexlify(hexsig)):
        print 'Verified'
    else:
        print 'Not verified'


def main(args):
    Verify(args.pubkey)

if __name__ == '__main__':
    try:
        import Crypto
    except ImportError:
        print 'Crypto not found, install it by \'pip install pycrypto\''
        exit(1)
    import argparse
    import socket

    parser = argparse.ArgumentParser(description='verifier.py --p pubkey')
    parser.add_argument('--p', dest='pubkey')
    args = parser.parse_args()

    main(args)
