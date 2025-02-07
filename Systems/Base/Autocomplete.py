import logging

import discord
from sqlalchemy import select, false, not_, true
from sqlalchemy.exc import NoResultFound

from Backend.Database.database_models import get_tracker, get_macro, get_condition, Character_Vault
from Backend.utils.Char_Getter import get_character
from Backend.utils.AsyncCache import Cache
from Backend.Database.database_models import async_session


class AutoComplete:
    def __init__(self, ctx: discord.AutocompleteContext, guild):
        self.ctx = ctx
        self.guild = guild

    @Cache.ac_cache
    async def character_query(self, user, gm):
        Tracker = await get_tracker(self.ctx)
        async with async_session() as session:
            if gm and int(self.guild.gm) == self.ctx.interaction.user.id:
                # print("You are the GM")
                char_result = await session.execute(select(Tracker.name).order_by(Tracker.name.asc()))
            elif not gm:
                char_result = await session.execute(select(Tracker.name).order_by(Tracker.name.asc()))
            else:
                # print("Not the GM")
                char_result = await session.execute(
                    select(Tracker.name).where(Tracker.user == user).order_by(Tracker.name.asc())
                )
            return char_result.scalars().all()

    async def character_select(self, **kwargs):
        if "gm" in kwargs:
            gm = kwargs["gm"]
        else:
            gm = False

        if "multi" in kwargs:
            multi = kwargs["multi"]
        else:
            multi = False

        logging.info("character_select")
        try:
            character = await self.character_query(self.ctx.interaction.user.id, gm)

            if self.ctx.value != "":
                val = self.ctx.value.lower()
                if multi and val[-1] == ",":
                    return [f"{val.title()} {option}" for option in character]
                return [option.title() for option in character if val in option.lower()]
            return character

        except NoResultFound:
            return []
        except Exception as e:
            logging.warning(f"epf character_select: {e}")
            return []

    async def get_vault_chars(self, user):
        async with async_session() as session:
            result = await session.execute(
                select(Character_Vault)
                .where(Character_Vault.user == user)
                .where(Character_Vault.system == self.guild.system)
                .where(Character_Vault.guild_id != self.guild.id)
            )
            return result.scalars().all()

    async def vault_search(self, **kwargs):
        # print("vault search")
        output_list = []
        if "gm" in kwargs:
            gm = kwargs["gm"]
        else:
            gm = False

        # vault search
        vault_chars = await self.get_vault_chars(self.ctx.interaction.user.id)

        for item in vault_chars:
            output_list.append(f"{item.name}, {item.guild_id}")

        if gm:
            char_list = await self.character_select(gm=gm)
            output_list.extend(char_list)
        # print("output list:", output_list)

        if self.ctx.value != "":
            val = self.ctx.value.lower()
            return [char for char in output_list if val in char.lower()]
        else:
            return output_list

    async def npc_select(self, **kwargs):
        logging.info("character_select")
        try:
            Tracker = await get_tracker(self.ctx)
            async with async_session() as session:
                char_result = await session.execute(
                    select(Tracker.name).where(Tracker.player == false()).order_by(Tracker.name.asc())
                )
                character = char_result.scalars().all()
            if self.ctx.value != "":
                val = self.ctx.value.lower()
                return [option for option in character if val in option.lower()]
            return character
        except NoResultFound:
            return []
        except Exception as e:
            logging.warning(f"character_select: {e}")

            return []

    async def add_condition_select(self, **kwargs):
        return []

    @Cache.ac_cache
    async def get_macro_list(self, character, attk):
        Tracker = await get_tracker(self.ctx, id=self.guild.id)
        Macro = await get_macro(self.ctx, id=self.guild.id)

        async with async_session() as session:
            char_result = await session.execute(select(Tracker.id).where(Tracker.name == character))
            char = char_result.scalars().one()

        async with async_session() as session:
            if not attk:
                macro_result = await session.execute(
                    select(Macro.name).where(Macro.character_id == char).order_by(Macro.name.asc())
                )
            else:
                macro_result = await session.execute(
                    select(Macro.name)
                    .where(Macro.character_id == char)
                    .where(not_(Macro.macro.contains(",")))
                    .order_by(Macro.name.asc())
                )
            return macro_result.scalars().all()

    async def macro_select(self, **kwargs):
        if "attk" in kwargs:
            attk = kwargs["attk"]
        else:
            attk = False

        character = self.ctx.options["character"]
        char_split = character.split(",")
        if len(char_split) > 1:
            character = char_split[0]

        try:
            macro_list = await self.get_macro_list(character, attk)
            if self.ctx.value != "":
                val = self.ctx.value.lower()
                return [option for option in macro_list if val in option.lower()]
            else:
                return macro_list
        except Exception as e:
            logging.warning(f"a_macro_select: {e}")
            return []

    @Cache.ac_cache
    async def get_conditions(self, character):
        Character_Model = await get_character(character, self.ctx, guild=self.guild)
        Condition = await get_condition(self.ctx, id=self.guild.id)
        async with async_session() as session:
            result = await session.execute(
                select(Condition.title)
                .where(Condition.character_id == Character_Model.id)
                .where(Condition.visible == true())
                .order_by(Condition.title.asc())
            )
            return result.scalars().all()

    async def cc_select(self, **kwargs):
        character = self.ctx.options["character"]

        try:
            condition = await self.get_conditions(character)
            if self.ctx.value != "":
                val = self.ctx.value.lower()
                return [option for option in condition if val in option.lower()]
            else:
                return condition
        except NoResultFound:
            return []
        except Exception as e:
            logging.warning(f"cc_select: {e}")
            return []

    async def save_select(self, **kwargs):
        return []

    @Cache.ac_cache
    async def query_attributes(self, target):
        Tracker = await get_tracker(self.ctx, id=self.guild.id)
        Condition = await get_condition(self.ctx, id=self.guild.id)
        async with async_session() as session:
            result = await session.execute(select(Tracker).where(Tracker.name == target))
            tar_char = result.scalars().one()
        async with async_session() as session:
            result = await session.execute(
                select(Condition.title).where(Condition.character_id == tar_char.id).where(Condition.visible == false())
            )
            return result.scalars().all()

    async def get_attributes(self, **kwargs):
        logging.info("get_attributes")
        try:
            target = self.ctx.options["target"]
            invisible_conditions = await self.query_attributes(target)

            if self.ctx.value != "":
                val = self.ctx.value.lower()
                return [option for option in invisible_conditions if val in option.lower()]
            else:
                return invisible_conditions

        except Exception as e:
            logging.warning(f"get_attributes, {e}")
            return []

    async def attacks(self, **kwargs):
        return ["Not Available for this system"]

    async def stats(self, **kwargs):
        return ["Not Available for this system"]

    async def dmg_types(self, **kwargs):
        return ["Not Available for this system"]

    async def npc_lookup(self, **kwargs):
        return ["Not Available for this system"]

    async def spell_list(self, **kwargs):
        return ["Not Available for this system"]

    async def spell_level(self, **kwargs):
        return ["Not Available for this system"]

    async def init(self, **kwargs):
        return []

    async def flex(self, **kwargs):
        return ["Decrement at beginning of the Turn", "Decrement at end of the Turn"]
