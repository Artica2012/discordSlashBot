# initiative.py
# Initiative Tracker Module

# imports
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from sqlalchemy import insert
import database_models
import database_operations
import sqlite3
import sqlalchemy as db
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from database_models import Global, ConditionTable, TrackerTable, Base
from sqlalchemy.orm import Session, Query
from sqlalchemy import select, update, delete, insert

from dice_roller import DiceRoller

import os
from dotenv import load_dotenv

# define global variables
role_ids = [1011880400513151058, 1011880477298278461, 1011880538199556176]
load_dotenv(verbose=True)
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
SERVER_DATA = os.getenv('SERVERDATA')


# Functions

# Tables - These will allow a central place for changes, also saves a ton of lines of code

# The tracker table
def tracker_table(server: discord.Guild, metadata):
    tablename = f"Tracker_{server.id}"
    emp = db.Table(tablename, metadata,
                   db.Column('id', db.INTEGER(), autoincrement=True, primary_key=True),
                   db.Column('name', db.String(255), nullable=False, unique=True),
                   db.Column('init', db.INTEGER(), default=0),
                   db.Column('player', db.BOOLEAN, default=False),
                   db.Column('user', db.INTEGER(), nullable=False),
                   db.Column('current_hp', db.INTEGER(), default=0),
                   db.Column('max_hp', db.INTEGER(), default=1),
                   db.Column('temp_hp', db.INTEGER(), default=0),
                   )
    return emp


# The condition table
def condition_table(server: discord.Guild, metadata):
    tablename = f"Condition_{server.id}"
    con = db.Table(tablename, metadata,
                   db.Column('id', db.INTEGER(), autoincrement=True, primary_key=True),
                   db.Column('character_id', db.INTEGER(), ForeignKey(f'Tracker_{server.id}.id')),
                   db.Column('condition', db.String(255), nullable=False),
                   db.Column('duration', db.INTEGER()),
                   db.Column('beginning', db.BOOLEAN, default=False)
                   )
    return con


# Set up the tracker if it does not exit.db
def setup_tracker(server: discord.Guild):
    try:
        engine = create_engine(f'sqlite:///{SERVER_DATA}.db', future=True)
        # engine = create_engine('postgresql://')
        conn = engine.connect()
        metadata = db.MetaData()
        emp = tracker_table(server, metadata)
        con = condition_table(server, metadata)
        metadata.create_all(engine)
        Base.metadata.create_all(engine)

        with Session(engine) as session:
            guild = Global(
                guild_id=server.id,
                time=0,
            )
            session.add(guild)
            session.commit()

        return True
    except Exception as e:
        print(e)
        return False


# Add a player to the database
def add_player(name: str, user: int, server: discord.Guild, HP: int):
    engine = create_engine(f'sqlite:///{SERVER_DATA}.db', future=True)
    tablename = f'Tracker_{server.id}'
    metadata = db.MetaData()
    try:
        emp = tracker_table(server, metadata)
        stmt = emp.insert().values(
            name=name,
            init=0,
            player=True,
            user=user,
            current_hp=HP,
            max_hp=HP,
            temp_hp=0
        )
        compiled = stmt.compile()
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


# Add an NPC to the database
def add_npc(name: str, user: int, server: discord.Guild, HP: int):
    engine = create_engine(f'sqlite:///{SERVER_DATA}.db', future=True)
    tablename = f'Tracker_{server.id}'
    metadata = db.MetaData()
    try:
        emp = tracker_table(server, metadata)
        stmt = emp.insert().values(
            name=name,
            init=0,
            player=False,
            user=user,
            current_hp=HP,
            max_hp=HP,
            temp_hp=0
        )
        compiled = stmt.compile()
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def set_init(server: discord.Guild, name: str, init: int):
    engine = create_engine(f'sqlite:///{SERVER_DATA}.db', future=True)
    metadata = db.MetaData()
    try:
        emp = tracker_table(server, metadata)
        stmt = update(emp).where(emp.c.name == name).values(
            init=init
        )
        compiled = stmt.compile()
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return True
    except Exception as e:
        print(e)
        return False


def advance_initiative(server: discord.Guild):
    engine = create_engine(f'sqlite:///{SERVER_DATA}.db', future=True)
    with Session(engine) as session:
        guild = session.execute(select(Global).filter_by(guild_id=server.id)).scalar_one()
        init_pos = int(guild.initiative)
        init_pos += 1
        if init_pos >= len(get_init_list(server)):
            init_pos = 0
        guild.initiative = init_pos
        session.commit()
    display_string = display_init(get_init_list(server), init_pos)
    return display_string


