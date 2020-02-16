from pathlib import PurePosixPath
from .spoofy import get_spoofy_url_or_none
from gmusicapi import Mobileclient
from os import getenv

async def gpm_url_to_data(url):
    # the ID is the last element in the path, -1 is a special array accessor that returns the last element
    return await GPMData(url.path[-1]).load()

# We call this to re-login on each request because I like excessive guarantees
async def login():
    mm = Mobileclient()
    mm.oauth_login(getenv('GMUSIC_DEVICE_ID'))
    return mm

# These four functions break down the large object we receive from GPM
# down into the few properties we actually need. These return None instead of
# throwing exceptions when calls fail since we're assuming a failed call
# just means that whatever we're looking for isn't that type
#
# Thanks for making me do it this way, Google. Really appreaciate that.
async def get_artist_info(id):
    try:
        result = (await login()).get_artist_info(id, False, 0, 0)
        return {
            'type': 'artist',
            'album': None,
            'artist': result['name'],
            'track': None
        }
    except:
        return None

async def get_album_info(id):
    try:
        result = (await login()).get_album_info(id, False)
        return {
            'type': 'album',
            'album': result['name'],
            'artist': result['artist'],
            'track': None
        }
    except:
        return None

async def get_track_info(id):
    try:
        result = (await login()).get_track_info(id)
        return {
            'type': 'track',
            'album': result['album'],
            'artist': result['artist'],
            'track': result['title']
        }
    except:
        return None

# Since there is no way to tell what kind of GPM object we have from just
# the URL, we just try to get each type until we find one that doesn't fail.
# If we can't do this, assume the user is feeding us bad links and Rickroll accordingly
async def get_info(id):
    result = await get_album_info(id)
    if result is not None:
        return result

    result = await get_track_info(id)
    if result is not None:
        return result

    result = await get_artist_info(id)
    if result is not None:
        return result

    return {
        'type': 'track',
        'album': 'Whenever You Need Somebody',
        'artist': 'Rick Astley',
        'track': 'Never Gonna Give You Up'
    }

# This class has four attributes
# type, which can be one of 'track', 'album', or 'artist'
# album, which, if set, will be the album name
# artist, which, if set, will be the artist name
# track, which, if set, will be the track title
class GPMData:
    # Set our ID during construction, the async load will need this
    def __init__(self, id):
        self.id = id

    async def load(self):
        # Make several GPM calls to figure out what our ID refers to and set our data accordingly
        info = await get_info(self.id)
        self.type = info['type']
        self.album = info['album']
        self.artist = info['artist']
        self.track = info['track']
        return self
