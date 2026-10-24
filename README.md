# Left! Left! LEFT! Playtest 简体中文汉化补丁

[![Release](https://img.shields.io/badge/release-v1.0.0-blue)](../../releases/latest)
[![Game](https://img.shields.io/badge/Steam-AppID%205425110-1b2838)](https://store.steampowered.com/app/5425110/)
[![Build](https://img.shields.io/badge/build-26172243-green)]()

非官方简体中文 UI 汉化补丁，适用于 Steam 版 **Left! Left! LEFT! Playtest**。

## 下载

前往 [Releases](../../releases/latest) 下载：

- `LeftLeftLEFT_zh_CN_patch_v1.0.0.zip`

ZIP SHA-256：

```text
715845b84e1fbfe730e78a2d807b3078518271cb188c1b57acaf8ed97e3d3126
```

## 适用版本

- Steam AppID：**5425110**
- buildid：**26172243**
- Unity：**6000.3.16f1**（Windows x64，IL2CPP）
- 测试日期：2026-10-24

> 仅适用于上述 build。Steam 更新后请等待新版本补丁；安装器会校验文件哈希并拒绝不匹配的版本。

## 安装

1. 先完全退出游戏。
2. 解压 ZIP 到任意文件夹（不要直接在压缩包里运行）。
3. 双击 `install.bat`。
4. 如果脚本没有自动找到游戏，输入：

   `D:\steam\steamapps\common\Left! Left! LEFT! Playtest`

5. 看到“安装完成”后启动游戏。

安装器会自动把原文件备份到：

`LeftLeftLEFT_Data/_zh_CN_backup_<时间戳>/`

## 卸载

双击 `uninstall.bat`，按备份还原原文件。

## 内容

- 翻译 128 个可见 TextMeshProUGUI 文本组件（43 条唯一文本）：主菜单、好友/邀请、设置、暂停、关卡选择等。
- 将 `sharedassets0.assets` 的 `ShareTechMono-Regular SDF` 字体资产切换为 **DynamicOS + Microsoft YaHei**，运行时生成中文字形。
- 不修改 `LeftLeftLEFT.exe`、`GameAssembly.dll`、`steam_api64.dll`、`resources.assets`、存档或网络协议。

## 已知限制

1. 只适用于 build 26172243 / Unity 6000.3.16f1。
2. 依赖 Windows 的 **Microsoft YaHei** 字体；精简系统或非中文 Windows 可能显示方框。
3. 标题 `Left! Left! LEFT!`、`PLAYTEST`、`LOADING...` 保留英文。
4. 运行时生成的角色状态标签（`DRIVER`、`NAVIGATOR`、`empty seat`）保留英文；未修改 `global-metadata.dat`。
5. 仅覆盖 UI，不改变玩法或网络协议；多人游戏可各自选择中文/英文。
6. 非官方粉丝补丁；游戏资产版权归 Stellux Interactive 所有，请勿单独售卖或再分发游戏资产。

## 源文件 / 复现

- `translation/zh_CN.json`：43 条唯一文本的原文→译文
- `source/texts.json`：148 个文本组件的路径 ID 映射
- `tools/build_patch.py`：可复现构建脚本（需要 Python 3.10+ 与 UnityPy）
- `PATCH_MANIFEST.json`：原文件/补丁文件大小与 SHA-256

## 授权

翻译文本与文档：CC BY-NC-SA 4.0；脚本：MIT。游戏原始资产版权归其权利人所有。

## 免责声明

本补丁与 Stellux Interactive、Steam 或 Valve 无隶属关系。请先备份；使用风险自负。
