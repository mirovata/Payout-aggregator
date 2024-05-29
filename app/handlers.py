import json
from datetime import datetime

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.algorithm import payout_aggregator

router = Router()


@router.message(F.text != '/start')
async def command_report_handler(message: Message):
    try:
        dict1 = json.loads(message.text)
        dt_from = datetime.fromisoformat(dict1['dt_from'])
        dt_upto = datetime.fromisoformat(dict1['dt_upto'])
        group_type = dict1['group_type']
        if (group_type in ['month', 'hour', 'day']
           and (dt_from < dt_upto and dt_from != dt_upto)):
            result = await payout_aggregator(dt_from, dt_upto, group_type)
            await message.answer(json.dumps(result))
        else:
            raise Exception
    except Exception:
        await message.answer(
              'Допустимо отправлять только следующие запросы:\n'
              '{"dt_from": "2022-09-01T00:00:00",'
              '"dt_upto": "2022-12-31T23:59:00", "group_type": "month"}\n'
              '{"dt_from": "2022-10-01T00:00:00",'
              '"dt_upto": "2022-11-30T23:59:00", "group_type": "day"}\n'
              '{"dt_from": "2022-02-01T00:00:00",'
              '"dt_upto": "2022-02-02T00:00:00", "group_type": "hour"}'
            )


@router.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f'Добро пожаловать, {message.from_user.first_name}!')
