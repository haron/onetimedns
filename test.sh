#!/bin/bash
set +x

URL="https://onetimedns.net/set?name=test124&secret=F4elBU8OR"

echo Testing API
curl -s $URL
echo

echo Testing resolve
host -t A $(curl -s $URL|python -c 'import sys, json; print json.load(sys.stdin)["record"]')
echo

echo -n "Testing website... "
(($(curl -s https://onetimedns.net/|grep -c OpenWRT) == 3)) && echo OK || echo FAIL
