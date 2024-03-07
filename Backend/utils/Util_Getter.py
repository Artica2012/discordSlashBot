import logging

from Systems.Base.Utilities import Utilities
from Systems.D4e.D4e_Utilities import D4e_Utilities
from Systems.PF2e.PF2_utilities import PF2_Utilities
from Systems.EPF.EPF_Utilities import EPF_Utilities
from Systems.STF.STF_Utilities import STF_Utilities
from Backend.Database.database_operations import USERNAME, PASSWORD, HOSTNAME, PORT, SERVER_DATA
from Backend.Database.database_operations import get_asyncio_db_engine
from Backend.utils.utils import get_guild


async def get_utilities(ctx, guild=None, engine=None):
    logging.info("get_character")
    if engine is None:
        engine = get_asyncio_db_engine(user=USERNAME, password=PASSWORD, host=HOSTNAME, port=PORT, db=SERVER_DATA)
    guild = await get_guild(ctx, guild)
    if guild.system == "D4e":
        return D4e_Utilities(ctx, guild, engine)
    elif guild.system == "PF2":
        return PF2_Utilities(ctx, guild, engine)
    elif guild.system == "EPF":
        return EPF_Utilities(ctx, guild, engine)
    elif guild.system == "STF":
        return STF_Utilities(ctx, guild, engine)
    else:
        return Utilities(ctx, guild, engine)