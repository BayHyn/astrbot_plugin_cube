
import time
from typing import Dict
from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register
from astrbot.core.message.components import Image, Plain
from astrbot.core.platform.astr_message_event import AstrMessageEvent

from .render import DrawCube
from cube_rs import CubeCore  # type: ignore
from .rank import Rank


@register(
    "astrbot_plugin_cube",
    "Zhalslar",
    "魔方插件",
    "1.0.0",
    "https://github.com/Zhalslar/astrbot_plugin_cube",
)
class PokeproPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.rank = Rank()
        self.obj_dist: Dict[str, CubeCore] = {}  # 记录魔方对象

    @filter.command("魔方", alias={"cube", "cb"})
    async def start_cube(self, event: AstrMessageEvent):
        """进行魔方游戏"""
        group_id = event.get_group_id()

        # 开启魔方
        if group_id not in self.obj_dist:
            cube = CubeCore()
            cube.scramble(1000)
            self.obj_dist[group_id] = cube
            yield event.chain_result(
                [
                    Plain("本群的魔方已生成"),
                    Image.fromBytes(DrawCube(cube.get_cube()).get_buf()),
                ]
            )
            return


        cube = self.obj_dist[group_id]

        # 输入步骤
        steps = event.message_str.removeprefix("魔方").removeprefix("cube").removeprefix("cb").strip()
        cube.rotate(steps)

        # 还原完成
        if cube.is_solved():
            duration = self.get_duration(cube.get_start_time())
            formatted_duration = self.format_duration(duration)
            self.rank.update_duration(group_id=group_id, duration=duration)
            yield event.chain_result(
                [
                    Plain(f"还原成功！耗时 {formatted_duration}"),
                    Image.fromBytes(DrawCube(cube.get_cube()).get_buf()),
                ]
            )
            del self.obj_dist[group_id]
            return

        chain = []
        if steps:
            chain.append(Plain(f"操作: {cube.get_last_step()}"))
        else:
            duration = self.get_duration(cube.get_start_time())
            formatted_duration = self.format_duration(duration)
            chain.append(Plain(f"耗时：{formatted_duration}"))
        chain.append(Image.fromBytes(DrawCube(cube.get_cube()).get_buf()))
        yield event.chain_result(chain)

    @filter.command("撤销操作")
    async def back_cube(self, event: AstrMessageEvent):
        group_id = event.get_group_id()
        cube = self.obj_dist[group_id]
        if len(cube.get_last_step()) == 0:
            yield event.plain_result("已撤销为最初状态")
        plain_texts: str = cube.get_last_step()
        for plain_text in plain_texts[::-1]:
            meth = ""
            if plain_text.islower():
                meth += plain_text
                cube.rotate(plain_text.upper())
            else:
                meth += plain_text
                cube.rotate(plain_text.lower())
        yield event.chain_result(
            [
                Plain(f"撤销操作:{''.join(plain_texts)}"),
                Image.fromBytes(DrawCube(cube.get_cube()).get_buf()),
            ]
        )
    @filter.command("打乱魔方")
    async def break_cube(self, event: AstrMessageEvent):
        group_id = event.get_group_id()
        cube = self.obj_dist[group_id]
        cube.scramble(1000)
        yield event.chain_result(
            [
                Plain("已打乱本群的魔方"),
                Image.fromBytes(DrawCube(cube.get_cube()).get_buf()),
            ]
        )

    @filter.command("还原魔方")
    async def init_cube(self, event: AstrMessageEvent):
        group_id = event.get_group_id()
        cube = CubeCore()
        self.obj_dist[group_id] = cube
        yield event.chain_result(
            [
                Plain("已还原本群的魔方"),
                Image.fromBytes(DrawCube(cube.get_cube()).get_buf()),
            ]
        )

    @filter.command("魔方排行榜")
    async def rank_cube(self, event: AstrMessageEvent):
        """魔方排行榜"""
        rank_text = self.rank.get_rank()
        yield event.plain_result(rank_text)

    @staticmethod
    def format_duration(duration: int) -> str:
        """格式化耗时，不显示小时和分钟为0的部分"""
        seconds, milliseconds = divmod(duration, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        time_parts = []
        if hours > 0:
            time_parts.append(f"{hours:02d}")
        if minutes > 0 or hours > 0:
            time_parts.append(f"{minutes:02d}")
        time_parts.append(f"{seconds:02d}.{milliseconds:03d}")

        return ":".join(time_parts)

    @staticmethod
    def get_duration(start_time: int) -> int:
        """获取毫秒级耗时"""
        return int((time.time() * 1000) - start_time)

