# imports
import asyncio
import logging

import d20
import discord
from discord import Interaction
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from Base.Tracker import get_init_list
from Base.Utilities import Utilities
from database_models import get_tracker, get_condition
from error_handling_reporting import error_not_initialized, ErrorReport
from utils.Char_Getter import get_character
from utils.Tracker_Getter import get_tracker_model
from utils.utils import get_guild


# import D4e.d4e_functions


class D4e_Utilities(Utilities):
    def __init__(self, ctx, guild, engine):
        super().__init__(ctx, guild, engine)

    async def add_character(self, bot, name: str, hp: int, player_bool: bool, init: str):
        logging.info("add_character")
        try:
            initiative = 0
            if self.guild.initiative is not None:
                try:
                    roll = d20.roll(init)
                    initiative = roll.total
                except ValueError:
                    await self.ctx.channel.send(f"Invalid Initiative String `{init}`, Please check and try again.")
                    return False
                except Exception:
                    initiative = 0

            D4eModal = D4eAddCharacterModal(
                name=name,
                hp=hp,
                init=init,
                initiative=initiative,
                player=player_bool,
                ctx=self.ctx,
                engine=self.engine,
                bot=bot,
                title=name,
            )
            await self.ctx.send_modal(D4eModal)
            return True

        except NoResultFound:
            await self.ctx.channel.send(error_not_initialized, delete_after=30)
            return False
        except Exception as e:
            logging.warning(f"add_character: {e}")
            report = ErrorReport(self.ctx, "add_character", e, bot)
            await report.report()
            return False


class D4eAddCharacterModal(discord.ui.Modal):
    def __init__(self, name: str, hp: int, init: str, initiative, player, ctx, engine, bot, *args, **kwargs):
        self.name = name
        self.hp = hp
        self.init = init
        self.initiative = initiative
        self.player = player
        self.ctx = ctx
        self.engine = engine
        self.bot = bot
        super().__init__(
            discord.ui.InputText(
                label="AC",
                placeholder="Armor Class",
            ),
            discord.ui.InputText(
                label="Fort",
                placeholder="Fortitude",
            ),
            discord.ui.InputText(
                label="Reflex",
                placeholder="Reflex",
            ),
            discord.ui.InputText(
                label="Will",
                placeholder="Will",
            ),
            *args,
            **kwargs,
        )

    async def callback(self, interaction: discord.Interaction):
        self.stop()
        await interaction.response.send_message(f"{self.name} Created")
        guild = await get_guild(self.ctx, None)
        # Character_Model = await get_character(self.name, self.ctx, guild=guild, engine=self.engine)
        Tracker_Model = await get_tracker_model(self.ctx, self.bot, guild=guild, engine=self.engine)

        embed = discord.Embed(
            title="Character Created (D&D 4e)",
            fields=[
                discord.EmbedField(name="Name: ", value=self.name, inline=True),
                discord.EmbedField(name="HP: ", value=f"{self.hp}", inline=True),
                discord.EmbedField(name="AC: ", value=self.children[0].value, inline=True),
                discord.EmbedField(name="Fort: ", value=self.children[1].value, inline=True),
                discord.EmbedField(name="Reflex: ", value=self.children[2].value, inline=True),
                discord.EmbedField(name="Will: ", value=self.children[3].value, inline=True),
                discord.EmbedField(name="Initiative: ", value=self.init, inline=True),
            ],
            color=discord.Color.dark_gold(),
        )

        async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)
        async with async_session() as session:
            Tracker = await get_tracker(self.ctx, self.engine, id=guild.id)
            async with session.begin():
                tracker = Tracker(
                    name=self.name,
                    init_string=self.init,
                    init=self.initiative,
                    player=self.player,
                    user=self.ctx.user.id,
                    current_hp=self.hp,
                    max_hp=self.hp,
                    temp_hp=0,
                )
                session.add(tracker)
            await session.commit()

        async with async_session() as session:
            result = await session.execute(select(Tracker.id).where(Tracker.name == self.name))
            id = result.scalars().one()
        Condition = await get_condition(self.ctx, self.engine, id=guild.id)

        async with session.begin():
            session.add(
                Condition(
                    character_id=id,
                    title="AC",
                    number=int(self.children[0].value),
                    counter=True,
                    visible=False,
                )
            )
            session.add(
                Condition(
                    character_id=id,
                    title="Fort",
                    number=int(self.children[1].value),
                    counter=True,
                    visible=False,
                )
            )
            session.add(
                Condition(
                    character_id=id,
                    title="Reflex",
                    number=int(self.children[2].value),
                    counter=True,
                    visible=False,
                )
            )
            session.add(
                Condition(
                    character_id=id,
                    title="Will",
                    number=int(self.children[3].value),
                    counter=True,
                    visible=False,
                )
            )
            await session.commit()

        async with session.begin():
            if guild.initiative is not None:
                if not await Tracker_Model.init_integrity_check(guild.initiative, guild.saved_order):
                    # print(f"integrity check was false: init_pos: {guild.initiative}")
                    for pos, row in enumerate(await get_init_list(self.ctx, self.engine)):
                        await asyncio.sleep(0)
                        if row.name == guild.saved_order:
                            guild.initiative = pos
                            # print(f"integrity checked init_pos: {guild.initiative}")
                            await session.commit()
        await Tracker_Model.update()
        await Tracker_Model.update_pinned_tracker()
        # print("Tracker Updated")
        await self.ctx.channel.send(embeds=[embed])

    async def on_error(self, error: Exception, interaction: Interaction) -> None:
        logging.warning(error)