def get_init_list(server: discord.Guild):
    engine = create_engine(f'sqlite:///{SERVER_DATA}.db', future=True)
    metadata = db.MetaData()
    emp = tracker_table(server, metadata)
    stmt = emp.select().order_by(emp.c.init.desc())
    # print(stmt)
    data = []
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(row)
            data.append(row)
        print(data)
        return data


def display_init(init_list: list, selected: int):
    row_data = []
    for row in init_list:
        row_data.append({'id': row[0],
                         'name': row[1],
                         'init': row[2],
                         'player': row[3],
                         'user': row[4],
                         'chp': row[5],
                         'maxhp': row[6],
                         'thp': row[7]
                         })

    output_string = "```" \
                    "Initiative:\n"
    for x, row in enumerate(row_data):
        if x == selected:
            selector = '>>>'
        else:
            selector = ''
        if row['player']:
            if row['thp'] != 0:
                string = f"{selector} {row['init']} {str(row['name']).title()}: {row['chp']}/{row['maxhp']} ({row['thp']}) Temp\n"
            else:
                string = f"{selector}  {row['init']} {str(row['name']).title()}: {row['chp']}/{row['maxhp']}\n"
        else:
            hp_string = calculate_hp(row['chp'], row['maxhp'])
            string = f"{selector}  {row['init']} {str(row['name']).title()}: {hp_string} \n"
        output_string += string
    output_string += '```'
    print(output_string)
    return output_string


def calculate_hp(chp, maxhp):
    hp_string = ''
    hp = chp / maxhp
    if hp == 1:
        hp_string = 'Uninjured'
    elif hp >= .5:
        hp_string = 'Injured'
    elif hp >= .1:
        hp_string = 'Bloodied'
    else:
        hp_string = 'Critical'

    return hp_string


# The Initiative Cog
class InitiativeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    initiative = SlashCommandGroup("initiative", "Initiative Tracker")

    @initiative.command(guild_ids=[GUILD])
    async def setup(self, ctx: discord.ApplicationContext):
        response = setup_tracker(ctx.guild)
        if response:
            await ctx.respond("Server Setup", ephemeral=True)
        else:
            await ctx.respond("Server Failed", ephemeral=True)

    @initiative.command(guild_ids=[GUILD])
    async def add_character(self, ctx: discord.ApplicationContext, name: str, hp: int):
        response = add_player(name, ctx.user.id, ctx.guild, hp)
        if response:
            await ctx.respond(f"Character {name} added successfully", ephemeral=True)
        else:
            await ctx.respond(f"Error Adding Character", ephemeral=True)

    @initiative.command(guild_ids=[GUILD])
    async def add_npc(self, ctx: discord.ApplicationContext, name: str, hp: int):
        response = add_npc(name, ctx.user.id, ctx.guild, hp)
        if response:
            await ctx.respond(f"Character {name} added successfully", ephemeral=True)
        else:
            await ctx.respond(f"Error Adding Character", ephemeral=True)

    @initiative.command(guild_ids=[GUILD])
    async def start_initiative(self, ctx: discord.ApplicationContext):
        engine = create_engine(f'sqlite:///{SERVER_DATA}.db', future=True)
        init_list = get_init_list(ctx.guild)

        with Session(engine) as session:
            guild = session.execute(select(Global).filter_by(guild_id=ctx.guild_id)).scalar_one()
            guild.initiative = 0
            session.commit()
        display_string = display_init(init_list, 0)
        await ctx.respond(display_string)

    @initiative.command(guild_ids=[GUILD])
    async def next(self, ctx: discord.ApplicationContext):
        display_string = advance_initiative(ctx.guild)
        await ctx.respond(display_string)

    @initiative.command(guild_ids=[GUILD])
    async def init(self, ctx: discord.ApplicationContext, character: str, init: str):
        dice = DiceRoller('')
        try:
            initiative = int(init)
            success = set_init(ctx.guild, character, initiative)
            if success:
                await ctx.respond(f"Iniative: {initiative}")
            else:
                await ctx.respond("Failed to set initiative.", ephemeral=True)
        except:
            roll = dice.plain_roll(init)
            success = set_init(ctx.guild, character, roll[1])
            if success:
                await ctx.respond(f"Iniative: {roll[0]} = {roll[1]}")
            else:
                await ctx.respond("Failed to set initiative.", ephemeral=True)

def setup(bot):
    bot.add_cog(InitiativeCog(bot))
