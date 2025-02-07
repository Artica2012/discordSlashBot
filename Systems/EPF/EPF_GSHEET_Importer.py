import logging
from math import floor

import d20
import discord
import numpy
import pandas as pd
from sqlalchemy import select, func

from Backend.Database.engine import async_session, lookup_session
from Systems.EPF.EPF_Automation_Data import EPF_retreive_complex_data
from Systems.EPF.EPF_Character import spell_lookup, EPF_Weapon, delete_intested_items, invest_items, get_EPF_Character
from Backend.Database.database_models import get_EPF_tracker
from Backend.utils.utils import get_guild
from Systems.EPF.EPF_NPC_Importer import write_resitances

Interpreter = {
    "U": 0,
    "T": 2,
    "E": 4,
    "M": 6,
    "L": 8,
    "Str": "str",
    "Dex": "dex",
    "Con": "con",
    "Int": "itl",
    "Wis": "wis",
    "Cha": "cha",
    "None": "",
    "Striking": "striking",
    "Greater Striking": "greaterStriking",
    "Major Striking": "majorStriking",
    "Yes": True,
    "No": False,
    numpy.nan: "",
}


async def epf_g_sheet_import(ctx: discord.ApplicationContext, char_name: str, base_url: str, guild=None, image=None):
    try:
        parsed_url = base_url.split("/")
        # print(parsed_url)
        sheet_id = parsed_url[5]
        logging.warning(f"G-sheet import: ID - {sheet_id}")
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
        df = pd.read_excel(url, header=[0])

        guild = await get_guild(ctx, guild)

        EPF_tracker = await get_EPF_tracker(ctx, id=guild.id)
        async with async_session() as session:
            query = await session.execute(select(EPF_tracker).where(func.lower(EPF_tracker.name) == char_name.lower()))
            character = query.scalars().all()
        if len(character) > 0:
            overwrite = True
        else:
            overwrite = False
        headers = list(df.columns.values)
        # print(headers)
        # print(headers[0])
        # print(df)

        decision_header = headers[0].strip()

        if decision_header == "Info:":
            character, spells, attacks, items, resistance = await epf_g_sheet_character_import(df)
        elif decision_header == "Eidolon:":
            character, spells, attacks, items, resistance = await epf_g_sheet_eidolon_import(ctx, char_name, df, guild)
        elif decision_header == "Companion:":
            character, spells, attacks, items, resistance = await epf_g_sheet_companion_import(df)
        elif decision_header == "NPC:":
            # print("Its an NPC")
            character, spells, attacks, items, resistance = await epf_g_sheet_npc_import(df)
        else:
            return False

        initiative_num = 0
        if not overwrite:
            if guild.initiative is not None:
                # print("In initiative")
                try:
                    perception_mod = character["level"] + character["perception"] + floor((character["wis"] - 10) / 2)
                    roll = d20.roll(f"1d20+{perception_mod}")
                    initiative_num = roll.total
                except Exception:
                    initiative_num = 0

        if "lore" in character:
            # print("lore")
            lore = character["lore"]
            # print(lore)
        else:
            # print("not lore")
            lore = ""

        if overwrite:
            async with async_session() as session:
                query = await session.execute(
                    select(EPF_tracker).where(func.lower(EPF_tracker.name) == char_name.lower())
                )
                character_data = query.scalars().one()

                character_data.max_hp = character["hp"]
                character_data.char_class = character["class"]
                character_data.ac_base = character["ac_base"]
                character_data.level = character["level"]
                character_data.class_dc = character["class_dc"]
                character_data.str = character["str"]
                character_data.dex = character["dex"]
                character_data.con = character["con"]
                character_data.itl = character["itl"]
                character_data.wis = character["wis"]
                character_data.cha = character["cha"]
                character_data.fort_pof = character["fort"]
                character_data.reflex_prof = character["reflex"]
                character_data.will_prof = character["will"]
                character_data.perception_prof = character["perception"]
                character_data.class_prof = character["class_prof"]
                character_data.key_ability = character["key_ability"]
                character_data.unarmored_prof = character["unarmored"]
                character_data.light_armor_prof = character["light"]
                character_data.medium_armor_prof = character["medium"]
                character_data.heavy_armor_prof = character["heavy"]

                character_data.unarmed_prof = character["unarmed"]
                character_data.simple_prof = character["simple"]
                character_data.martial_prof = character["martial"]
                character_data.advanced_prof = character["advanced"]

                character_data.arcane_prof = character["arcane"]
                character_data.divine_prof = character["divine"]
                character_data.occult_prof = character["occult"]
                character_data.primal_prof = character["primal"]

                character_data.acrobatics_prof = character["acrobatics"]
                character_data.arcana_prof = character["arcana"]
                character_data.athletics_prof = character["athletics"]
                character_data.crafting_prof = character["crafting"]
                character_data.deception_prof = character["deception"]
                character_data.diplomacy_prof = character["diplomacy"]
                character_data.intimidation_prof = character["intimidation"]
                character_data.medicine_prof = character["medicine"]
                character_data.nature_prof = character["nature"]
                character_data.occultism_prof = character["occultism"]
                character_data.performance_prof = character["performance"]
                character_data.religion_prof = character["religion"]
                character_data.society_prof = character["society"]
                character_data.stealth_prof = character["stealth"]
                character_data.survival_prof = character["survival"]
                character_data.thievery_prof = character["thievery"]
                character_data.feats = character["feats"]
                character_data.spells = spells
                character_data.attacks = attacks
                character_data.lores = lore
                if image is not None:
                    character.pic = image

                await session.commit()

        else:
            async with async_session() as session:
                async with session.begin():
                    new_char = EPF_tracker(
                        name=char_name,
                        player=True if "npc" not in character.keys() else False,
                        active=character["active"],
                        user=ctx.user.id,
                        current_hp=character["hp"],
                        max_hp=character["hp"],
                        temp_hp=0,
                        char_class=character["class"],
                        level=character["level"],
                        ac_base=character["ac_base"],
                        init=initiative_num,
                        class_prof=character["class_prof"],
                        class_dc=character["class_dc"],
                        str=character["str"],
                        dex=character["dex"],
                        con=character["con"],
                        itl=character["itl"],
                        wis=character["wis"],
                        cha=character["cha"],
                        fort_prof=character["fort"],
                        reflex_prof=character["reflex"],
                        will_prof=character["will"],
                        unarmored_prof=character["unarmored"],
                        light_armor_prof=character["light"],
                        medium_armor_prof=character["medium"],
                        heavy_armor_prof=character["heavy"],
                        unarmed_prof=character["unarmed"],
                        simple_prof=character["simple"],
                        martial_prof=character["martial"],
                        advanced_prof=character["advanced"],
                        arcane_prof=character["arcane"],
                        divine_prof=character["divine"],
                        occult_prof=character["occult"],
                        primal_prof=character["primal"],
                        acrobatics_prof=character["acrobatics"],
                        arcana_prof=character["arcana"],
                        athletics_prof=character["athletics"],
                        crafting_prof=character["crafting"],
                        deception_prof=character["deception"],
                        diplomacy_prof=character["diplomacy"],
                        intimidation_prof=character["intimidation"],
                        medicine_prof=character["medicine"],
                        nature_prof=character["nature"],
                        occultism_prof=character["occultism"],
                        perception_prof=character["perception"],
                        performance_prof=character["performance"],
                        religion_prof=character["religion"],
                        society_prof=character["society"],
                        stealth_prof=character["stealth"],
                        survival_prof=character["survival"],
                        thievery_prof=character["thievery"],
                        lores=lore,
                        feats=character["feats"],
                        key_ability=character["key_ability"],
                        attacks=attacks,
                        spells=spells,
                        resistance=resistance,
                        eidolon=character["eidolon"],
                        partner=character["partner"],
                        pic=image,
                    )
                    session.add(new_char)
                await session.commit()

        # This deletes both items and conditions
        await delete_intested_items(char_name, ctx, guild)
        # Rewrite the items
        # print(f"Items: {items}")
        for item in items:
            # print(item)
            result = await invest_items(item, char_name, ctx, guild)
            # print(result)

        Character = await get_EPF_Character(char_name, ctx, guild)
        # Write the conditions
        await write_resitances(resistance, Character, ctx, guild)
        await Character.update()
        return True

    except Exception:
        logging.warning("epf_g_sheet_import")
        return False


