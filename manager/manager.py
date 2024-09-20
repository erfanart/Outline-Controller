import logging,asyncio
from . import vpn
from .bot.key_bot import Bot
from .setting import *
import uuid

class Manager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config_file = CONFIG_FILE
        self.config = CONFIG
        self.bots = CONFIG['bots']
        
    def UuidGen(self):
        Uuid = uuid.uuid4()
        return Uuid


    async def refresher(self):
        while True:
            vpn.update()
            # print(await expired_key())
            await asyncio.sleep(30)



    async def main(self):
        tasks = []
        for bot_name,bot_info in self.bots.items():
            app_bot = Bot()
            locals()[bot_name]= asyncio.create_task(app_bot.makeapp(bot_info["token"],bot_info["url"]))
            tasks.append(locals()[bot_name])
        refresh = asyncio.create_task(self.refresher())
        tasks.append(refresh)
        await asyncio.gather(*tasks)

