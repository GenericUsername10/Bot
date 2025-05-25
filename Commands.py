from discord.ext import commands
import requests
import json


def admins() -> list[str]: 
    file = open("AdminList.txt", "r")
    list = file.read().split("\n")
    file.close()
    return list

def courses() -> dict[str, str]:

    courses : dict[str, str] = {}
    for i in range(1, 6):
        page = 1
        r = requests.get(f"https://content.osu.edu/v2/classes/search?q=&academic-career=ugrd&client=class-search-ui&sort=&p=1&campus=col&catalog-number={i}xxx")
        jsondata = json.loads(r.text)
        print("Page " + str(page))


        for course in jsondata.get("data").get("courses"):
            courses[f"{course.get("course").get("subject")} {course.get("course").get("catalogNumber")}"] = f"\n{course.get("course").get("title")}\n{course.get("course").get("description")}"
    
        while(jsondata.get("data").get("nextPageLink") != None):
            page = page + 1
            print("Page " + str(page))
            r = requests.get(f"https://content.osu.edu/v2/classes/search?q=&academic-career=ugrd&client=class-search-ui&sort=&p={page}&campus=col&catalog-number={i}xxx")

            jsondata = json.loads(r.text)
            for course in jsondata.get("data").get("courses"):
                courses[f"{course.get("course").get("subject")} {course.get("course").get("catalogNumber")}"] = f"\n{course.get("course").get("title")}\n{course.get("course").get("description")}"
    
    return courses

class Commands(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.list : list[str] = admins()
        self.courses = courses()
    
    @commands.command()
    async def test(self, ctx: commands.Context):
        test = await self.bot.is_owner(ctx.author)
        await ctx.send(str(test))

    @commands.command()
    async def update(self, ctx: commands.Context):
        if (str(ctx.author) not in self.list):
            await ctx.send("User not authorized. Refrain from using admin commands.")
            return
        self.courses = courses()
    
    @commands.command()
    async def classDesc(self, ctx: commands.Context, *args : str):
        courseTitle = args[0].upper() + " " + args[1]
        await ctx.send(f"{courseTitle}{self.courses.get(courseTitle)}")

    @commands.command()
    async def schedule(self, ctx: commands.Context):
        await ctx.send("https://buckeyelink.erp.osu.edu/psp/sps/EMPLOYEE/BUCK/c/PRJCS_MENU.PRJCS_SCHD_STRT.GBL")
    

    @commands.command()
    async def cmmds(self, ctx: commands.Context):
        await ctx.send("This is a")

    @commands.command()
    async def shutdown_protocol(self, ctx: commands.Context):
        if (str(ctx.author) not in self.list):
            await ctx.send("User not authorized. Refrain from using admin commands.")
            return
        
        await ctx.send("Termination confirmed. Ending session.")
        exit()
    