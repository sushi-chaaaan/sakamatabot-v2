import json
from typing import Any

import aiofiles
import tomli as toml
import yaml


async def download_file(url: str, /, *, filename: str):
    import aiohttp

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"failed to download {url}")
            async with aiofiles.open(filename, mode="wb") as f:
                await f.write(await resp.read())
                await f.close()
                return


def read_json(filename: str) -> dict:
    with open(filename, mode="r") as f:
        return json.load(f)


def read_yaml(filename: str) -> Any:
    with open(filename, mode="r") as f:
        return yaml.safe_load(f)


def read_multi_yaml(filename: str) -> list[Any]:
    with open(filename, mode="r") as f:
        return [obj for obj in yaml.safe_load_all(f)]


def convert_json_to_yaml(filename: str) -> None:
    data = read_json(filename)
    new_name = remove_file_extension(filename) + ".yaml"
    print(f"converting {filename} to {new_name}")

    with open(new_name, mode="w") as f:
        yaml.safe_dump(data, f)
        print("converted to yaml")
        return


def read_toml(filename: str) -> dict:
    with open(filename, mode="rb") as f:
        return toml.load(f)


def remove_file_extension(filename: str) -> str:
    from pathlib import Path

    return filename.removesuffix(Path(filename).suffix)


def write_log(filename: str, data: str, append: bool = True):
    m = "a" if append else "w"
    with open(filename, mode=m) as f:
        f.write(data)
        return


if __name__ == "__main__":
    file_name: str = input("input file name: ")
    convert_json_to_yaml(file_name)
    # print(read_yaml("config/persistent_view.yaml"))
