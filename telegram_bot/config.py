from dataclasses import dataclass
from typing import List

from environs import Env


# Manual about dataclass: https://docs.python.org/3/library/dataclasses.html
@dataclass
class TgBot:
    token: str
    admin_ids: List[int]


@dataclass
class Misc:
    other_parameters = None


@dataclass
class Config:
    tg_bot: TgBot
    misc: Misc


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
        ),
        misc=Misc()
    )
