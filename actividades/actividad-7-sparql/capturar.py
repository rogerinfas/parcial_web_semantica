import asyncio, pathlib, urllib.parse
from playwright.async_api import async_playwright

BASE = "http://localhost:3030"
DIR = pathlib.Path("actividades/actividad-7-sparql")
OUT = DIR / "capturas"

# (nombre, archivo .rq, alto del viewport, ver pestana Response)
CASOS = [
    ("ej1", "consultas/ej1_agregacion.rq", 1150, False),
    ("ej2", "consultas/ej2_optional.rq", 1420, False),
    ("ej3", "consultas/ej3_ask.rq", 1000, True),
    ("ej4", "consultas/ej4_construct.rq", 1250, False),
]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/chromium", headless=True)
        for name, rqf, alto, response_tab in CASOS:
            ctx = await b.new_context(viewport={"width": 1400, "height": alto}, device_scale_factor=1.5)
            page = await ctx.new_page()
            q = (DIR / rqf).read_text()
            await page.goto(f"{BASE}/#/", wait_until="networkidle")
            await page.goto(f"{BASE}/#/dataset/ds/query?query={urllib.parse.quote(q, safe='')}", wait_until="networkidle")
            await page.wait_for_timeout(1200)
            await page.click('button[aria-label="Run query"]')
            await page.wait_for_timeout(2500)
            if response_tab:
                await page.click('button[aria-label="Shows Response view"]')
                await page.wait_for_timeout(1200)
            dst = OUT / f"{name}.png"
            await page.screenshot(path=str(dst), full_page=False)
            print("captura:", dst)
            await ctx.close()
        await b.close()

asyncio.run(main())
