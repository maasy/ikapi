import sys
import time
import uuid
import json
import asyncio

from fastapi import APIRouter
import requests

from models import User_Pydantic, UserIn_Pydantic, Battle_Pydantic
from models import Users

tags = ["battles"]
router = APIRouter()

@router.get("/battle/{user_id}", tags=tags)
async def battle_update(user_id: int):
    user = await Users.get_or_none(id=user_id)
    cookie = user.cookie
    session_token = user.session_token
    if not user:
        pass
    url = "https://app.splatoon2.nintendo.net/api/results"
    app_unique_id = "80377059283410564865"
    app_user_agent = 'Mozilla/5.0 (Linux; Android 7.1.2; Pixel Build/NJH47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36'
    app_timezone_offset = str(int((time.mktime(time.gmtime()) - time.mktime(time.localtime()))/60))
    app_head = {
        'Host': 'app.splatoon2.nintendo.net',
        'x-unique-id': app_unique_id,
        'x-requested-with': 'XMLHttpRequest',
        'x-timezone-offset': app_timezone_offset,
        'User-Agent': app_user_agent,
        'Accept': '*/*',
        'Referer': 'https://app.splatoon2.nintendo.net/home',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ja-JP'
    }

    results_list = requests.get(url, headers=app_head, cookies=dict(iksm_session=cookie))
    if 'code' in json.loads(results_list.text):
        cookie = await gen_new_cookie(user, session_token)
        results_list = requests.get(url, headers=app_head, cookies=dict(iksm_session=cookie))

    return json.loads(results_list.text)