async def epf_g_sheet_character_import(df):
    logging.info("g-sheet-char")
    try:
        df.rename(
            columns={
                "Info:": "a",
                "Info: ": "a",
                "Unnamed: 1": "b",
                "Unnamed: 2": "c",
                "Unnamed: 3": "d",
                "Unnamed: 4": "e",
                "Unnamed: 5": "f",
                "Unnamed: 6": "g",
                "Unnamed: 7": "h",
                "Feats:": "h",
            },
            inplace=True,
        )

    except Exception:
        return False

    for i in range(3, 6):
        "`"

        df.b[i] = int(str(df.b[i]).strip("`"))
        df.d[i] = int(str(df.d[i]).strip("`"))

    # print(df)
    character = {
        "name": df.b[0],
        "level": int(df.d[0]),
        "active": True,
        "class": df.b[1],
        "hp": int(df.d[1]),
        "str": int(df.b[3]),
        "dex": int(df.b[4]),
        "con": int(df.b[5]),
        "itl": int(df.d[3]),
        "wis": int(df.d[4]),
        "cha": int(df.d[5]),
        "class_dc": int(df.b[7]),
        "ac_base": int(df.d[7]),
        "key_ability": Interpreter[df.f[7]],
        "fort": Interpreter[df.b[10]],
        "reflex": Interpreter[df.b[11]],
        "will": Interpreter[df.b[12]],
        "perception": Interpreter[df.b[14]],
        "acrobatics": Interpreter[df.b[16]],
        "arcana": Interpreter[df.b[17]],
        "athletics": Interpreter[df.b[18]],
        "crafting": Interpreter[df.b[19]],
        "deception": Interpreter[df.b[20]],
        "diplomacy": Interpreter[df.b[21]],
        "intimidation": Interpreter[df.b[22]],
        "medicine": Interpreter[df.b[23]],
        "nature": Interpreter[df.b[24]],
        "occultism": Interpreter[df.b[25]],
        "performance": Interpreter[df.b[26]],
        "religion": Interpreter[df.b[27]],
        "society": Interpreter[df.b[28]],
        "stealth": Interpreter[df.b[29]],
        "survival": Interpreter[df.b[30]],
        "thievery": Interpreter[df.b[31]],
        "UI": Interpreter[df.b[33]],
        "unarmored": Interpreter[df.e[10]],
        "light": Interpreter[df.e[11]],
        "medium": Interpreter[df.e[12]],
        "heavy": Interpreter[df.e[13]],
        "unarmed": Interpreter[df.e[16]],
        "simple": Interpreter[df.e[17]],
        "martial": Interpreter[df.e[18]],
        "advanced": Interpreter[df.e[19]],
        "arcane": Interpreter[df.e[22]],
        "divine": Interpreter[df.e[23]],
        "occult": Interpreter[df.e[24]],
        "primal": Interpreter[df.e[25]],
        "eidolon": False,
        "partner": None,
        "lore": "",
    }
    character["class_prof"] = (
        int(character["class_dc"])
        - int(character["level"])
        - (floor(int(character[character["key_ability"]]) - 10) / 2)
        - 10
    )
    # print(character["class_prof"])
    # print(character["class_dc"])
    # print(character["level"])
    # print(character["key_ability"])
    # print(character[character["key_ability"]])
    feats = ""
    feat_list = []
    if character["UI"] == True:
        feats += "Untrained Improvisation, "

    for i in range(0, 34):
        if type(df.h[i]) == str:
            feats += f"{df.h[i]}, "
            feat_list.append(df.h[i].strip())

    character["feats"] = feats
    spells = {}
    attacks = {}
    items = []
    resistances = {"resist": {}, "weak": {}, "immune": {}}

    lore = ""
    for i in range(29, 32):
        # print(df.d[i])
        if type(df.e[i]) == str and type(df.d[i]) == str:
            string = f"{df.d[i]}, {Interpreter[df.e[i]]}; "
            lore += string
    character["lore"] = lore

    for i in range(37, (len(df.a) - 1)):
        try:
            # print(i)
            name = df.a[i]
            # print(name)
            # print(name)
            if type(name) == str:
                tradition = df.c[i]
                match tradition:  # noqa
                    case "Arcane":
                        ability = Interpreter[df.f[22]]
                        proficiency = Interpreter[df.e[22]]
                    case "Divine":
                        ability = Interpreter[df.f[23]]
                        proficiency = Interpreter[df.e[23]]
                    case "Occult":
                        ability = Interpreter[df.f[24]]
                        proficiency = Interpreter[df.e[24]]
                    case "Primal":
                        ability = Interpreter[df.f[25]]
                        proficiency = Interpreter[df.e[25]]
                    case _:
                        ability = "cha"
                        proficiency = 0

                spell_data = await EPF_retreive_complex_data(name)
                if len(spell_data) > 0:
                    for s in spell_data:
                        data = s.data
                        data["ability"] = ability
                        data["trad"] = tradition.lower()
                        spells[s.display_name] = data
                else:
                    lookup_data = await spell_lookup(name)
                    if lookup_data[0] is True:
                        spell = {
                            "level": int(df.b[i]),
                            "tradition": tradition,
                            "ability": ability,
                            "proficiency": proficiency,
                            "type": lookup_data[1].type,
                            "save": lookup_data[1].save,
                            "damage": lookup_data[1].damage,
                            "heightening": lookup_data[1].heightening,
                        }
                        spells[name] = spell
        except Exception:
            pass

    for i in range(36, (len(df.e) - 1)):
        # print(df.e[i])
        if df.e[i] == "Name" and df.f[i] is not numpy.nan:
            # print(df.e[i])
            try:
                # print(df.f[i])
                try:
                    potency = int(df.f[i + 3])
                except Exception:
                    potency = 0
                die_num = 1
                # print(type(df.f[i + 4]))
                # print(df.f[i + 4])
                if Interpreter[df.f[i + 4]] == "striking":
                    die_num = 2
                elif Interpreter[df.f[i + 4]] == "greaterStriking":
                    die_num = 3
                elif Interpreter[df.f[i + 4]] == "majorStriking":
                    die_num = 4
                if df.f[i + 8] is not numpy.nan:
                    parsed_traits = df.f[i + 8].split(",")
                else:
                    parsed_traits = []
                if type(df.f[i + 9]) == str:
                    dmg_type = df.f[i + 9]
                else:
                    dmg_type = "Bludgeoning"

                if type(df.g[i + 9]) == str:
                    mat = str(df.g[i + 9]).lower()
                else:
                    mat = ""

                attack_data = {
                    "display": df.f[i],
                    "name": df.f[i + 1],
                    "prof": df.f[i + 2].lower(),
                    "pot": potency,
                    "str": Interpreter[df.f[i + 4]],
                    "runes": [],
                    "die_num": die_num,
                    "die": df.f[i + 5],
                    "crit": "*2",
                    "stat": Interpreter[df.f[i + 7]],
                    "dmg_type": dmg_type,
                    "attk_stat": Interpreter[df.f[i + 6]],
                    "traits": parsed_traits,
                    "mat": mat,
                }
                edited_attack = await attack_lookup(attack_data, character)

                double_attacks = False
                # Check for two handed and fatal
                for trait in edited_attack["traits"]:
                    # print(trait)
                    if "fatal-aim" in trait:
                        double_attacks = True
                        parsed_trait = trait.split("-")
                        fatal_die = parsed_trait[2]
                        attack_one = edited_attack.copy()
                        attack_two = edited_attack.copy()
                        trait_list = attack_one["traits"]
                        trait_copy = trait_list.copy()
                        for x, trait_item in enumerate(trait_list):
                            if trait_item == trait:
                                trait_copy[x] = f"fatal-{fatal_die}"

                        attack_one["traits"] = trait_copy
                        attack_one["display"] = f"{edited_attack['display']} (2H)"

                        trait_copy = []
                        for trait_id in trait_list:
                            if trait_id != trait:
                                trait_copy.append(i)

                        attack_two["display"] = f"{edited_attack['display']} (1H)"
                        attack_two["traits"] = trait_copy
                    if "two-hand" in trait:
                        double_attacks = True
                        parsed_trait = trait.split("-")
                        attk_2_die = parsed_trait[2]
                        attack_one = edited_attack.copy()
                        attack_two = edited_attack.copy()
                        attack_one["display"] = f"{edited_attack['display']} (2H)"
                        attack_one["die"] = attk_2_die
                        attack_two["display"] = f"{edited_attack['display']} (1H)"

                if double_attacks:
                    attacks[attack_one["display"]] = attack_one
                    attacks[attack_two["display"]] = attack_two
                else:
                    attacks[edited_attack["display"]] = edited_attack

            except Exception:
                pass
    # print(attacks)

    # print("Getting Items")
    for i in range(37, (len(df.h) - 1)):
        # print(i)
        # print(df.h[i])
        if df.h[i] != numpy.nan:
            # print(df.h[i])
            items.append(df.h[i])

    for feat in feat_list:
        feat_data = await EPF_retreive_complex_data(feat)
        for x in feat_data:
            attacks[x.display_name] = x.data

    return character, spells, attacks, items, resistances


