import os

from api_response.realtime import grab_notes

from api_response.utils import set_cookie

cookie_path = os.path.dirname(os.path.abspath(__file__)) + r'\cookie.txt'

set_cookie(cookie_path)
