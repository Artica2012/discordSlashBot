# attack_cog.py

import os

# imports
import discord
import asyncio
import sqlalchemy as db
from discord import option
from discord.commands import SlashCommandGroup, option
from discord.ext import commands, tasks
from dotenv import load_dotenv
from sqlalchemy import or_
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, selectinload, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

import dice_roller
from database_models import Global, Base, TrackerTable, ConditionTable, MacroTable, get_tracker_table, \
    get_condition_table, get_macro_table
from database_operations import get_asyncio_db_engine
from dice_roller import DiceRoller
from error_handling_reporting import ErrorReport, error_not_initialized
from time_keeping_functions import output_datetime, check_timekeeper, advance_time, get_time
from PF2e.pathbuilder_importer import pathbuilder_import
import PF2e.pf2_functions

# define global variables

load_dotenv(verbose=True)
if os.environ['PRODUCTION'] == 'True':
    TOKEN = os.getenv('TOKEN')
    USERNAME = os.getenv('Username')
    PASSWORD = os.getenv('Password')
    HOSTNAME = os.getenv('Hostname')
    PORT = os.getenv('PGPort')
else:
    TOKEN = os.getenv('BETA_TOKEN')
    USERNAME = os.getenv('BETA_Username')
    PASSWORD = os.getenv('BETA_Password')
    HOSTNAME = os.getenv('BETA_Hostname')
    PORT = os.getenv('BETA_PGPort')

GUILD = os.getenv('GUILD')
SERVER_DATA = os.getenv('SERVERDATA')
DATABASE = os.getenv('DATABASE')


# ---------------------------------------------------------------
# ---------------------------------------------------------------
# UTILITY FUNCTIONS

# Checks to see if the user of the slash command is the GM, returns a boolean
async def gm_check(ctx, engine):
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        result = await session.execute(select(Global).where(
            or_(
                Global.tracker_channel == ctx.interaction.channel_id,
                Global.gm_tracker_channel == ctx.interaction.channel_id
            )
        )
        )
        guild = result.scalars().one()
        if int(guild.gm) != int(ctx.interaction.user.id):
            return False
        else:
            return True


class AttackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.engine = get_asyncio_db_engine(user=USERNAME, password=PASSWORD, host=HOSTNAME, port=PORT, db=SERVER_DATA)
        self.async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

        # ---------------------------------------------------
        # ---------------------------------------------------
        # Autocomplete Methods

        # Autocomplete to give the full character list

    async def character_select(self, ctx: discord.AutocompleteContext):
        metadata = db.MetaData()
        character_list = []

        try:
            emp = await get_tracker_table(ctx, metadata, self.engine)
            stmt = emp.select()
            async with self.engine.begin() as conn:
                data = []
                for row in await conn.execute(stmt):
                    data.append(row)
                    print(row)
            for row in data:
                # if row[4] == ctx.interaction.user.id or gm_status:
                character_list.append(row[1])
            print(character_list)
            await self.engine.dispose()
            return character_list
        except Exception as e:
            print(f'character_select: {e}')
            report = ErrorReport(ctx, self.character_select.__name__, e, self.bot)
            await report.report()
            return False

        # Autocomplete to return the list of character the user owns, or all if the user is the GM

    async def character_select_gm(self, ctx: discord.AutocompleteContext):
        metadata = db.MetaData()
        character_list = []

        print('checking gm')
        gm_status = await gm_check(ctx, self.engine)
        print(f"GM:  {gm_status}")

        try:
            emp = await get_tracker_table(ctx, metadata, self.engine)
            stmt = emp.select()
            async with self.engine.begin() as conn:
                data = []
                for row in await conn.execute(stmt):
                    data.append(row)
                    print(row)
            for row in data:
                if row[4] == ctx.interaction.user.id or gm_status:
                    character_list.append(row[1])
            print(character_list)
            await self.engine.dispose()
            return character_list

        except Exception as e:
            print(f'character_select_gm: {e}')
            report = ErrorReport(ctx, self.character_select.__name__, e, self.bot)
            await report.report()
            return False

    async def a_macro_select(self, ctx: discord.AutocompleteContext):
        metadata = db.MetaData()
        character = ctx.options['character']
        macro = await get_macro_table(ctx, metadata, self.engine)
        emp = await get_tracker_table(ctx, metadata, self.engine)

        try:
            char_stmt = emp.select().where(emp.c.name == character)
            print(character)
            async with self.engine.begin() as conn:
                data = []
                macro_list = []
                for char_row in await conn.execute(char_stmt):
                    data.append(char_row)
                for row in data:
                    print(row)
                    macro_stmt = macro.select().where(macro.c.character_id == row[0])
                    for char_row in await conn.execute(macro_stmt):
                        if not ',' in  char_row[3]:
                            macro_list.append(f"{char_row[2]}: {char_row[3]}")
            await self.engine.dispose()
            return macro_list
        except Exception as e:
            print(f'a_macro_select: {e}')
            report = ErrorReport(ctx, self.a_macro_select.__name__, e, self.bot)
            await report.report()
            return False

    # ---------------------------------------------------
    # ---------------------------------------------------
    # Slash commands

    att = SlashCommandGroup("a", "Automatic Attack Commands")

    @att.command(description="Automatic Attack")
    @option('character', description='Character Attacking', autocomplete=character_select_gm)
    @option('target', description="Character to Target", autocomplete=character_select)
    @option('roll', description="Roll or Macro Roll", autocomplete=a_macro_select)
    @option('vs', description="Target Attribute",
            autocomplete=discord.utils.basic_autocomplete(PF2e.pf2_functions.PF2_attributes))
    @option('attack_modifier', description="Modifier to the macro (defaults to +)", required=False)
    @option('target_modifier', description="Modifier to the target's dc (defaults to +)", required=False)
    async def attack(self, ctx: discord.ApplicationContext, character: str, target: str, roll: str, vs: str, attack_modifier:str ='', target_modifier:str=''):
        metadata = db.MetaData()
        await ctx.response.defer()
        async with self.async_session() as session:
            result = await session.execute(select(Global).where(
                or_(
                    Global.tracker_channel == ctx.interaction.channel_id,
                    Global.gm_tracker_channel == ctx.interaction.channel_id
                )
            )
            )
            guild = result.scalars().one()
            if not guild.system:
                await ctx.respond("No system set, command inactive.")
                return

            if guild.system == 'PF2':
                # PF2 specific code
                output_string = await PF2e.pf2_functions.attack(ctx, self.engine, self.bot, character, target, roll, vs, attack_modifier, target_modifier)
            else:
                output_string = 'Error'
            await ctx.send_followup(output_string)

    @att.command(description="Saving Throw")
    @option('character', description='Saving Character', autocomplete=character_select_gm)
    @option('target', description="Character to use DC", autocomplete=character_select)
    @option('roll', description="Roll or Macro Roll", autocomplete=a_macro_select)
    @option('vs', description="Target Attribute",
            autocomplete=discord.utils.basic_autocomplete(PF2e.pf2_functions.PF2_attributes))
    @option('modifier', description="Modifier to the macro (defaults to +)", required=False)

    async def save(self, ctx: discord.ApplicationContext, character: str, target: str, vs: str, modifier:str=''):
        metadata = db.MetaData()
        await ctx.response.defer()
        async with self.async_session() as session:
            result = await session.execute(select(Global).where(
                or_(
                    Global.tracker_channel == ctx.interaction.channel_id,
                    Global.gm_tracker_channel == ctx.interaction.channel_id
                )
            )
            )
            guild = result.scalars().one()
            if not guild.system:
                await ctx.respond("No system set, command inactive.")
                return
            # PF2 specific code
            if guild.system == 'PF2':
                output_string = await PF2e.pf2_functions.save(ctx, self.engine, self.bot, character, target, vs, modifier)
                await ctx.send_followup(output_string)



def setup(bot):
    bot.add_cog(AttackCog(bot))
