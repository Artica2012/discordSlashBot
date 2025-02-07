# NPC_importer.py
import asyncio

import d20
import discord
from sqlalchemy import select
from Backend.Database.engine import async_session, lookup_session

from Backend.Database.database_models import (
    get_macro,
    get_condition,
    get_tracker,
    NPC,
)

# define global variables
from Backend.utils.utils import get_guild

# imports


async def npc_lookup(ctx: discord.ApplicationContext, name: str, lookup: str, elite: str, image: str = None):
    async with lookup_session() as session:
        result = await session.execute(select(NPC).where(NPC.name == lookup))
        data = result.scalars().one()

    # Add the character

    # elite/weak adjustments
    hp_mod = 0
    stat_mod = 0
    if elite == "elite":
        if data.level <= 1:
            hp_mod = 10
        elif data.level <= 4:
            hp_mod = 15
        elif data.level <= 19:
            hp_mod = 20
        else:
            hp_mod = 30
        stat_mod = 2
    if elite == "weak":
        if data.level <= 1:
            hp_mod = -10
        elif data.level <= 4:
            hp_mod = -15
        elif data.level <= 19:
            hp_mod = -20
        else:
            hp_mod = -30
        stat_mod = -2

    if elite == "weak":
        init_string = f"{data.init}{stat_mod}"
    else:
        init_string = f"{data.init}+{stat_mod}"

    try:
        guild = await get_guild(ctx, None)
        initiative_num = 0
        if guild.initiative is not None:
            try:
                initiative_num = int(data.init) + stat_mod

            except Exception:
                try:
                    roll = d20.roll(init_string)
                    initiative_num = roll.total
                except Exception:
                    initiative_num = 0

        async with async_session() as session:
            Tracker = await get_tracker(ctx, id=guild.id)
            async with session.begin():
                tracker = Tracker(
                    name=name,
                    init_string=init_string,
                    init=initiative_num,
                    player=False,
                    user=ctx.user.id,
                    current_hp=data.hp + hp_mod,
                    max_hp=data.hp + hp_mod,
                    temp_hp=0,
                    pic=image,
                )
                session.add(tracker)
            await session.commit()

        Condition = await get_condition(ctx, id=guild.id)
        async with async_session() as session:
            char_result = await session.execute(select(Tracker).where(Tracker.name == name))
            character = char_result.scalars().one()

        async with session.begin():
            session.add(
                Condition(
                    character_id=character.id,
                    title="AC",
                    number=data.ac + stat_mod,
                    counter=True,
                    visible=False,
                )
            )
            session.add(
                Condition(
                    character_id=character.id,
                    title="Fort",
                    number=data.fort + stat_mod,
                    counter=True,
                    visible=False,
                )
            )
            session.add(
                Condition(
                    character_id=character.id,
                    title="Reflex",
                    number=data.reflex + stat_mod,
                    counter=True,
                    visible=False,
                )
            )
            session.add(
                Condition(
                    character_id=character.id,
                    title="Will",
                    number=data.will + stat_mod,
                    counter=True,
                    visible=False,
                )
            )
            session.add(
                Condition(
                    character_id=character.id,
                    title="DC",
                    number=data.dc + stat_mod,
                    counter=True,
                    visible=False,
                )
            )
            await session.commit()

        # Parse Macros
        attack_list = data.macros.split("::")
        Macro = await get_macro(ctx, id=guild.id)
        async with session.begin():
            for x, attack in enumerate(attack_list[:-1]):
                await asyncio.sleep(0)
                # split the attack
                # print(attack)
                split_string = attack.split(";")
                # print(split_string)
                base_name = split_string[0].strip()
                attack_string = split_string[1].strip()
                damage_string = split_string[2].strip()
                if elite == "weak":
                    attack_macro = Macro(
                        character_id=character.id,
                        name=f"{x + 1}. {base_name} - Attack",
                        macro=f"{attack_string}{stat_mod}",
                    )
                else:
                    attack_macro = Macro(
                        character_id=character.id,
                        name=f"{x + 1}. {base_name} - Attack",
                        macro=f"{attack_string}+{stat_mod}",
                    )
                session.add(attack_macro)
                # print("Attack Added")
                if elite == "weak":
                    damage_macro = Macro(
                        character_id=character.id,
                        name=f"{x + 1}. {base_name} - Damage",
                        macro=f"{damage_string}{stat_mod}",
                    )
                else:
                    damage_macro = Macro(
                        character_id=character.id,
                        name=f"{x + 1}. {base_name} - Damage",
                        macro=f"{damage_string}+{stat_mod}",
                    )

                session.add(damage_macro)
                # print("Damage Added")
            await session.commit()
        # print("Committed")

    except Exception:
        await ctx.send_followup("Action Failed, please try again", delete_after=60)

    # print(ctx.message.id)
    return True
