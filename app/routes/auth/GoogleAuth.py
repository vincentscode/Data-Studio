import config
from app import app

import flask
import functools

from authlib.integrations.requests_client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

base_url = '/auth/'

ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

AUTHORIZATION_SCOPE = ' '.join([
    # basic information
    'openid', 'email', 'profile',

    # fitness api
    'https://www.googleapis.com/auth/fitness.location.read', 'https://www.googleapis.com/auth/fitness.activity.read',

    # tasks
    'https://www.googleapis.com/auth/tasks.readonly',

])

BASE_URI = "http://localhost:5000"
AUTH_REDIRECT_URI = BASE_URI + "/auth/google"

AUTH_TOKEN_KEY = 'google_auth_token'
AUTH_STATE_KEY = 'google_auth_state'


def no_cache(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = flask.make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return functools.update_wrapper(no_cache_impl, view)


def is_logged_in():
    return True if AUTH_TOKEN_KEY in flask.session else False


def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')

    oauth2_tokens = flask.session[AUTH_TOKEN_KEY]

    return google.oauth2.credentials.Credentials(
        oauth2_tokens['access_token'],
        refresh_token=oauth2_tokens['refresh_token'],
        client_id=config.GOOGLE_CLIENT_ID,
        client_secret=config.GOOGLE_CLIENT_SECRET,
        token_uri=ACCESS_TOKEN_URI)


def get_user_info():
    credentials = build_credentials()
    oauth2_client = googleapiclient.discovery.build('oauth2', 'v2', credentials=credentials)
    return oauth2_client.userinfo().get().execute()


@app.route(base_url + 'google/login')
@no_cache
def login(auth_scope=AUTHORIZATION_SCOPE):
    session = OAuth2Session(config.GOOGLE_CLIENT_ID, config.GOOGLE_CLIENT_SECRET, scope=auth_scope, redirect_uri=AUTH_REDIRECT_URI)
    uri, state = session.create_authorization_url(AUTHORIZATION_URL)

    print("[Login] state:", state)

    flask.session[AUTH_STATE_KEY] = state
    flask.session.permanent = True

    return flask.redirect(uri, code=302)


@app.route(base_url + 'google')
@no_cache
def google_auth_redirect():
    req_state = flask.request.args.get('state', default=None, type=None)
    print("[Redirect] state:", req_state)

    if req_state != flask.session[AUTH_STATE_KEY]:
        response = flask.make_response('Invalid state parameter', 401)
        return response

    session = OAuth2Session(config.GOOGLE_CLIENT_ID, config.GOOGLE_CLIENT_SECRET,
                            scope=AUTHORIZATION_SCOPE,
                            state=flask.session[AUTH_STATE_KEY],
                            redirect_uri=AUTH_REDIRECT_URI)

    oauth2_tokens = session.fetch_access_token(ACCESS_TOKEN_URI, authorization_response=flask.request.url)

    flask.session[AUTH_TOKEN_KEY] = oauth2_tokens
    print("[Redirect] user_info:", get_user_info())
    return flask.redirect(BASE_URI, code=302)


@app.route(base_url + 'google/logout')
@no_cache
def logout():
    flask.session.pop(AUTH_TOKEN_KEY, None)
    flask.session.pop(AUTH_STATE_KEY, None)

    return flask.redirect(BASE_URI, code=302)
