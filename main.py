from dotenv import load_dotenv

from model.type_alias import Environment
from src.bot import Bot
from tools.io import read_yaml


def check_env() -> str:
    # check environment variables
    conf = read_yaml(r"config/config.yaml")
    if conf["environment"] not in ["development", "production"]:
        raise ValueError(f"invalid environment: {conf['environment']}")
    else:
        environment: Environment = conf["environment"]
    env_path: str = f".env.{environment}"
    return env_path


def load_env() -> None:
    env_path: str = check_env()
    # print(env_path)
    load_dotenv(dotenv_path=env_path)


if __name__ == "__main__":
    load_env()
    bot = Bot()
    bot.run()
