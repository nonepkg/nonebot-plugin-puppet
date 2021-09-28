from yaml import safe_load, dump
from pathlib import Path
from typing import List, Dict

Req = Dict[str, List[str]]


class ReqList:
    __path: Path
    __req_list: Req
    __req_list_template: Req = {"friend": [], "invite": [], "add": []}

    def __init__(self, path: Path = Path() / "data" / "puppet" / "req_list.yml"):
        self.__path = path
        self.__load()

    def get_req(self):
        return self.__req_list

    # 添加请求
    def add_req(self, req: Req) -> "ReqList":
        for type in req:
            for flag in req[type]:
                if flag not in self.__req_list[type]:
                    self.__req_list[type].append(flag)
        self.__dump()
        return self

    # 移除请求
    def remove_req(self, req: Req) -> "ReqList":
        for type in req:
            for flag in req[type]:
                if flag in self.__req_list[type]:
                    self.__req_list[type].remove(flag)
        self.__dump()
        return self

    # 导入请求列表
    def __load(self) -> "ReqList":
        try:
            self.__req_list = safe_load(self.__path.open("r", encoding="utf-8"))
        except FileNotFoundError:
            self.__req_list = self.__req_list_template
        return self

    # 导出请求列表
    def __dump(self):
        self.__path.parent.mkdir(parents=True, exist_ok=True)
        dump(
            self.__req_list,
            self.__path.open("w", encoding="utf-8"),
            allow_unicode=True,
        )
