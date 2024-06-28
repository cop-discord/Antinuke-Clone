from typing import Optional, List, Dict
from playwright.async_api import Page, BrowserContext, async_playwright
from dataclasses import dataclass
from tuuid import tuuid
from discord import File
from io import BytesIO
from asyncio import ensure_future, sleep
from playwright_stealth import stealth_async

@dataclass
class BrowserPage:
    page: Page
    key: str
    busy: bool

class Session:
    def __init__(self: "Session", headless: Optional[bool] = True, proxy: Optional[Dict[str, str]] = None):
        self.proxy: Optional[Dict[str, str]] = proxy
        self.headless: bool = headless
        self.pages: List[BrowserPage] = list()
        self.browser = None
        self.context = None

    async def new_context(self: "Session", **kwargs) -> BrowserContext:
        if not kwargs.get('user_agent'):
            self.context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0", **kwargs
            )
        else:
            self.context = await self.browser.new_context(**kwargs)
        return self.context
    
    async def launch(self: "Session"):
        self.browser = await async_playwright().__aenter__()
        self.browser = await self.browser.chromium.launch(
            args=["--stealth", "--no-incognito"],
            proxy=self.proxies[0],
            ignore_default_args=["--headless"],
            slow_mo=False,
            headless = self.headless
        )

    async def get_page(self: "Session") -> Page:
        if len(self.pages) == 0:
            page = await self.browser.new_page()
            key = str(tuuid())
            await stealth_async(page)
            self.pages.append(BrowserPage(page, True, key))
            ensure_future(self.update_page(key, True))
            return page
        for page in self.pages:
            if not page.busy:
                page.busy = True
                key = page.key
                ensure_future(self.update_page(key, True))
                return page.page
        page = await self.browser.new_page()
        await self.context.new_cdp_session(page)
        key = str(tuuid())
        await stealth_async(page)
        self.pages.append(BrowserPage(page, True, key))
        ensure_future(self.update_page(key, True))
        return page

    async def update_page(self: "Session", key: str, later: Optional[bool] = False):
        if later:
            await sleep(20)
        page = [p for p in self.pages if p.key == key][0]
        index = self.pages.index(page)
        page.busy = False
        self.pages[index] = page
        return True
    
    async def screenshot(self: "Session", url: str):
        page = await self.get_page()
        await page.goto(url, wait_until = "networkidle")
        _ = await page.screenshot()
        await self.update_page(page.key, True)
        return File(fp = BytesIO(_), filename = "screenshot.png")
    
    #not putting anymore time or effort into this its meant to be shit lol