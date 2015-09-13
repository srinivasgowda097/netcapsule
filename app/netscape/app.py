#from selenium import webdriver
#from selenium.webdriver.common.proxy import *

from bottle import route, default_app, run, request, response

import requests
import redis
import logging

import time
import sys
import os

PYWB_HOST_PORT = 'memoframe_pywb_1:8080'

REDIS_HOST = 'memoframe_redis_1'

curr_ip = '127.0.0.1'
driver = None

redis_client = redis.StrictRedis(REDIS_HOST)

HOST = os.environ['HOSTNAME']

EXPIRE_TIME = 300


logging.basicConfig(format='%(asctime)s: [%(levelname)s]: %(message)s',
                    level=logging.DEBUG)



def set_timestamp(timestamp):
    params = {'ts': timestamp,
              'ip': curr_ip}

    try:
        r = requests.get('http://set.pywb.proxy/', params=params, proxies={'http': PYWB_HOST_PORT, 'https': PYWB_HOST_PORT})

        if r.status_code == 200:
            return {'success': r.json()}
        else:
            return {'error': r.body}

    except Exception as e:
        return {'error': str(e)}


@route('/set')
def route_set_ts():
    ts = request.query.get('ts')
    res = set_timestamp(ts)

    global driver
    if driver and res.get('success'):
        try:
            driver.refresh()
        except Exception as e:
            logging.debug(e)

    return res

@route(['/ping'])
def ping():
    global redis_client

    if not redis_client.sismember('all_containers', HOST):
        return

    redis_client.expire('c:' + HOST, EXPIRE_TIME)

    global driver

    ts = None
    sec = None
    url = None

    return {'url': url, 'ts': ts, 'sec': sec}



def do_init():
    url = ''
    ts = ''

    if len(sys.argv) > 1:
        global curr_ip
        curr_ip = sys.argv[1]

        if len(sys.argv) > 2:
            url = sys.argv[2]
            if len(sys.argv) > 3:
                ts = sys.argv[3]

    #load_browser(url, ts)
    return default_app()

application = do_init()

@application.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


if __name__ == "__main__":
    run(host='0.0.0.0', port='6082')
