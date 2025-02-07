import logging

import d20
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.openapi.models import APIKey
from pydantic import BaseModel

from Backend.API.api_utils import get_guild_by_id, get_username_by_id, post_message, get_api_key
from Discord.Bot import bot
from Backend.Database.database_operations import log_roll
from Backend.utils.error_handling_reporting import API_ErrorReport
from Backend.utils.parsing import opposed_roll, eval_success
from Backend.utils.utils import relabel_roll
import json

router = APIRouter()


class RollData(BaseModel):
    roll: str
    user: int | None = None
    dc: int | None = None
    secret: bool | None = False
    guildid: int | None = None
    discord_post: bool | None = False


@router.post("/roll")
async def api_roll(roll_data: RollData, background_tasks: BackgroundTasks, api_key: APIKey = Depends(get_api_key)):
    # print(roll_data)
    roll = relabel_roll(roll_data.roll)
    try:
        guild = await get_guild_by_id(roll_data.guildid)
        username = get_username_by_id(roll_data.user)

        roll_result = d20.roll(roll)
        roll_str = opposed_roll(roll_result, d20.roll(f"{roll_data.dc}")) if roll_data.dc else roll_result
        if roll_data.dc is not None:
            success = eval_success(roll_result, d20.roll(f"{roll_data.dc}"))
        else:
            success = None
        if roll_data.discord_post:
            try:
                if roll_data.secret:
                    background_tasks.add_task(
                        post_message, guild, message=f"```Secret Roll from {username}```\n{roll}\n{roll_str}", gm=True
                    )
                else:
                    background_tasks.add_task(
                        post_message, guild, message=f"```Roll from {username}```\n{roll}\n{roll_str}"
                    )
                post = True
            except Exception:
                post = False
        else:
            post = False

        output = {
            "roll": str(roll),
            "roll_result": str(roll_result),
            "total": int(roll_result.total),
            "success": success,
            "posted": post,
            "secret": roll_data.secret,
        }

        log_output = f"{output['roll']}:\n{output['roll_result']}"
        await log_roll(guild.id, username, log_output, secret=roll_data.secret)

        #
        json_op = json.dumps(output)
        # print(json_op)
        # return output
        return json_op

    except Exception as e:
        logging.warning(f"API /roll: {e}")
        report = API_ErrorReport(roll_data, "dice_roller", e, bot)
        await report.report()
