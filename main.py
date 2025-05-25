import discord as disc
from discord.ext import commands
import asyncio
from Commands import Commands




async def main():
    file = open("DiscToken.txt", "r")
    token = file.readline()
    file.close()

    intents = disc.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)
    
    await bot.add_cog(Commands(bot))
    await bot.start(token=token)

if (__name__ == '__main__'):
    asyncio.run(main())