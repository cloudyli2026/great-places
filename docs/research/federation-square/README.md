# Federation Square — 实际验证记录

核查日期：2026-11-13。变更在 `research/federation-square-evidence` 分支，供PR Review；GitHub Pages生产站从main发布，不因本分支提交自动更新。

## 浏览器回归

真实 Chromium 156 / Playwright，1440×1000桌面、390×844移动及320×740窄屏；不是仅通过HTML源码推测显示效果。

**348项通过，0项失败，0页面脚本错误，0失败网络请求。** [机器记录](browser-results.json)

- 中英文各7章：仅当前章显示、正确高亮、正文与图注切换、html lang、图片alt、反向语言隐藏、页面无横向溢出。
- 逐章滚动到图片并执行浏览器 `img.decode()`，确认不是返回HTML的伪图片链接。检查包括本地SVG和原出版站图片；重复出现的资产也逐处检查。
- 实际点击导航和前一章；浏览器后退；旧 `#climate`、`#sources`、`#fed-gis-figure-ground` 路由。
- 点击图底放大，Escape关闭，焦点返回原按钮。
- 打印模式可见；实际导出[单页A4横向PDF](federation-square-factsheet.pdf)，`pdfinfo`确认1页。
- 本环境HTTPS经受管代理。Chromium仅信任当前环境代理CA的SPKI指纹；没有使用全局忽略证书错误。普通HTTP检查使用默认CA验证。该设置属于测试环境，不进入网页。

首轮实测发现重复图像ID和旧版打印样式造成空白；均修复后重新执行完整回归。本报告记录最终通过结果。

## 桌面与移动截图

以下是实际浏览器页面截图，以WebP保存；不是建筑研究原件或AI生成图。

| 章节 | 桌面1440px | 移动390px |
|---|---|---|
| 概况 | [桌面截图](desktop-intro.webp) | [移动截图](mobile-intro.webp) |
| 官方图底与图纸 | [桌面截图](desktop-scale.webp) | [移动截图](mobile-scale.webp) |
| 建筑边界与Atrium | [桌面截图](desktop-boundary.webp) | [移动截图](mobile-boundary.webp) |
| 使用、节庆与集会 | [桌面截图](desktop-life.webp) | [移动截图](mobile-life.webp) |

## 图底与来源

**GIS：907条建筑记录、907个多边形、28个内环、13,860个顶点；闭环／数值／类型检查通过，离线重建逐字节相同。** [机器结果](gis-results.txt)

快照SHA256：`6dd22665cce833d2a41433cf2b41b4d4dd5d9366d89b1b819178644a19695144`。独立检查还核对图幅裁切、内环填充和100m图形尺。图底保留2020原始几何，排除Bridge，白色区域不代表全部可步行。

**资源：34个本地引用有效；29个唯一远程URL全部GET通过，0失败。** [逐URL状态、MIME、字节数及哈希](link-results.json)

远程检查包含当前页面全部图片与外部链接、来源登记里的图片，以及2个真实PDF的文件头和MIME校验。此结论仅针对04页面及其资产，不声称修复了全站其他案例。逐资产登记由页面生成器同步为同源JSON，避免分支删除后遗留失效的GitHub分支链接。

## 研究完成度

[与01逐项对照审核](../../../cases/federation-square/RESEARCH_AUDIT.md)在Git仓库中；公开网页的“评价与来源”章亦内置对应表。

完成了真实出版图纸展示和官方GIS重建；**完整四向正立面套图、正式空间句法计算与独立行为观察仍缺证据，不能宣称已完成**。剖面内的真实投影立面与立面照片分别标注，不把后者当作测绘图。原版权文件继续留在出版站，图片直接显示并附出处。

## 重跑

```sh
python -m http.server 8000 --directory docs
# 另一个终端；Node中需可用Playwright，默认Chromium路径/usr/bin/chromium
node tests/federation-browser.cjs
python tests/federation-gis.py
python tests/federation-links.py
```

页面重建：`python scripts/build_federation_page.py`。GIS离线重建：`python scripts/update_federation_gis.py --offline`。运行默认浏览器测试会将新记录保存到当前目录下的 `work/browser-results/`，不会自动覆盖已提交报告。
