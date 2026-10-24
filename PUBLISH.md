# GitHub 发布步骤

这个目录已经整理成 GitHub 仓库内容。推荐仓库名：

```text
LeftLeftLEFT-zh-CN
```

## 网页操作

1. 打开 https://github.com/new
2. Repository name 填 `LeftLeftLEFT-zh-CN`
3. 选择 **Public**，创建仓库。
4. 上传本目录除 `release/` 外的文件：
   - README.md
   - LICENSE.md
   - CHANGELOG.md
   - TESTING.md
   - PATCH_MANIFEST.json
   - translation/
   - source/
   - tools/
5. 进入 **Releases → Draft a new release**
6. Tag 填 `v1.0.0`，标题填：
   `v1.0.0 — Left! Left! LEFT! Playtest 简体中文汉化补丁`
7. 上传 `release/LeftLeftLEFT_zh_CN_patch_v1.0.0.zip`
8. 发布。

## 命令行（安装了 Git 和 GitHub CLI）

```powershell
gh auth login
cd github-publish
git init
git add .
git commit -m "Left! Left! LEFT! Playtest 简体中文汉化补丁 v1.0.0"
gh repo create LeftLeftLEFT-zh-CN --public --source=. --remote=origin --push
gh release create v1.0.0 .\release\LeftLeftLEFT_zh_CN_patch_v1.0.0.zip `
  --title "v1.0.0 — Left! Left! LEFT! Playtest 简体中文汉化补丁" `
  --notes-file CHANGELOG.md
```

## 让别人搜得到

- 仓库 Description 填：`Left! Left! LEFT! Playtest 简体中文汉化补丁 | Steam build 26172243`
- Topics 填：`left-left-left`, `playtest`, `chinese-localization`, `unity`, `steam`
- README 标题保持完整游戏名 + “简体中文汉化补丁”
- 发布后把 Release 链接发到 Steam 社区指南、Bilibili 简介、Keylol/NGA/贴吧
- 可在 Bing Webmaster / Google Search Console 提交仓库或 Release URL（可选）

搜索引擎是否收录、排名如何，取决于索引时间和外链，不能保证第一页。
