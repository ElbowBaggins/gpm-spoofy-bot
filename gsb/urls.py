from urllib.parse import urlsplit, urlunsplit, unquote, parse_qs
from pathlib import PurePosixPath
from types import SimpleNamespace

from .gpm import gpm_url_to_data
from .spoofy import get_spoofy_url_or_none

# For a given list of URLs, each URL is converted into an object containing data about the item the URL refers to.
# This is then used to query Spotify and produce either a Spotify album, artist, or track URL
async def remap_urls(urls):
    result = [await get_spoofy_url_or_none(await gpm_url_to_data(url)) for url in urls]
    if (len(result) == 0):
        return None
    return result

# All Google Play Music URLs start with
# https://play.google.com/music
def validate_url(url):
    if url is not None:
        if url.hostname == 'play.google.com':
            if (len(url.path) > 0):
                if (url.path[0] == 'music'):
                    return True
    return False

# Splits all found URLs into their component parts, retaining only GPM URLs
def split_urls(urls):
    return list(filter(lambda split_url: validate_url(split_url), map(lambda url: complete_urlsplit(url), urls)))

# Returns an array of path segments, or an empty array for an empty path
def split_path(path):
    result = PurePosixPath(unquote(path)).parts
    if len(result) > 0:
        return list(result[1:])
    else:
        return []

# Works like urlsplit but also splits the path into its parts
# such that '/path/to/here' because an array of strings of the form ['path', 'to', 'here']
# this is helpful for reading the ID out of the GPM URLs
# This version also returns None instead of throwing an exception.
# For our usage, this causes it to return None when encountering non-URL content or a malformed URL
# and this causes it to get filtered out later, which is what we want
def complete_urlsplit(url):
    try:
        result = urlsplit(url)
        return SimpleNamespace(**{
            'scheme': result.scheme,
            'netloc': result.netloc,
            'path': split_path(result.path),
            'query': parse_qs(result.query),
            'fragment': result.fragment,
            'username': result.username,
            'password': result.password,
            'hostname': result.hostname,
            'port': result.port
        })
    except:
        return None