async def gen_new_cookie(user, session_token):
    timestamp = int(time.time())
    guid = str(uuid.uuid4())

    app_head = {
        'Host':            'accounts.nintendo.com',
        'Accept-Encoding': 'gzip',
        'Content-Type':    'application/json; charset=utf-8',
        'Accept-Language': 'ja-JP',
        'Content-Length':  '439',
        'Accept':          'application/json',
        'Connection':      'Keep-Alive',
        'User-Agent':      'OnlineLounge/1.6.1.2 NASDKAPI Android'
    }

    body = {
        'client_id':     '71b963c1b7b6d119', # Splatoon 2 service
        'session_token': session_token,
        'grant_type':    'urn:ietf:params:oauth:grant-type:jwt-bearer-session-token'
    }

    url = "https://accounts.nintendo.com/connect/1.0.0/api/token"

    r = requests.post(url, headers=app_head, json=body)
    id_response = json.loads(r.text)

    # get user info
    try:
        app_head = {
            'User-Agent':      'OnlineLounge/1.6.1.2 NASDKAPI Android',
            'Accept-Language': 'ja-JP',
            'Accept':          'application/json',
            'Authorization':   'Bearer {}'.format(id_response["access_token"]),
            'Host':            'api.accounts.nintendo.com',
            'Connection':      'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
    except:
        print("Not a valid authorization request. Please delete config.txt and try again.")
        print("Error from Nintendo (in api/token step):")
        print(json.dumps(id_response, indent=2))
        sys.exit(1)
    url = "https://api.accounts.nintendo.com/2.0.0/users/me"

    r = requests.get(url, headers=app_head)
    user_info = json.loads(r.text)

    nickname = user_info["nickname"]

    # get access token
    app_head = {
        'Host':             'api-lp1.znc.srv.nintendo.net',
        'Accept-Language':  'ja-JP',
        'User-Agent':       'com.nintendo.znca/1.6.1.2 (Android/7.1.2)',
        'Accept':           'application/json',
        'X-ProductVersion': '1.6.1.2',
        'Content-Type':     'application/json; charset=utf-8',
        'Connection':       'Keep-Alive',
        'Authorization':    'Bearer',
        # 'Content-Length':   '1036',
        'X-Platform':       'Android',
        'Accept-Encoding':  'gzip'
    }

    body = {}
    try:
        idToken = id_response["access_token"]

        flapg_nso = call_flapg_api(idToken, guid, timestamp, "nso")

        parameter = {
            'f':          flapg_nso["f"],
            'naIdToken':  flapg_nso["p1"],
            'timestamp':  flapg_nso["p2"],
            'requestId':  flapg_nso["p3"],
            'naCountry':  user_info["country"],
            'naBirthday': user_info["birthday"],
            'language':   user_info["language"]
        }
    except SystemExit:
        sys.exit(1)
    except:
        print("Error(s) from Nintendo:")
        print(json.dumps(id_response, indent=2))
        print(json.dumps(user_info, indent=2))
        sys.exit(1)
    body["parameter"] = parameter

    url = "https://api-lp1.znc.srv.nintendo.net/v1/Account/Login"

    r = requests.post(url, headers=app_head, json=body)
    splatoon_token = json.loads(r.text)

    try:
        idToken = splatoon_token["result"]["webApiServerCredential"]["accessToken"]
        flapg_app = call_flapg_api(idToken, guid, timestamp, "app")
    except:
        print("Error from Nintendo (in Account/Login step):")
        print(json.dumps(splatoon_token, indent=2))
        sys.exit(1)

    # get splatoon access token
    try:
        app_head = {
            'Host':             'api-lp1.znc.srv.nintendo.net',
            'User-Agent':       'com.nintendo.znca/1.6.1.2 (Android/7.1.2)',
            'Accept':           'application/json',
            'X-ProductVersion': '1.6.1.2',
            'Content-Type':     'application/json; charset=utf-8',
            'Connection':       'Keep-Alive',
            'Authorization':    'Bearer {}'.format(splatoon_token["result"]["webApiServerCredential"]["accessToken"]),
            'Content-Length':   '37',
            'X-Platform':       'Android',
            'Accept-Encoding':  'gzip'
        }
    except:
        print("Error from Nintendo (in Account/Login step):")
        print(json.dumps(splatoon_token, indent=2))
        sys.exit(1)

    body = {}
    parameter = {
        'id':                5741031244955648,
        'f':                 flapg_app["f"],
        'registrationToken': flapg_app["p1"],
        'timestamp':         flapg_app["p2"],
        'requestId':         flapg_app["p3"]
    }
    body["parameter"] = parameter

    url = "https://api-lp1.znc.srv.nintendo.net/v2/Game/GetWebServiceToken"

    r = requests.post(url, headers=app_head, json=body)
    splatoon_access_token = json.loads(r.text)

    # get cookie
    try:
        app_head = {
            'Host':                    'app.splatoon2.nintendo.net',
            'X-IsAppAnalyticsOptedIn': 'false',
            'Accept':                  'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':         'gzip,deflate',
            'X-GameWebToken':          splatoon_access_token["result"]["accessToken"],
            'Accept-Language':         'ja-JP',
            'X-IsAnalyticsOptedIn':    'false',
            'Connection':              'keep-alive',
            'DNT':                     '0',
            'User-Agent':              'Mozilla/5.0 (Linux; Android 7.1.2; Pixel Build/NJH47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
            'X-Requested-With':        'com.nintendo.znca'
        }
    except:
        print("Error from Nintendo (in Game/GetWebServiceToken step):")
        print(json.dumps(splatoon_access_token, indent=2))
        sys.exit(1)

    url = "https://app.splatoon2.nintendo.net/?lang={}".format('ja-JP')
    r = requests.get(url, headers=app_head)

    cookie = r.cookies["iksm_session"]
    user.cookie = cookie
    await user.save()

    return cookie

def call_flapg_api(id_token, guid, timestamp, type):
    '''Passes in headers to the flapg API (Android emulator) and fetches the response.'''

    try:
        api_app_head = {
            'x-token': id_token,
            'x-time':  str(timestamp),
            'x-guid':  guid,
            'x-hash':  get_hash_from_s2s_api(id_token, timestamp),
            'x-ver':   '3',
            'x-iid':   type
        }
        api_response = requests.get("https://flapg.com/ika2/api/login?public", headers=api_app_head)
        f = json.loads(api_response.text)["result"]
        return f
    except:
        try: # if api_response never gets set
            if api_response.text:
                print(u"Error from the flapg API:\n{}".format(json.dumps(json.loads(api_response.text), indent=2, ensure_ascii=False)))
            elif api_response.status_code == requests.codes.not_found:
                print("Error from the flapg API: Error 404 (offline or incorrect headers).")
            else:
                print("Error from the flapg API: Error {}.".format(api_response.status_code))
        except:
            pass
        sys.exit(1)

def get_hash_from_s2s_api(id_token, timestamp):
    '''Passes an id_token and timestamp to the s2s API and fetches the resultant hash from the response.'''

    # check to make sure we're allowed to contact the API. stop spamming my web server pls

    try:
        version = '1.5.4'
        api_app_head = { 'User-Agent': "splatnet2statink/{}".format(version) }
        api_body = { 'naIdToken': id_token, 'timestamp': timestamp }
        api_response = requests.post("https://elifessler.com/s2s/api/gen2", headers=api_app_head, data=api_body)
        return json.loads(api_response.text)["hash"]
    except:
        print("Error from the splatnet2statink API:\n{}".format(json.dumps(json.loads(api_response.text), indent=2)))