async def epf_g_sheet_eidolon_import(ctx: discord.ApplicationContext, char_name: str, df, guild):
    logging.info("g-sheet eidolon")
    try:
        df.rename(
            columns={
                "Eidolon:": "a",
                "Eidolon: ": "a",
                "Unnamed: 1": "b",
                "Unnamed: 2": "c",
                "Unnamed: 3": "d",
                "Unnamed: 4": "e",
                "Unnamed: 5": "f",
                "Unnamed: 6": "g",
                "Unnamed: 7": "h",
            },
            inplace=True,
        )

        # print(df)
    except Exception:
        return False

    guild = await get_guild(ctx, guild)

    try:
        EPF_tracker = await get_EPF_tracker(ctx, id=guild.id)
        # print(df.b[1])
        partner_name: str = df.b[1]
        partner_name = partner_name.strip()
        async with async_session() as session:
            query = await session.execute(
                select(EPF_tracker).where(func.lower(EPF_tracker.name) == partner_name.lower())
            )
            partner_query = query.scalars().one()
            partner_query.partner = char_name
            await session.commit()
        Partner = await get_EPF_Character(partner_name, ctx, guild=guild)
        # print(Partner.char_name)
    except:
        logging.warning("Import Error")
        raise

    for i in range(3, 6):
        "`"

        df.b[i] = int(str(df.d[i]).strip("`"))
        df.d[i] = int(str(df.d[i]).strip("`"))

    character = {
        "name": df.b[0],
        "level": Partner.character_model.level,
        "class": "Eidolon",
        "active": False,
        "hp": Partner.max_hp,
        "str": int(df.b[3]),
        "dex": int(df.b[4]),
        "con": int(df.b[5]),
        "itl": int(df.d[3]),
        "wis": int(df.d[4]),
        "cha": int(df.d[5]),
        "class_dc": Partner.character_model.class_dc,
        "ac_base": int(df.d[7]),
        "key_ability": Partner.character_model.key_ability,
        "fort": Interpreter[df.b[10]],
        "reflex": Interpreter[df.b[11]],
        "will": Interpreter[df.b[12]],
        "perception": Partner.character_model.perception_prof,
        "acrobatics": Partner.character_model.acrobatics_prof,
        "arcana": Partner.character_model.arcana_prof,
        "athletics": Partner.character_model.athletics_prof,
        "crafting": Partner.character_model.crafting_prof,
        "deception": Partner.character_model.deception_prof,
        "diplomacy": Partner.character_model.diplomacy_prof,
        "intimidation": Partner.character_model.intimidation_prof,
        "medicine": Partner.character_model.medicine_prof,
        "nature": Partner.character_model.nature_prof,
        "occultism": Partner.character_model.occultism_prof,
        "performance": Partner.character_model.performance_prof,
        "religion": Partner.character_model.religion_prof,
        "society": Partner.character_model.society_prof,
        "stealth": Partner.character_model.stealth_prof,
        "survival": Partner.character_model.survival_prof,
        "thievery": Partner.character_model.thievery_prof,
        "UI": False,
        "unarmored": Interpreter[df.e[10]],
        "light": 0,
        "medium": 0,
        "heavy": 0,
        "unarmed": Interpreter[df.e[13]],
        "simple": 0,
        "martial": 0,
        "advanced": 0,
        "arcane": Partner.character_model.arcane_prof,
        "divine": Partner.character_model.divine_prof,
        "occult": Partner.character_model.occult_prof,
        "primal": Partner.character_model.primal_prof,
        "feats": "",
        "class_prof": Partner.character_model.class_prof,
        "eidolon": True,
        "partner": Partner.char_name,
    }

    spells = {}
    attacks = {}
    items = []
    resistances = {"resist": {}, "weak": {}, "immune": {}}

    for i in range(18, (len(df.a) - 1)):
        name = df.a[i]
        # print(name)
        if name != numpy.nan:
            lookup_data = await spell_lookup(name)
            if lookup_data[0] is True:
                tradition = df.c[i]
                # print(tradition)
                match tradition:
                    case "Arcane":
                        ability = "cha"
                        proficiency = Partner.character_model.arcane_prof
                    case "Divine":
                        ability = "cha"
                        proficiency = Partner.character_model.divine_prof
                    case "Occult":
                        ability = "cha"
                        proficiency = Partner.character_model.occult_prof
                    case "Primal":
                        ability = "cha"
                        proficiency = Partner.character_model.occult_prof
                    case _:
                        ability = "cha"
                        proficiency = 0

                spell = {
                    "level": int(df.b[i]),
                    "tradition": tradition,
                    "ability": ability,
                    "proficiency": proficiency,
                    "type": lookup_data[1].type,
                    "save": lookup_data[1].save,
                    "damage": lookup_data[1].damage,
                    "heightening": lookup_data[1].heightening,
                }
                spells[name] = spell

    for i in range(17, (len(df.e) - 1)):
        if df.e[i] == "Name" and df.f[i] is not numpy.nan:
            try:
                # print(df.f[i])
                try:
                    potency = int(df.f[i + 3])
                except Exception:
                    potency = 0
                die_num = 1
                # print(type(df.f[i + 4]))
                # print(df.f[i + 4])
                if Interpreter[df.f[i + 4]] == "striking":
                    die_num = 2
                elif Interpreter[df.f[i + 4]] == "greaterStriking":
                    die_num = 3
                elif Interpreter[df.f[i + 4]] == "majorStriking":
                    die_num = 4
                if df.f[i + 8] is not numpy.nan:
                    parsed_traits = df.f[i + 8].split(",")
                else:
                    parsed_traits = []
                # print(df.f[i + 9])
                if type(df.f[i + 9]) == str:
                    dmg_type = df.f[i + 9]
                else:
                    dmg_type = "Bludgeoning"

                attack_data = {
                    "display_name": df.f[i],
                    "name": df.f[i + 1],
                    "prof": df.f[i + 2].lower(),
                    "pot": potency,
                    "str": Interpreter[df.f[i + 4]],
                    "runes": [],
                    "die_num": die_num,
                    "die": df.f[i + 5],
                    "crit": "*2",
                    "stat": Interpreter[df.f[i + 7]],
                    "dmg_type": dmg_type,
                    "attk_stat": Interpreter[df.f[i + 6]],
                    "traits": parsed_traits,
                }
                edited_attack = await attack_lookup(attack_data, character)
                attacks[edited_attack["display_name"]] = edited_attack
            except Exception:
                pass
    # print(attacks)

    # print("Getting Items")
    for i in range(17, (len(df.h) - 1)):
        # print(i)
        # print(df.h[i])
        if df.h[i] != numpy.nan:
            # print(df.h[i])
            items.append(df.h[i])

    return character, spells, attacks, items, resistances


