
<div align="center">

![:name](https://count.getloli.com/@astrbot_plugin_cube?name=astrbot_plugin_cube&theme=minecraft&padding=6&offset=0&align=top&scale=1&pixelated=1&darkmode=auto)

# astrbot_plugin_cube

_✨ [astrbot](https://github.com/AstrBotDevs/AstrBot) 魔方插件 ✨_  

[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![AstrBot](https://img.shields.io/badge/AstrBot-3.4%2B-orange.svg)](https://github.com/Soulter/AstrBot)
[![GitHub](https://img.shields.io/badge/作者-Zhalslar-blue)](https://github.com/Zhalslar)

</div>

## 🤝 介绍

魔方插件，支持三阶魔方，可多人参与

## 📦 安装

- 可以直接在astrbot的插件市场搜索astrbot_plugin_cube，点击安装，耐心等待安装完成即可
- 若是安装失败，可以尝试直接克隆源码：

```bash
# 克隆仓库到插件目录
cd /AstrBot/data/plugins
git clone https://github.com/Zhalslar/astrbot_plugin_cube

# 控制台重启AstrBot
```

## ⌨️ 使用说明

### 命令表

|     命令  | 简化命令 |  描述  |
|------|-------------|--------|
| /魔方     | /cb   | 初始化本群的魔方 |
| /魔方 <操作符> | /cb xxx   | 操作魔方，操作符详见下文 |
| /打乱魔方 | /cbk  | 打乱当前群聊的魔方         |
| /还原魔方 | /cbr  | 还原当前群聊的魔方         |
| /撤销操作 | /cbb  | 撤销上一步操作         |
| /添加公式 | /cba  | 添加魔方公式         |
| /删除公式 | /cbd  | 添加魔方公式         |
| /公式列表 | /cbl  | 查看存储的魔方公式    |
| /魔方帮助 | /cbh  | 查看魔方帮助         |

### 操作符

| 操作符 | 描述 |
|----------|---------|
| F、f | 转动正面（forword）  |
| B、b | 转动背面（back）  |
| L、l | 转动左面（left）  |
| R、r | 转动右面（right）  |
| U、u | 转动上面（up） |
| D、d | 转动下面（down）  |

- 大小写区别：大写为顺时针转动，小写为逆时针转动

- 示例：`/cb FfBbLlRrUuDd`(可组合操作符形成公式)

## 👥 贡献指南

- 🌟 Star 这个项目！（点右上角的星星，感谢支持！）
- 🐛 提交 Issue 报告问题
- 💡 提出新功能建议
- 🔧 提交 Pull Request 改进代码

## 📌 注意事项

- 想第一时间得到反馈的可以来插件反馈群（QQ群）：460973561（不点star不给进）

## 🤝 鸣谢

本插件的的核心代码来源于：
[https://github.com/initialencounter/cube](https://github.com/initialencounter/cube)
