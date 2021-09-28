from yaml import safe_load, dump
from pathlib import Path
from typing import List, Dict

Conv = Dict[str, List[int]]


class ConvMapping:
    __path: Path
    __conv_mapping: Dict[str, Dict[int, Conv]]

    def __init__(self, path: Path = Path() / "data" / "puppet" / "conv_mapping.yml"):
        self.__path = path
        self.__load()

    def get_conv(
        self, conv: Conv = {"user": [], "group": []}, reverse: bool = False
    ) -> Conv:

        tmp_conv_mapping = {"user": [], "group": []}

        if conv == {"user": [], "group": []}:
            for type_a in self.__conv_mapping:
                for id_a in self.__conv_mapping[type_a]:
                    tmp_conv_mapping[type_a].append(id_a)
        else:
            if reverse:
                for type_b in conv:
                    for id_b in conv[type_b]:
                        for type_a in self.__conv_mapping:
                            for id_a in self.__conv_mapping[type_a]:
                                if id_b in self.__conv_mapping[type_a][id_a][type_b]:
                                    tmp_conv_mapping[type_a].append(id_a)
            else:
                for type_a in conv:
                    for id_a in conv[type_a]:
                        if id_a in self.__conv_mapping[type_a]:
                            tmp_conv_mapping = self.__conv_mapping[type_a][id_a]

        return tmp_conv_mapping

    def update_conv(self, conv: Conv) -> "ConvMapping":
        other = ConvMapping().__add_conv(conv).__remove_conv(conv)
        self.__add_conv(conv).__remove_conv(other.get_conv())
        self.__dump()
        return self

    # 添加会话映射
    def link_conv(
        self, conv_a: Conv, conv_b: Conv, unidirect=False
    ) -> Dict[str, Dict[int, Conv]]:
        result = {"user": {}, "group": {}}
        for type in result:
            for id in conv_b[type] if unidirect else conv_a[type] + conv_b[type]:
                result[type][id] = {"user": [], "group": []}
        for type_b in conv_b:
            for id_b in conv_b[type_b]:
                for type_a in conv_a:
                    for id_a in conv_a[type_a]:
                        if (
                            type_a == type_b
                            and id_a == id_b
                            or id_a not in self.__conv_mapping[type_a]
                            or id_b not in self.__conv_mapping[type_b]
                        ):
                            continue
                        if id_b not in self.__conv_mapping[type_a][id_a][type_b]:
                            self.__conv_mapping[type_a][id_a][type_b].append(id_b)
                            result[type_b][id_b][type_a].append(id_a)
                        if (
                            not unidirect
                            and id_a not in self.__conv_mapping[type_b][id_b][type_a]
                        ):
                            self.__conv_mapping[type_b][id_b][type_a].append(id_a)
                            result[type_a][id_a][type_b].append(id_b)
        self.__dump()
        return result

    # 移除会话映射
    def unlink_conv(
        self, conv_a: Conv, conv_b: Conv, unidirect=False
    ) -> Dict[str, Dict[int, Conv]]:
        result = {"user": {}, "group": {}}
        for type in result:
            for id in conv_b[type] if unidirect else conv_a[type] + conv_b[type]:
                result[type][id] = {"user": [], "group": []}
        for type_b in conv_b:
            for id_b in conv_b[type_b]:
                for type_a in conv_a:
                    for id_a in conv_a[type_a]:
                        if (
                            type_a == type_b
                            and id_a == id_b
                            or id_a not in self.__conv_mapping[type_a]
                            or id_b not in self.__conv_mapping[type_b]
                        ):
                            continue
                        if id_b in self.__conv_mapping[type_a][id_a][type_b]:
                            self.__conv_mapping[type_a][id_a][type_b].remove(id_b)
                            result[type_b][id_b][type_a].append(id_a)
                        if (
                            not unidirect
                            and id_a in self.__conv_mapping[type_b][id_b][type_a]
                        ):
                            self.__conv_mapping[type_b][id_b][type_a].remove(id_a)
                            result[type_a][id_a][type_b].append(id_b)
        self.__dump()
        return result

    # 添加会话
    def __add_conv(self, conv: Conv) -> "ConvMapping":
        for type in conv:
            for id in conv[type]:
                if id not in self.__conv_mapping[type]:
                    self.__conv_mapping[type][id] = {"user": [], "group": []}
        return self

    # 移除会话
    def __remove_conv(self, conv: Conv) -> "ConvMapping":
        new_conv_mapping = {"user": {}, "group": {}}
        for type_a in self.__conv_mapping:
            for id_a in self.__conv_mapping[type_a]:
                if id_a not in conv[type_a]:
                    new_conv_mapping[type_a][id_a] = self.__conv_mapping[type_a][id_a]
                    for type_b in self.__conv_mapping[type_a][id_a]:
                        for id_b in self.__conv_mapping[type_a][id_a][type_b]:
                            if id_b in conv[type_b]:
                                new_conv_mapping[type_a][id_a][type_b].remove(id_b)
        self.__conv_mapping = new_conv_mapping
        return self

    # 导入会话映射
    def __load(self) -> "ConvMapping":
        try:
            self.__conv_mapping = safe_load(self.__path.open("r", encoding="utf-8"))
        except FileNotFoundError:
            self.__conv_mapping = {"user": {}, "group": {}}
        return self

    # 导出会话映射
    def __dump(self):
        self.__path.parent.mkdir(parents=True, exist_ok=True)
        dump(
            self.__conv_mapping,
            self.__path.open("w", encoding="utf-8"),
            allow_unicode=True,
        )
