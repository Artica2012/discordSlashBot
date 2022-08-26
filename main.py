# main.py

# imports
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from initialize import connect_test
import database_operations

# environmental variables
load_dotenv(verbose=True)
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
DATABASE = os.getenv("DATABASE")

# set up the bot/intents
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} is connected.")


@bot.slash_command(guild_ids=[GUILD])
async def hello(ctx: discord.ApplicationContext):
    """Say Hello to the Bot"""
    await ctx.respond(f"Hello {ctx.author}!")


@bot.slash_command(name="hi", guild_ids=[GUILD])
async def global_command(ctx: discord.ApplicationContext, num: int):
    await ctx.respond(f'Your number is {num}')


@bot.slash_command(guild_ids=[GUILD])
async def joined(ctx: discord.ApplicationContext, member: discord.Member = None):
    user = member or ctx.author
    await ctx.respond(f"{user.name} joined at {discord.utils.format_dt(user.joined_at)}")


connect_test(DATABASE)

conn = database_operations.create_connection(DATABASE)
# query_data = database_operations.query_database(conn, "feat", "fast")
# print(query_data)
# for row in query_data:
#     print(row)
# query_data = database_operations.whole_database(conn, "feat")
# for row in query_data:
#     print(row)
bot.load_extension("button_roles")
bot.run(TOKEN)
