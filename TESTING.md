# 测试记录

- 测试日期：2026-10-24
- 系统：Windows 11 24H2
- 游戏：Steam AppID 5425110，buildid 26172243
- Unity：6000.3.16f1，Windows x64 IL2CPP

## 结果

1. 原版启动正常，主菜单可见。
2. 安装补丁后启动：
   - `Player.log` 中 `was not found in the ... font asset` 缺字警告：**0**
   - 未出现脚本异常 / 空引用 / 资源加载失败。
   - 主菜单 OCR 识别到：`主菜单`、`设置`、`退出`、`车组`、`驾驶破车`、`领航员` 等中文。
3. 补丁文件逐一通过 UnityPy 重新加载：
   - `level0`: 1424 objects
   - `level1`: 40354 objects
   - `level2`: 138439 objects
   - `level3`: 64424 objects
   - `sharedassets0.assets`: 38 objects
4. 安装器 / 卸载器在隔离的假游戏目录中完成备份、复制、SHA-256 校验、还原测试。

## 复现命令

```powershell
python tools/build_patch.py --game "D:\steam\steamapps\common\Left! Left! LEFT! Playtest" --out build
```

注意：构建脚本需要一份**未修改**的 build 26172243；Steam 更新后请重新核对文件哈希。
