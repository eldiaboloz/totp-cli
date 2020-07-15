#!/usr/bin/env python
import pyotp
import gnupg
import json
import sys
import os

if len(sys.argv) < 2:
    exit(1)

dir_path = os.path.dirname(os.path.realpath(__file__))
gpg = gnupg.GPG(gnupghome=dir_path + '/.gnupg', verbose=False)
decrypted_data = gpg.decrypt_file(open(dir_path + '/totp_init.json.pgp', 'rb'), passphrase=None)
if not decrypted_data.ok:
    sys.stderr.write('status: ', decrypted_data.status)
    sys.stderr.write('stderr: ', decrypted_data.stderr)
    sys.stderr.write('decrypted string: ', decrypted_data.data)
    exit(1)
config_all = json.loads(decrypted_data.data)
config = config_all[sys.argv[1]];
totp = pyotp.totp.TOTP(config['secret'], digits=config['digits'], interval=config['period'])
sys.stdout.write(totp.now())
