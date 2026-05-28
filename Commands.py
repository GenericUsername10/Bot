from discord.ext import commands
import requests
import json

# Generates the list of admin users
# This list is hidden
def admins() -> list[str]: 
    file = open("AdminList.txt", "r")
    list = file.read().split("\n")
    file.close()
    return list


# This function updates the dictionary using http requests
# TODO: Change to aiohttp instead of requests later
def courseTuple() -> tuple[dict[str, str], dict[str, list]]:

    courses : dict[str, str] = {}
    section : dict[str, list] = {}
    for i in range(1, 6):
        page = 1
        r = requests.get(f"https://content.osu.edu/v2/classes/search?q=&academic-career=ugrd&client=class-search-ui&sort=&p=1&campus=col&catalog-number={i}xxx")
        jsondata = json.loads(r.text)
        print("Page " + str(page))


        for course in jsondata.get("data").get("courses"):
            courses[f"{course.get("course").get("subject")} {course.get("course").get("catalogNumber")}"] = f"\n{course.get("course").get("title")}\n{course.get("course").get("description")}"
            course.get("sections").insert(0, f"\n{course.get("course").get("title")}\n")
            section[f"{course.get("course").get("subject")} {course.get("course").get("catalogNumber")}"] = course.get("sections")
    
        while(jsondata.get("data").get("nextPageLink") != None):
            page = page + 1
            print("Page " + str(page))
            r = requests.get(f"https://content.osu.edu/v2/classes/search?q=&academic-career=ugrd&client=class-search-ui&sort=&p={page}&campus=col&catalog-number={i}xxx")

            jsondata = json.loads(r.text)
            for course in jsondata.get("data").get("courses"):
                courses[f"{course.get("course").get("subject")} {course.get("course").get("catalogNumber")}"] = f"\n{course.get("course").get("title")}\n{course.get("course").get("description")}"
                course.get("sections").insert(0, f"\n{course.get("course").get("title")}\n")
                section[f"{course.get("course").get("subject")} {course.get("course").get("catalogNumber")}"] = course.get("sections")
                # f"\n{course.get("course").get("title")}\n{course.get("sections")[0]}"
    
    return (courses, section)

# All bot commands are in this class
class Commands(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        self.list : list[str] = admins()
        tuple = courseTuple()
        self.courses = tuple[0]
        self.section = tuple[1]
    
    @commands.command()
    async def test(self, ctx: commands.Context):
        test = await self.bot.is_owner(ctx.author)
        await ctx.send(str(test))

    '''
    async def test(self, ctx: commands.Context):
        atest = await self.bot.is_owner(ctx.author)
        await ctx.send(str(atest))

    tests = commands.Command(test)
    '''
    
    # Only admins can use this command due to the resources it consumes
    @commands.command()
    async def update(self, ctx: commands.Context):
        if (str(ctx.author) not in self.list):
            return
        tuple = courseTuple()
        self.courses = tuple[0]
        self.section = tuple[1]

    @commands.command()
    async def about(self, ctx: commands.Context):
        await ctx.send("A simple bot used give information about courses and other things. Use !cmmds to find out more.")
    
    @commands.command()
    async def classDesc(self, ctx: commands.Context, *args : str):
        courseTitle = args[0].upper() + " " + args[1]
        await ctx.send(f"{courseTitle}{self.courses.get(courseTitle)}")

    @commands.command()
    async def schedule(self, ctx: commands.Context):
        await ctx.send("https://buckeyelink.erp.osu.edu/psp/sps/EMPLOYEE/BUCK/c/PRJCS_MENU.PRJCS_SCHD_STRT.GBL")
    

    @commands.command()
    async def cmmds(self, ctx: commands.Context):
        await ctx.send("1. !classDesc [Course Type (ex. Math)] [Course Number]\n" +
        "Gives a short description of the course with a list of the pre-reqs required.\n"
        + "Ex. Math 1151 gives information regarding Calc 1.\n\n" +
        "2. !cmmds gives a list of the commands"
        "3. !sections to be implemented"
        )

        

    # Only admins can use this command because it shuts the bot off
    @commands.command()
    async def shutdown(self, ctx: commands.Context):
        if (str(ctx.author) not in self.list):
            return
        
        await ctx.send("Termination confirmed. Ending session.")
        exit()
    
    '''
    @commands.command()
    async def sections(self, ctx: commands.Context, *args : str):
        
        courseTitle = args[0].upper() + " " + args[1]
        sections = self.section[courseTitle]
        await ctx.send(sections[0])
        for i in range(1, len(sections)):
            await ctx.send(str(i))
            await ctx.send(sections[i]["term"])
            await ctx.send(sections[i]["meetings"])

        await ctx.send("Done")
'''