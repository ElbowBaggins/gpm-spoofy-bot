### gpm-spoofy-bot
A Discord bot for converting Google Play Music links to Spoofy links, in Python. For some reason.

Today I tried Python.
I didn't like it.

To make this thing work you need these environment variables set
`SPOTIPY_CLIENT_ID`
`SPOTIPY_CLIENT_SECRET`
`GMUSIC_DEVICE_ID`
`DISCORD_BOT_TOKEN`

You will probably need to `pip install gmusicapi` and run its `Mobileclient.perform_oauth()` routine before running this
or the GPM integrations will fail.

Why are you setting up your own instance of this anyway?
