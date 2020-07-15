#!/usr/bin/env bash
set -euf -o pipefail

[ "$#" -ge 1 ] && name="$1" || name=""

if [ -n "$name" ]; then
  coproc "$(dirname "$(realpath "$0")")/totp.py" "$name" "yes" >/dev/null 2>&1
  exec 1>&-
  exit
fi

cat "$(dirname "$(realpath "$0")")/totp_names.txt"

# vim:sw=2:ts=2:et:
