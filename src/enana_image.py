from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

from nonebot.adapters.onebot.v11 import MessageSegment
from PIL.Image import Image as PILImage

ImageSource = bytes | bytearray | memoryview | BytesIO | Path | str | PILImage


def png_bytes(image: PILImage) -> bytes:
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def image_bytes(source: ImageSource) -> bytes:
    if isinstance(source, bytes):
        return source
    if isinstance(source, (bytearray, memoryview)):
        return bytes(source)
    if isinstance(source, BytesIO):
        return source.getvalue()
    if isinstance(source, PILImage):
        return png_bytes(source)
    if isinstance(source, Path):
        return source.read_bytes()
    if isinstance(source, str):
        return Path(source).read_bytes()
    data = source.read()
    return data if isinstance(data, bytes) else bytes(data)


def image_segment(source: ImageSource) -> MessageSegment:
    data = image_bytes(source)
    return MessageSegment.image(f"base64://{base64.b64encode(data).decode()}")


def uni_image(source: ImageSource):
    from nonebot_plugin_alconna import UniMessage

    return UniMessage.image(raw=image_bytes(source))


def uni_image_segment(source: ImageSource):
    from nonebot_plugin_alconna.uniseg import Image

    return Image(raw=image_bytes(source))


async def render_html_png(
    html: str,
    *,
    viewport: tuple[int, int] = (1440, 1080),
    device_scale_factor: float = 1,
    full_page: bool = True,
    wait_until: str = "load",
    wait_for_function: str | None = None,
) -> bytes:
    from playwright.async_api import async_playwright

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        try:
            page = await browser.new_page(
                viewport={"width": viewport[0], "height": viewport[1]},
                device_scale_factor=device_scale_factor,
            )
            await page.set_content(html, wait_until=wait_until)
            if wait_for_function is not None:
                await page.wait_for_function(wait_for_function)
            return await page.screenshot(full_page=full_page, type="png")
        finally:
            await browser.close()
