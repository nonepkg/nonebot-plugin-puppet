import yaml
from pathlib import Path
from typing import Union, Optional, List, Dict

__DATA_PATH = Path() / "data" / "puppet" / "conv_mapping.yml"


def get_conv_mapping(
    type: Optional[str] = None,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
) -> Dict[str, List[int]]:

    conv_mapping = __load_conv_mapping()

    if type is None:
        type = "user" if user_id else "group"
    id = user_id if type == "user" else group_id

    if id in conv_mapping[type]:
        tmp_conv_mapping = conv_mapping[type][id]
    else:
        tmp_conv_mapping = {"user": [], "group": []}

    return tmp_conv_mapping


def link_conv(
    conv_a: List[List[Union[str, int]]] = [],
    conv_b: List[List[Union[str, int]]] = [],
):
    return __update_conv_mapping(
        True,
        conv_a,
        conv_b,
    )


def unlink_conv(
    conv_a: List[List[Union[str, int]]] = [],
    conv_b: List[List[Union[str, int]]] = [],
):
    return __update_conv_mapping(
        False,
        conv_a,
        conv_b,
    )


def auto_update_conv_mapping(conv: List[List[Union[str, int]]] = []):

    conv_mapping = __load_conv_mapping()
    new_conv_mapping = {"user": {}, "group": {}}

    for type, id in conv:
        if id not in conv_mapping:
            new_conv_mapping[type][id] = {"user": [], "group": []}

    for type_a in conv_mapping:
        for id_a in conv_mapping[type_a]:
            if id_a in [id for type, id in conv]:
                new_conv_mapping[type_a][id_a] = conv_mapping[type_a][id_a]
                for type_b in conv_mapping[type_a][id_a]:
                    for id_b in conv_mapping[type_a][id_a][type_b]:
                        if id_b not in [id for type, id in conv]:
                            new_conv_mapping[type_a][id_a][type_b].remove(id_b)

    __dump_conv_mapping(new_conv_mapping)


# 更新会话映射
def __update_conv_mapping(
    link: bool,
    conv_a: List[List[Union[str, int]]] = [],
    conv_b: List[List[Union[str, int]]] = [],
):

    conv_mapping = __load_conv_mapping()

    if link:
        for type_a, id_a in conv_a:
            for type_b, id_b in conv_b:
                if type_a == type_b and id_a == id_b:
                    continue
                if id_b not in conv_mapping[type_a][id_a][type_b]:
                    conv_mapping[type_a][id_a][type_b].append(id_b)
                if id_a not in conv_mapping[type_b][id_b][type_a]:
                    conv_mapping[type_b][id_b][type_a].append(id_a)
    else:
        for type_a, id_a in conv_a:
            for type_b, id_b in conv_b:
                if id_b in conv_mapping[type_a][id_a][type_b]:
                    conv_mapping[type_a][id_a][type_b].remove(id_b)
                if id_a in conv_mapping[type_b][id_b][type_a]:
                    conv_mapping[type_b][id_b][type_a].remove(id_a)

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
