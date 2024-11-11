
import asyncio
from shazamio import Shazam

class ShazamWrapper:
    def __init__(self):
        self.shazam = Shazam()

    def recognize_song(self, file_path):
        async def recognize(file_path):
            return await self.shazam.recognize(file_path)

        return asyncio.run(recognize(file_path))