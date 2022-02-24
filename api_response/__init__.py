from os import getcwd

from api_response.realtime import grab_notes

from api_response.utils import set_cookie

if getcwd().endswith('api_response'):
    set_cookie(getcwd() + '\\cookie.txt')
else:
    set_cookie(getcwd() + '\\api_response\\cookie.txt')