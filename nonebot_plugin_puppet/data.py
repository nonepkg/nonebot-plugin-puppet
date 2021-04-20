import yaml
from pathlib import Path
from typing import List, Dict

Conv = Dict[str, List[int]]


class ConvMapping:
    path: Path
    conv_mapping: Dict[str, Dict[int, Conv]]

    def __init__(self, path: Path = Path() / "data" / "puppet" / "conv_mapping.yml"):
        self.__load(self, path)

    def get_conv(self, conv: Conv = {"user": [], "group": []}) -> Conv:

        tmp_conv_mapping = {"user": [], "group": []}

        if not conv == {"user": [], "group": []}:
            for type in conv:
                if conv[type] in self.conv_mapping[type]:
                    tmp_conv_mapping = self.conv_mapping[type][conv[type]]
        else:
            for type in self.conv_mapping:
                for id in self.conv_mapping[type]:
                    tmp_conv_mapping[type].append(id)

        return tmp_conv_mapping

    def update_conv(self, conv: Conv) -> "ConvMapping":
        other = ConvMapping().__add_conv(conv).__remove_conv(conv)
        self.__add_conv(conv).__remove_conv(other.get_conv())
        self.__dump()
        return self

    # 添加会话映射
    def link_conv(
        self, conv_a: Conv, conv_b: Conv
    ) -> Dict[str, Dict[int, Dict[str, Dict[int, bool]]]]:
        result = {"user": {}, "group": {}}
        for type in result:
            for id in conv_a[type] + conv_b[type]:
                result[type][id] = {"user": {}, "group": {}}
        for type_a in conv_a:
            for id_a in conv_a[type_a]:
                for type_b in conv_b:
                    for id_b in conv_b[type_b]:
                        if type_a == type_b and conv_a == conv_b:
                            result[type_a][id_a][type_b][id_b] = False
                            continue
                        if id_b in self.conv_mapping[type_a][id_a][type_b]:
                            result[type_a][id_a][type_b][id_b] = False
                        else:
                            self.conv_mapping[type_a][id_a].append(id_b)
                            result[type_a][id_a][type_b][id_b] = True
                        if id_a in self.conv_mapping[type_b][id_b][type_a]:
                            result[type_b][id_b][type_a][id_a] = False
                        else:
                            self.conv_mapping[type_b][id_b][type_a].append(id_a)
                            result[type_b][id_b][type_a][id_a] = True
        self.__dump()
        return result

    # 移除会话映射
    def unlink_conv(
        self, conv_a: Conv, conv_b: Conv
    ) -> Dict[str, Dict[int, Dict[str, Dict[int, bool]]]]:
        result = {"user": {}, "group": {}}
        for type in result:
            for id in conv_a[type] + conv_b[type]:
                result[type][id] = {"user": {}, "group": {}}
        for type_a in conv_a:
            for id_a in conv_a[type_a]:
                for type_b in conv_b:
                    for id_b in conv_b[type_b]:
                        if type_a == type_b and conv_a == conv_b:
                            result[type_a][id_a][type_b][id_b] = False
                            continue
                        if id_b not in self.conv_mapping[type_a][id_a][type_b]:
                            result[type_a][id_a][type_b][id_b] = False
                        else:
                            self.conv_mapping[type_a][id_a][type_b].remove(id_b)
                            result[type_a][id_a][type_b][id_b] = True
                        if id_a not in self.conv_mapping[type_b][id_b][type_a]:
                            result[type_b][id_b][type_a][id_a] = False
                        else:
                            self.conv_mapping[type_b][id_b][type_a].remove(id_a)
                            result[type_b][id_b][type_a][id_a] = True
        self.__dump()
        return result

    # 添加会话
    def __add_conv(self, conv: Conv) -> "ConvMapping":
        for type in conv:
            for id in conv[type]:
                if id not in self.conv_mapping[type]:
                    self.conv_mapping[type][id] = {"user": [], "group": []}
        self.__dump()
        return self

    # 移除会话
    def __remove_conv(self, conv: Conv) -> "ConvMapping":
        new_conv_mapping = {"user": {}, "group": {}}
        for type_a in self.conv_mapping:
            for id_a in self.conv_mapping[type_a]:
                if id_a not in conv[type_a]:
                    new_conv_mapping[type_a][id_a] = self.conv_mapping[type_a][id_a]
                    for type_b in self.conv_mapping[type_a][id_a]:
                        for id_b in self.conv_mapping[type_a][id_a][type_b]:
                            if id_b in conv[type_b]:
                                new_conv_mapping[type_a][id_a][type_b].remove(id_b)
        self.conv_mapping = new_conv_mapping
        self.__dump()
        return self

    # 导入会话映射
    def __load(self, path: Path) -> "ConvMapping":
        self.path = path
        try:
            self.conv_mapping = yaml.safe_load(self.path.open("r", encoding="utf-8"))
        except FileNotFoundError:
            self.conv_mapping = {"user": {}, "group": {}}
        return self

    # 导出会话映射
    def __dump(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        yaml.dump(
            self.conv_mapping,
            self.path.open("w", encoding="utf-8"),
            allow_unicode=True,
        )
