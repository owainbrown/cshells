"""Frame captures of the header for review (ADR-0008).

Start `make serve` first, then run `make header-check`. Needs:
    pip install playwright && playwright install chromium webkit
Writes PNGs to build/header-check/.
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

URL = "http://localhost:1313/"
OUT = Path(__file__).resolve().parents[2] / "build" / "header-check"
TIMES = [0.5, 1.75, 3.5, 5.25, 7.2, 8.1, 13.15, 14.1]   # seconds into the animations

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        for engine in (p.chromium, p.webkit):
            browser = await engine.launch()
            for width in (1100, 390, 320):
                for scheme in ("light", "dark"):
                    page = await browser.new_page(viewport={"width": width, "height": 480}, color_scheme=scheme)
                    await page.goto(URL)
                    await page.evaluate("document.fonts.ready")
                    for t in TIMES:
                        await page.evaluate(f"document.getAnimations().forEach(a=>{{a.pause(); a.currentTime={t*1000};}})")
                        await page.locator(".site-header").screenshot(path=OUT / f"{engine.name}-{width}-{scheme}-{t}.png")
                    await page.close()
            await browser.close()
    print(f"wrote captures to {OUT}")

asyncio.run(main())
