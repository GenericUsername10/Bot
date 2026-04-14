import discord as disc
from discord.ext import commands
import asyncio
from Commands import Commands



# Main
async def main():
    # The bot token is hidden
    # WARNING: Do not change following three lines of code
    file = open("DiscToken.txt", "r")
    token = file.readline()
    file.close()

    intents = disc.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)
    
    await bot.add_cog(Commands(bot))

    @bot.event
    async def on_guild_join(guild):
        if guild.system_channel:
            await guild.system_channel.send("Please use !about or !cmmds to learn more.")


    await bot.start(token=token)

if (__name__ == '__main__'):
    asyncio.run(main())