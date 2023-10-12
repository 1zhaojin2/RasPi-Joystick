# move the kinematics command to here
import math
import discord
from discord.ext import commands


class CogFunction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='say', help='Sends a message in the channel')
    @commands.has_any_role(1049861416577945650, 1091342989563019386)
    async def say(self, ctx, *, message):
        # delete the message and send 
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(name='kinematics', help='Solves a kinematics equation. Usage: input 3 variables and the bot will solve for the other 2. E.g. -kinematics vi=5,vf=10,t=2')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kinematics(self, ctx, message):

        # split message into a list
        message = message.split(',')
        # delete the sent message

        vi = None;
        vf = None;
        a = None;
        d = None;
        t = None;


        # find the variables
        # dont forget to handle negative numbers
        # if the number is negative, the message will be like vi=-5
        # so you need to find the index of the equal sign and then convert the string to a float
        for i in range(len(message)):
            if message[i].find('vi=') != -1:
                vi = float(message[i][message[i].find('=')+1:])
            elif message[i].find('vf=') != -1:
                vf = float(message[i][message[i].find('=')+1:])
            elif message[i].find('a=') != -1:
                a = float(message[i][message[i].find('=')+1:])
            elif message[i].find('d=') != -1:
                d = float(message[i][message[i].find('=')+1:])
            elif message[i].find('t=') != -1:
                t = float(message[i][message[i].find('=')+1:])

        # find the missing variable, note that 2 variables can be missing. Only 3 variables are needed to solve for the other 2
        # be careful of which equation to use based on the variables given
        # for example, if vi, vf, and a are given, use equation 5
        # be careful for the case where you need to use the quadratic formula to solve for t
        if vi == None:
            if vf != None and a != None and d != None:
                vi = vf - a * t
            elif vf != None and a != None and t != None:
                vi = vf - a * t
            elif vf != None and d != None and t != None:
                vi = (d - vf * t) / (-0.5 * t**2)
            elif a != None and d != None and t != None:
                vi = (d - 0.5 * a * t**2) / t
        if vf == None:
            if vi != None and a != None and d != None:
                vf = vi + a * t
            elif vi != None and a != None and t != None:
                vf = vi + a * t
            elif vi != None and d != None and t != None:
                vf = (d - vi * t) / (0.5 * t**2)
            elif a != None and d != None and t != None:
                vf = (d + 0.5 * a * t**2) / t
        if a == None:
            if vi != None and vf != None and d != None:
                a = (vf**2 - vi**2) / (2 * d)
            elif vi != None and vf != None and t != None:
                a = (vf - vi) / t
            elif vi != None and d != None and t != None:
                a = (d - vi * t) / (0.5 * t**2)
            elif vf != None and d != None and t != None:
                a = (d - vf * t) / (-0.5 * t**2)
        if d == None:
            if vi != None and vf != None and a != None:
                d = (vf**2 - vi**2) / (2 * a)
            elif vi != None and vf != None and t != None:
                d = (vf + vi) / 2 * t
            elif vi != None and a != None and t != None:
                d = vi * t + 0.5 * a * t**2
            elif vf != None and a != None and t != None:
                d = vf * t - 0.5 * a * t**2
        if t == None:
            if vi != None and vf != None and a != None:
                t = (vf - vi) / a
            elif vi != None and vf != None and d != None:
                t = 2 * d / (vf + vi)
            elif vi != None and a != None and d != None:
                t = (-vi + math.sqrt(vi**2 + 2 * a * d)) / a
            elif vf != None and a != None and d != None:
                t = (vf + math.sqrt(vf**2 - 2 * a * d)) / a
        
        # round to 3 decimal places
        vi = round(vi, 3)
        vf = round(vf, 3)
        a = round(a, 3)
        d = round(d, 3)
        t = round(t, 3)

        # add units
        vi = str(vi) + ' m/s'
        vf = str(vf) + ' m/s'
        a = str(a) + ' m/s^2'
        d = str(d) + ' m'
        t = str(t) + ' s'


        # return the variables as an embed
        embed = discord.Embed(title="Kinematics Solver Alpha v0.1.5", description=f"vi: {vi}\nvf: {vf}\na: {a}\nd: {d}\nt: {t}", color=0xff0000)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CogFunction(bot))