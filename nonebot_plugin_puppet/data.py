import yaml
from pathlib import Path
from typing import Optional, Dict

__DATA_PATH = Path() / "data" / "puppet" / "conv_mapping.yml"


def get_conv_mapping(reverse: bool = False):
    conv_mapping = __load_conv_mapping()

    if reverse:
        return {conv_mapping[key]["conv_id"]: key for key in conv_mapping}

    return conv_mapping


def link_conv(
    origin: int,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
):
    __update_conv_mapping(origin, True, user_id, group_id)


def unlink_conv(origin: int):
    __update_conv_mapping(origin, False)


# 更新会话映射
def __update_conv_mapping(
    origin: int,
    link: bool,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
):
    conv_mapping = get_conv_mapping()

    if link:
        conv_id = user_id if user_id else group_id
        type = "user" if user_id else "group"
        conv_mapping[origin] = {"type": type, "conv_id": conv_id}
    else:
        conv_mapping.pop(origin)

    __dump_conv_mapping(conv_mapping)


# 保存会话映射
def __load_conv_mapping() -> Dict[int, int]:
    try:
        return yaml.safe_load(__DATA_PATH.open("r", encoding="utf-8"))
    except FileNotFoundError:
        return {}


# 保存会话映射
def __dump_conv_mapping(conv_mapping: Dict[int, int]):
    __DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    yaml.dump(
        conv_mapping,
        __DATA_PATH.open("w", encoding="utf-8"),
        allow_unicode=True,
    )
