import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import urlsplit, urlunsplit, quote
from types import SimpleNamespace

# This takes the given gpm_data, uses it to find a Spotify ID
# and then builds a Spotify URL. Spotify's URLs are clear, simple, and easy to understand.
# Unlike SOMEONE'S.
async def get_spoofy_url_or_none(gpm_data):
    spoofy_id = await get_spoofy_id(gpm_data)
    if spoofy_id is not None:
        return urlunsplit([
            'https',
            'open.spotify.com',
            f'/{gpm_data.type}/{spoofy_id}',
            '',
            '',
        ])
    # If we don't find an ID (it's not on Spotify?), Who Can It Be Now?
    return 'https://open.spotify.com/track/5rfJ2Bq2PEL8yBjZLzouEu'

# It looks up the ID based on type. Duh.
async def get_spoofy_id(gpm_data):
    if gpm_data.type == 'album':
        return await get_album_id(gpm_data.album, gpm_data.artist)
    elif gpm_data.type == 'artist':
        return await get_artist_id(gpm_data.artist)
    elif gpm_data.type == 'track':
        return await get_track_id(gpm_data.album, gpm_data.artist, gpm_data.track)
    else:
        return None

# These three functions do essentially the same thing as their GPM counterparts except they just return an ID string,
# or None if the lookup fails
# Note that the search params are quoted. We're assuming, at most, one result for most of these and that the first will be correct.
async def get_album_id(album, artist):
    results = await search(f'album:"{album}" artist:"{artist}"', type='album')
    try:
        return results['albums']['items'][0]['id']
    except:
        return None

async def get_artist_id(artist):
    results = await search(f'artist:"{artist}"', type='artist')
    try:
        return results['artists']['items'][0]['id']
    except:
        return None

async def get_track_id(album, artist, track):
    results = await search(f'album:"{album}" artist:"{artist}" track:"{track}"', type='track')
    try:
        return results['tracks']['items'][0]['id']
    except:
        return None

# This wraps Spotipy's search function and ensures we're refreshing credentials on each request
# Just in case
async def search(q, limit=10, offset=0, type="track", market=None):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    return sp.search(q, limit, offset, type, market)
