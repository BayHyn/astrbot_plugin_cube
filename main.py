
import time
from typing import Dict
from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register
from astrbot.core.message.components import Image, Plain
from astrbot.core.platform.astr_message_event import AstrMessageEvent

from .render import DrawCube
from cube_rs import CubeCore  # type: ignore


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
        # 唤醒前缀
        self.wake_prefix: list[str] = context.get_config()["wake_prefix"]
        # 魔方对象字典
        self.obj_dist: Dict[str, CubeCore] = {}
        # 魔方绘制器
        self.drawer = DrawCube()

    @filter.command("魔方", alias={"cb"})
    async def start_cube(self, event: AstrMessageEvent):
        """进行魔方游戏"""
        group_id = event.get_group_id()
        steps = event.message_str.removeprefix("魔方").removeprefix("cb").strip()

        # 魔方初始化
        if group_id not in self.obj_dist:
            cube = CubeCore()
            self.obj_dist[group_id] = cube
            if not steps:
                yield event.chain_result(
                    [
                        Plain("本群的魔方已生成"),
                        Image.fromBytes(self.drawer.draw(cube.get_cube())),
                    ]
                )
                return

        # 魔方对象
        cube = self.obj_dist[group_id]
        raw_status = cube.is_solved()

        # 输入步骤
        cube.rotate(steps)

        if raw_status is False and cube.is_solved():
            yield event.chain_result(
                [
                    Plain(f"还原成功！耗时 {self.get_duration(cube.get_start_time())}"),
                    Image.fromBytes(self.drawer.draw(cube.get_cube())),
                ]
            )
            del self.obj_dist[group_id]
            return

        chain = []
        if steps:
            chain.append(Plain(f"操作: {cube.get_last_step()}"))
        else:
            chain.append(Plain(f"耗时：{self.get_duration(cube.get_start_time())}"))
        chain.append(Image.fromBytes(self.drawer.draw(cube.get_cube())))
        yield event.chain_result(chain)

    @filter.command("撤销操作", alias={"cbb"})
    async def back_cube(self, event: AstrMessageEvent):
        "撤销上一步的操作"
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
                Image.fromBytes(self.drawer.draw(cube.get_cube())),
            ]
        )
    @filter.command("打乱魔方", alias={"cbk"})
    async def break_cube(self, event: AstrMessageEvent):
        """打乱当前群聊的魔方"""
        group_id = event.get_group_id()
        cube = self.obj_dist[group_id]
        cube.scramble(1000)
        yield event.chain_result(
            [
                Plain("已打乱本群的魔方"),
                Image.fromBytes(self.drawer.draw(cube.get_cube())),
            ]
        )

    @filter.command("重置魔方", alias={"cbr"})
    async def reset_cube(self, event: AstrMessageEvent):
        """重置当前群聊的魔方"""
        group_id = event.get_group_id()
        cube = CubeCore()
        self.obj_dist[group_id] = cube
        yield event.chain_result(
            [
                Plain("已重置本群的魔方"),
                Image.fromBytes(self.drawer.draw(cube.get_cube())),
            ]
        )

    @filter.command("魔方帮助", alias={"cbh"})
    async def cube_help(self, event: AstrMessageEvent):
        """魔方帮助"""
        prefix = self.wake_prefix[0] if self.wake_prefix else ""
        help_text = (
            f"{prefix}cb <操作符> - 操作魔方\n"
            f"{prefix}cbb - 撤销上一步操作\n"
            f"{prefix}cbk - 打乱当前群聊的魔方\n"
            f"{prefix}cbr - 重置当前群聊的魔方\n\n"
            "操作符：FfBbLlRrUuDd\n"
            "对应面：前后左右上下\n"
            "大小写：大写顺时针，小写逆时针"
        )
        yield event.plain_result(help_text)

    @staticmethod
    def get_duration(start_time: int) -> str:
        """获取毫秒级耗时(格式化)"""
        duration = int((time.time() * 1000) - start_time)
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

