import yaml
from pydantic import BaseModel
from pathlib import Path
from typing import Union, Optional, List, Dict

__DATA_PATH = Path() / "data" / "transfer" / "conv_mapping.yml"

class Map(BaseModel):
    user: Union[Dict[int,"Map"],List[int]]
    group: Union[Dict[int,"Map"],List[int]]

def get_conv_mapping(
    reverse: bool = False,
) -> Dict[str, Dict[int, Dict[str, List[int]]]]:

    conv_mapping = __load_conv_mapping()

    if reverse:
        reverse_conv_mapping = {"user": {}, "group": {}}
        for send_type in conv_mapping:
            for send_conv_id in conv_mapping[send_type]:
                for recv_type in conv_mapping[send_type][send_conv_id]:
                    for recv_conv_id in conv_mapping[send_type][send_conv_id][
                        recv_type
                    ]:
                        if recv_conv_id in reverse_conv_mapping[recv_type]:
                            if (
                                send_type
                                in reverse_conv_mapping[recv_type][recv_conv_id]
                            ):
                                reverse_conv_mapping[recv_type][recv_conv_id][
                                    send_type
                                ].append(send_conv_id)
                            else:
                                reverse_conv_mapping[recv_type][recv_conv_id][
                                    send_type
                                ] = [send_conv_id]
                        else:
                            reverse_conv_mapping[recv_type][recv_conv_id] = {
                                send_type: [send_conv_id]
                            }
        return reverse_conv_mapping
    else:
        return conv_mapping


def link_conv(
    send_type: Optional[str] = None,
    send_user_id: Optional[int] = None,
    send_group_id: Optional[int] = None,
    recv_type: Optional[str] = None,
    recv_user_id: Optional[int] = None,
    recv_group_id: Optional[int] = None,
):
    __update_conv_mapping(
        True,
        send_type,
        send_user_id,
        send_group_id,
        recv_type,
        recv_user_id,
        recv_group_id,
    )


def unlink_conv(
    send_type: Optional[str] = None,
    send_user_id: Optional[int] = None,
    send_group_id: Optional[int] = None,
    recv_type: Optional[str] = None,
    recv_user_id: Optional[int] = None,
    recv_group_id: Optional[int] = None,
):
    __update_conv_mapping(
        False,
        send_type,
        send_user_id,
        send_group_id,
        recv_type,
        recv_user_id,
        recv_group_id,
    )


# 更新会话映射
def __update_conv_mapping(
    link: bool,
    send_type: Optional[str] = None,
    send_user_id: Optional[int] = None,
    send_group_id: Optional[int] = None,
    recv_type: Optional[str] = None,
    recv_user_id: Optional[int] = None,
    recv_group_id: Optional[int] = None,
):
    conv_mapping = get_conv_mapping()

    if not send_type:
        send_type = "user" if send_user_id else "group"
    send_conv_id = send_user_id if send_type == "user" else send_group_id

    if not recv_type:
        recv_type = "user" if recv_user_id else "group"
    recv_conv_id = recv_user_id if recv_type == "user" else recv_group_id

    if link:
        if send_conv_id in conv_mapping[send_type]:
            if recv_type in conv_mapping[send_type][send_conv_id]:
                conv_mapping[send_type][send_conv_id][recv_type].append(recv_conv_id)
            else:
                conv_mapping[send_type][send_conv_id][recv_type] = [recv_conv_id]
        else:
            conv_mapping[send_type][send_conv_id] = {recv_type: [recv_conv_id]}
    else:
        conv_mapping[send_type][send_conv_id][recv_type].remove(recv_conv_id)

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
