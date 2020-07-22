#!/usr/bin/env python
import pyotp
import gnupg
import json
import sys
import os
import subprocess


def getConfig(path=''):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if path == '':
        path = dir_path + '/totp_init.json.pgp'
    gpg = gnupg.GPG(gnupghome=dir_path + '/.gnupg', verbose=False)
    decrypted_data = gpg.decrypt_file(open(path, 'rb'), passphrase=None)
    if not decrypted_data.ok:
        sys.stderr.write('status: ', decrypted_data.status)
        sys.stderr.write('stderr: ', decrypted_data.stderr)
        sys.stderr.write('decrypted string: ', decrypted_data.data)
        exit(1)
    return json.loads(decrypted_data.data)


def paste(totp):
    subprocess.Popen(['xclip', '-in', '-selection', 'clipboard'], stdin=subprocess.PIPE) \
        .communicate(input=totp.encode('ascii'))
    subprocess.run(['xdotool', 'type', totp])
    subprocess.run(['xdotool', 'key', 'Return'])


if len(sys.argv) < 2:
    exit(1)
config_all = getConfig()
config = config_all[sys.argv[1]]
totp = pyotp.totp.TOTP(config['secret'], digits=config['digits'], interval=config['period']).now()
if os.environ["DISPLAY"]:
    paste(totp)
else:
    print(totp)