async def attack_lookup(attack, character: dict):
    try:
        async with lookup_session() as session:
            result = await session.execute(
                select(EPF_Weapon).where(func.lower(EPF_Weapon.name) == str(attack["display"]).lower())
            )
            data = result.scalars().one()
    except Exception:
        try:
            async with lookup_session() as session:
                result = await session.execute(
                    select(EPF_Weapon).where(func.lower(EPF_Weapon.name) == str(attack["name"]).lower())
                )
                data = result.scalars().one()
        except:
            return attack

    if data.range is not None:
        attack["stat"] = None

    for item in data.traits:
        if "deadly" in item:
            if "deadly" in item:
                string = item.split("-")
                if data.striking_rune == "greaterStriking":
                    dd = 2
                elif data.striking_rune == "majorStriking":
                    dd = 3
                else:
                    dd = 1
                attack["crit"] = f"*2 + {dd}{string[1]}"
        elif item.strip().lower() == "finesse" and character["dex"] > character["str"]:
            # print("Finesse")
            attack["attk_stat"] = "dex"
        elif item.strip().lower() == "brutal":
            attack["attk_stat"] = "str"
    attack["traits"] = data.traits
    attack["dmg_type"] = data.damage_type
    return attack


async def epf_g_sheet_companion_import(df):
    logging.info("g-sheet-char")
    try:
        df.rename(
            columns={
                "Companion:": "a",
                "Companion: ": "a",
                "Unnamed: 1": "b",
                "Unnamed: 2": "c",
                "Unnamed: 3": "d",
                "Unnamed: 4": "e",
                "Unnamed: 5": "f",
                "Unnamed: 6": "g",
                "Unnamed: 7": "h",
            },
            inplace=True,
        )

        # print(df)
    except Exception:
        return False

    for i in range(3, 6):
        "`"

        df.b[i] = int(str(df.d[i]).strip("`"))
        df.d[i] = int(str(df.d[i]).strip("`"))

    # print(df)
    character = {
        "name": df.b[0],
        "level": int(df.d[0]),
        "active": False,
        "class": df.b[1],
        "hp": int(df.d[1]),
        "str": int(df.b[3]),
        "dex": int(df.b[4]),
        "con": int(df.b[5]),
        "itl": int(df.d[3]),
        "wis": int(df.d[4]),
        "cha": int(df.d[5]),
        "class_dc": int(df.b[7]),
        "ac_base": int(df.d[7]),
        "key_ability": "str",
        "fort": Interpreter[df.b[10]],
        "reflex": Interpreter[df.b[11]],
        "will": Interpreter[df.b[12]],
        "perception": Interpreter[df.b[14]],
        "acrobatics": Interpreter[df.b[16]],
        "arcana": Interpreter[df.b[17]],
        "athletics": Interpreter[df.b[18]],
        "crafting": Interpreter[df.b[19]],
        "deception": Interpreter[df.b[20]],
        "diplomacy": Interpreter[df.b[21]],
        "intimidation": Interpreter[df.b[22]],
        "medicine": Interpreter[df.b[23]],
        "nature": Interpreter[df.b[24]],
        "occultism": Interpreter[df.b[25]],
        "performance": Interpreter[df.b[26]],
        "religion": Interpreter[df.b[27]],
        "society": Interpreter[df.b[28]],
        "stealth": Interpreter[df.b[29]],
        "survival": Interpreter[df.b[30]],
        "thievery": Interpreter[df.b[31]],
        "UI": False,
        "unarmored": Interpreter[df.e[10]],
        "light": 0,
        "medium": 0,
        "heavy": 0,
        "unarmed": Interpreter[df.e[16]],
        "simple": 0,
        "martial": 0,
        "advanced": 0,
        "arcane": 0,
        "divine": 0,
        "occult": 0,
        "primal": 0,
        "eidolon": False,
        "partner": None,
    }

    character["class_prof"] = (
        int(character["class_dc"])
        - int(character["level"])
        - (floor(int(character[character["key_ability"]]) - 10) / 2)
        - 10
    )
    feats = ""
    character["feats"] = feats
    spells = {}
    attacks = {}
    items = []
    resistances = {"resist": {}, "weak": {}, "immune": {}}

    for i in range(34, (len(df.e) - 1)):
        # print(i, df.a[i], df.b[i])
        if df.a[i] == "Name" and df.b[i] is not numpy.nan:
            try:
                # print(df.b[i])
                try:
                    potency = int(df.b[i + 3])
                except Exception:
                    potency = 0
                die_num = 1
                # print(type(df.b[i + 4]))
                # print(df.b[i + 4])
                if Interpreter[df.b[i + 4]] == "striking":
                    die_num = 2
                elif Interpreter[df.b[i + 4]] == "greaterStriking":
                    die_num = 3
                elif Interpreter[df.b[i + 4]] == "majorStriking":
                    die_num = 4
                if df.b[i + 8] is not numpy.nan:
                    parsed_traits = df.b[i + 8].split(",")
                else:
                    parsed_traits = []

                if type(df.b[i + 9]) == str:
                    dmg_type = df.b[i + 9]
                else:
                    dmg_type = "Bludgeoning"

                attack_data = {
                    "display_name": df.b[i],
                    "name": df.b[i + 1],
                    "prof": "" if type(df.b[i + 2]) != str else df.b[i + 2].lower(),
                    "pot": potency,
                    "str": Interpreter[df.b[i + 4]],
                    "runes": [],
                    "die_num": die_num,
                    "die": df.b[i + 5],
                    "crit": "*2",
                    "stat": Interpreter[df.b[i + 7]],
                    "dmg_type": dmg_type,
                    "attk_stat": Interpreter[df.b[i + 6]],
                    "traits": parsed_traits,
                }

                # print(attack_data)
                edited_attack = await attack_lookup(attack_data, character)
                attacks[edited_attack["display_name"]] = edited_attack
                # print(attacks)
            except Exception:
                pass
    # print(attacks)

    # print("Getting Items")
    for i in range(34, (len(df.d) - 1)):
        # print(i)
        # print(df.d[i])
        if df.d[i] != numpy.nan:
            # print(df.d[i])
            items.append(df.d[i])

    return character, spells, attacks, items, resistances


