def pn(n):
    return '0' * (4 - len(str(n))) + str(n)

def GenerateKey():
    from Crypto.PublicKey import RSA

    k = RSA.generate(1024)
    fpriv = open('myprivkey.pem', 'w')
    fpriv.write(k.exportKey('PEM'))
    fpriv.close()
    fpub = open('mypubkey.pem', 'w')
    fpub.write(k.publickey().exportKey('PEM'))
    fpub.close()
    print 'keypair generated'

def Sign(args):
    from Crypto.Signature import PKCS1_v1_5
    from Crypto.Hash import SHA256
    from Crypto.PublicKey import RSA
    from binascii import hexlify

    k = RSA.importKey(open('myprivkey.pem', 'r').read())
    h = SHA256.new(args.message)
    signer = PKCS1_v1_5.new(k)
    signature = signer.sign(h)
    hexsig = hexlify(signature)
    # print hexsig
    tosend = pn(len(args.message)) + args.message + pn(len(hexsig)) + hexsig
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((args.hostname, 9998))
    s.send(tosend)
    s.close()
    # print tosend

def main(args):
    if args.genkey:
        GenerateKey()
    else:
        Sign(args)

if __name__ == '__main__':
    try:
        import Crypto
    except ImportError:
        print 'Crypto not found, install it by \'pip install pycrypto\''
        exit(1)
    import argparse
    import socket

    parser = argparse.ArgumentParser(description='signer.py --genkey|--c hostname --m message')
    parser.add_argument('--genkey', dest='genkey', action='store_true')
    parser.add_argument('--c', dest='hostname')
    parser.add_argument('--m', dest='message')
    args = parser.parse_args()

    main(args)
