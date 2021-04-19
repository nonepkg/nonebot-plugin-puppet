import yaml
from pathlib import Path
from typing import Literal, Optional, List, Dict

__DATA_PATH = Path() / "data" / "transfer" / "conv_mapping.yml"

def get_conv_mapping(
    type: Optional[str] = None,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
) -> Dict[str, List[int]]:

    if type is None:
        type = "user" if user_id else "group"
    id = user_id if type == "user" else group_id

    conv_mapping = __load_conv_mapping()

    if id in conv_mapping[type]:
        tmp_conv_mapping = conv_mapping[type][id]
    else:
        tmp_conv_mapping = {"user":[],"group":[]}

    return tmp_conv_mapping

def link_conv(
    user_id_a: List[int] = [],
    group_id_a: List[int] = [],
    user_id_b: List[int] = [],
    group_id_b: List[int] = [],
) -> Dict[str, ]:
    __update_conv_mapping(
        True,
        user_id_a,
        group_id_a,
        user_id_b,
        group_id_b,
    )


def unlink_conv(
    user_id_a: List[int] = [],
    group_id_a: List[int] = [],
    user_id_b: List[int] = [],
    group_id_b: List[int] = [],
) -> Dict[str, List[int]]:
    __update_conv_mapping(
        False,
        user_id_a,
        group_id_a,
        user_id_b,
        group_id_b,
    )


# 更新会话映射
def __update_conv_mapping(
    link: bool,
    user_id_a: List[int] = [],
    group_id_a: List[int] = [],
    user_id_b: List[int] = [],
    group_id_b: List[int] = [],
) -> Dict[str, List[int]]:

    conv_mapping = __load_conv_mapping()

    conv_a = [["user", user_id] for user_id in user_id_a] + [["group", group_id] for group_id in group_id_a]
    conv_b = [["user", user_id] for user_id in user_id_b] + [["group", group_id] for group_id in group_id_b]

    if link:
        for type_a,id_a in conv_a:
            for type_b,id_b in conv_b:
                if id_a not in conv_mapping[type_a]:
                    conv_mapping[type_a][id_a] = {"user": [id_b], "group": []}
                else:
                    if id_b not in conv_mapping[type_a][id_a][type_b]:
                        conv_mapping[type_a][id_a][type_b].append(id_b)
                if id_b not in conv_mapping[type_b]:
                    conv_mapping[type_b][id_b] = {"user": [id_a], "group": []}
                else:
                    if id_a not in conv_mapping[type_b][id_b][type_a]:
                        conv_mapping[type_b][id_b][type_a].append(id_a)
    else:
        for type_a,id_a in conv_a:
            for type_b,id_b in conv_b:
                if id_a in conv_mapping[type_a]:
                    if id_b in conv_mapping[type_a][id_a][type_b]:
                        conv_mapping[type_a][id_a][type_b].remove(id_b)
                    is_empty = True
                    for type in conv_mapping[type_a][id_a]:
                        if conv_mapping[type_a][id_a][type]:
                            is_empty=False
                            break
                    if is_empty:
                        conv_mapping[type_a].pop(id_a)

                if id_b in conv_mapping[type_b]:
                    if id_a in conv_mapping[type_b][id_b][type_a]:
                        conv_mapping[type_b][id_b][type_a].remove(id_a)
                    is_empty = True
                    for type in conv_mapping[type_b][id_b]:
                        if conv_mapping[type_b][id_b][type]:
                            is_empty=False
                            break
                    if is_empty:
                        conv_mapping[type_b].pop(id_b)

    __dump_conv_mapping(conv_mapping)


# 保存会话映射
def __load_conv_mapping() -> Dict[str, Dict[int, Dict[str, List[int]]]]:
    try:
        return yaml.safe_load(__DATA_PATH.open("r", encoding="utf-8"))
    except FileNotFoundError:
        return {"user": {}, "group": {}}


# 保存会话映射
def __dump_conv_mapping(conv_mapping: Dict[str, Dict[int, Dict[str, List[int]]]]):

    __DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    yaml.dump(
        conv_mapping,
        __DATA_PATH.open("w", encoding="utf-8"),
        allow_unicode=True,
    )