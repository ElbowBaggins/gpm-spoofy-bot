from discord import Client
from os import getenv
from .urls import remap_urls, split_urls

class GsbClient(Client):
    TOKEN = None

    async def on_ready(self):
        print('Logged on as: ', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        # get a list of all message fragments that were GPM URLs
        possible_urls = split_urls(message.content.split())
        # only start showing the typing indicator if we have URLs to look up
        # so we're not pointlessly making noise
        if len(possible_urls) > 0:
            # Holds the typing indicator open until this with block exits
            async with message.channel.typing():
                # remap_urls returns a new list where every GPM URL in possible_urls is replaced
                # with a Spotify URL to the same content, or the 'error' content.
                new_urls = await remap_urls(possible_urls)

                # if we really got a list back AND it has items, send each item to the channel
                # otherwise respond with the error content
                if new_urls is not None:
                    if len(new_urls) > 0:
                        for i in new_urls:
                            await message.channel.send(i)
                    else:
                        await message.channel.send('https://open.spotify.com/track/5rfJ2Bq2PEL8yBjZLzouEu')

    def run(self):
        return Client.run(self, GsbClient.TOKEN)


