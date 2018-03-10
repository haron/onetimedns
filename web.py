import hashlib
import redis
from flask import Flask, request, jsonify
from base36 import base36encode, base36decode
from werkzeug.contrib.fixers import ProxyFix
from secret import local_secret
from settings import ZONE_NAME

# SETTINGS
base = '.%s' % ZONE_NAME
expires = 3600 * 24 # seconds to keep record which is not being renewed
request_limit = 20 # no more than {request_limit} requests in {request_ttl} seconds is processed
request_ttl = 120
# SETTINGS DONE

app = Flask(__name__)
app.debug = True
app.wsgi_app = ProxyFix(app.wsgi_app)
debug = app.logger.debug
r = redis.Redis()

def renew(key, ip):
    r.set(key, ip)
    r.expire(key, expires)
    update_limit(ip)
    return {
            'status': 'OK',
            'record': key,
            'value': ip,
            'expires': expires
            }

def record(name, secret):
    val = hashlib.sha224(name + secret + local_secret).hexdigest()
    hashval = base36encode(int(val, 16))
    key = name + '.' + hashval + base
    return key

def limit_exceeded(ip):
    res = r.get(ip)
    if res and int(res) > request_limit:
        return True
    else:
        return False

def update_limit(ip):
    r.incr(ip)
    ttl = r.ttl(ip)
    if ttl < 0:
        r.expire(ip, request_ttl)

def error(message):
    ret = {
            'status': 'FAIL',
            'error_message': message
            }
    return jsonify(ret)

@app.route('/set')
def set():
    ipv4 = request.headers["X-Real-IP"]
    if limit_exceeded(ipv4):
        return error('Request limit exceeded (10 req/min)')

    name = request.args.get('name', None)
    secret = request.args.get('secret', None)
    if not name or not secret:
        return error('Please specify both "name" and "secret" parameters')

    key = record(name, secret)
    keys = r.keys(name + '.*')
    if keys:
        current = keys[0]
        if current == key:
            ret = renew(key, ipv4)
        else:
            return error('Auth failed')
    else:
        ret = renew(key, ipv4)
    return jsonify(ret)

@app.route('/status')
def status():
    key = request.args.get('record', '')
    ret = {
            'record': key,
            'status': 'not found'
            }
    if r.get(key):
        ret['status'] = 'found'
        ret['expires'] = r.ttl(key)
    return jsonify(ret)

def main():
    app.run(host="0.0.0.0")

if __name__ == '__main__':
    main()