async def epf_g_sheet_npc_import(df):
    logging.info("g-sheet-char")
    try:
        df.rename(
            columns={
                "NPC:": "a",
                "NPC: ": "a",
                "Unnamed: 1": "b",
                "Unnamed: 2": "c",
                "Unnamed: 3": "d",
                "Unnamed: 4": "e",
                "Unnamed: 5": "f",
                "Unnamed: 6": "g",
                "Unnamed: 7": "h",
                "Unnamed: 8": "i",
                "Unnamed: 9": "j",
                "Unnamed: 10": "k",
                "Unnamed: 11": "l",
                "Unnamed: 12": "m",
            },
            inplace=True,
        )

        # print(df)
    except Exception:
        return False

    for i in range(3, 6):
        "`"

        df.b[i] = int(str(df.d[i]).strip("`"))
        df.d[i] = int(str(df.d[i]).strip("`"))

    # Back Calculations
    str_mdd = int(df.b[3])
    str_stat = 10 + (int(df.b[3]) * 2)
    dex_mdd = int(df.b[4])
    dex_stat = 10 + (int(df.b[4]) * 2)
    con_mdd = int(df.b[5])
    con_stat = 10 + (int(df.b[5]) * 2)
    itl_mdd = int(df.d[3])
    itl_stat = 10 + (int(df.d[3]) * 2)
    wis_mdd = int(df.d[4])
    wis_stat = 10 + (int(df.d[4]) * 2)
    cha_mdd = int(df.d[5])
    cha_stat = 10 + (int(df.d[5]) * 2)

    level = int(df.d[0])

    # print(df.b[18])

    character = {
        "name": df.b[0],
        "level": level,
        "active": True,
        "class": df.b[1],
        "npc": True,
        "hp": int(df.d[1]),
        "str": str_stat,
        "dex": dex_stat,
        "con": con_stat,
        "itl": itl_stat,
        "wis": wis_stat,
        "cha": cha_stat,
        "class_dc": 0 if df.b[18] == numpy.nan else int(df.b[18]),
        "ac_base": int(df.b[7]),
        "key_ability": "",
        "fort": int(df.b[10]) - level - con_mdd,
        "reflex": int(df.b[11]) - level - dex_mdd,
        "will": int(df.b[12]) - level - wis_mdd,
        "perception": await gs_npc_skill_calc(df.b[14], level, wis_mdd),
        "acrobatics": await gs_npc_skill_calc(df.e[10], level, dex_mdd),
        "arcana": await gs_npc_skill_calc(df.e[11], level, itl_mdd),
        "athletics": await gs_npc_skill_calc(df.e[12], level, str_mdd),
        "crafting": await gs_npc_skill_calc(df.e[13], level, itl_mdd),
        "deception": await gs_npc_skill_calc(df.e[14], level, cha_mdd),
        "diplomacy": await gs_npc_skill_calc(df.e[15], level, cha_mdd),
        "intimidation": await gs_npc_skill_calc(df.e[16], level, cha_mdd),
        "medicine": await gs_npc_skill_calc(df.e[17], level, wis_mdd),
        "nature": await gs_npc_skill_calc(df.e[18], level, wis_mdd),
        "occultism": await gs_npc_skill_calc(df.e[19], level, itl_mdd),
        "performance": await gs_npc_skill_calc(df.e[20], level, cha_mdd),
        "religion": await gs_npc_skill_calc(df.e[21], level, wis_mdd),
        "society": await gs_npc_skill_calc(df.e[22], level, itl_mdd),
        "stealth": await gs_npc_skill_calc(df.e[23], level, dex_mdd),
        "survival": await gs_npc_skill_calc(df.e[24], level, wis_mdd),
        "thievery": await gs_npc_skill_calc(df.e[25], level, dex_mdd),
        "UI": False,
        "unarmored": 0,
        "light": 0,
        "medium": 0,
        "heavy": 0,
        "unarmed": 0,
        "simple": 0,
        "martial": 0,
        "advanced": 0,
        "arcane": 0,
        "divine": 0,
        "occult": 0,
        "primal": 0,
        "eidolon": False,
        "partner": None,
        "feats": "",
        "class_prof": 0,
    }
    spells = {}
    attacks = {}
    items = []
    resistances = {"resist": {}, "weak": {}, "immune": {}}

    for i in range(31, (len(df.a) - 1)):
        name = df.a[i]
        # print(name)
        if name != numpy.nan:
            lookup_data = await spell_lookup(name)
            if lookup_data[0] is True:
                # print(df.b[17], level, cha_mdd)
                # print(int(df.b[17]) - level - cha_mdd)
                proficiency = int(df.b[17]) - level - cha_mdd
                spell = {
                    "level": int(df.b[i]),
                    "tradition": "NPC",
                    "ability": "cha",
                    "proficiency": proficiency,
                    "dc": int(df.b[18]),
                    "type": lookup_data[1].type,
                    "save": lookup_data[1].save,
                    "damage": lookup_data[1].damage,
                    "heightening": lookup_data[1].heightening,
                }
                spells[name] = spell

    for i in range(30, (len(df.d) - 1)):
        # print(df.d[i], df.e[i])
        if df.d[i] == "Name" and df.e[i] is not numpy.nan:
            try:
                # print(df.e[i])
                try:
                    potency = int(df.e[i + 1])
                except Exception:
                    potency = 0
                die_num = int(df.e[i + 2])
                if df.e[i + 3] is not numpy.nan:
                    parsed_traits = df.e[i + 3].split(",")
                else:
                    parsed_traits = []

                attk_stat = "str"
                crit = "*2"
                dmg_stat = "str"
                # print(df.g[i], type(df.g[i]))
                if type(df.g[i]) == str:
                    dmg_type = df.g[i]
                else:
                    dmg_type = "Bludgeoning"

                if df.f[i] == "Ranged":
                    attk_stat = "dex"
                    dmg_stat = None

                for item in parsed_traits:
                    if "deadly" in item:
                        if "deadly" in item:
                            string = item.split("-")
                            if int(df.e[i + 2]) == 3:
                                dd = 2
                            elif int(df.e[i + 2]) == 4:
                                dd = 3
                            else:
                                dd = 1
                            crit = f"*2 + {dd}{string[1]}"
                    elif item.strip().lower() == "finesse" and dex_mdd > str_mdd:
                        # print("Finesse")
                        attk_stat = "dex"
                    elif item.strip().lower() == "brutal":
                        attk_stat = "str"

                attack_data = {
                    "display_name": df.e[i],
                    "name": df.e[i],
                    "prof": "NPC_C",
                    "pot": potency,
                    "runes": [],
                    "die_num": die_num,
                    "die": df.f[i + 2],
                    "crit": crit,
                    "stat": dmg_stat,
                    "dmg_type": dmg_type,
                    "attk_stat": attk_stat,
                    "traits": parsed_traits,
                    "dmg_bonus": int(df.g[i + 2]),
                }

                attacks[attack_data["display_name"]] = attack_data
            except Exception:
                pass
    # print(attacks)
    # print(len(df.i) - 1)
    for i in range(31, (len(df.i) - 1)):
        # print(i)
        if df.i[i] is not numpy.nan and df.j[i] is not numpy.nan:
            # print(df.i[i], df.j[i])
            resistances["resist"][df.i[i]] = int(df.j[i])

    for i in range(31, (len(df.k) - 1)):
        # print(i)
        if df.k[i] is not numpy.nan and df.l[i] is not numpy.nan:
            # print(df.k[i], df.l[i])
            resistances["weak"][df.k[i]] = int(df.l[i])

    for i in range(31, (len(df.m) - 1)):
        # print(i)
        if df.m[i] is not numpy.nan:
            # print(df.m[i])
            resistances["immune"][df.m[i]] = 1
    # print(resistances)

    return character, spells, attacks, items, resistances


async def gs_npc_skill_calc(skill_mod, level, stat_mod):
    if skill_mod is numpy.nan:
        return 0
    else:
        return int(skill_mod) - level - stat_mod
