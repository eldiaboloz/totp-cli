#!/usr/bin/env bash
set -euf -o pipefail

myp="$(dirname $(realpath "$0"))"
export GNUPGHOME="${myp}/.gnupg"
name=${1-}
if [ -z "$name" ]; then
  if [ ! -t 0 ]; then
    echo "name is empty!" 1>&2
    exit 1
  fi
  name=$(cat "${myp}/totp_names.txt" | fzf)
fi
totp="$(
  oathtool --totp=sha1 \
    $(
      cat "${myp}/"totp_init.json.pgp |
        gpg -d |
        jq -r ".\"$name\""'|"-d \(.digits) -s \(.period) -b \(.secret)"' |
        tr -d '\n'
    )
)"
[ -n "$DISPLAY" ] &&
  (
    xdotool type "$totp"
    xdotool key Return
  ) ||
  echo "$totp"
