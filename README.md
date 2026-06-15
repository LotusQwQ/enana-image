# enana-image

《绘名号高性能！》bot 正在使用的图片底层工具代码。

## 功能

| 功能 | 说明 |
| --- | --- |
| `image_segment()` | 把图片 bytes、文件路径或 PIL 图片转成 OneBot v11 图片消息 |
| `uni_image()` | 把图片转成 nonebot-plugin-alconna 的 UniMessage 图片 |
| `uni_image_segment()` | 生成 nonebot-plugin-alconna 的图片片段 |
| `render_html_png()` | 用 Playwright 把 HTML/CSS 页面截图成 PNG |

## 依赖

按实际使用选择安装：

```bash
pip install pillow playwright nonebot-adapter-onebot nonebot-plugin-alconna
playwright install chromium
```

## 说明

这里只放通用图片工具代码，不包含 bot 配置、密钥、用户数据和具体插件业务逻辑。
