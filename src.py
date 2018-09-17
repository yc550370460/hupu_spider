import aiohttp
import asyncio
import async_timeout
import bs4 as bs
import re
import os
from yarl import URL


BASIC_URL = "https://bbs.hupu.com/23562936.html"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "imgs")

async def get_pages(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, verify_ssl=False) as res:
            imgs = list()
            page = await res.text()
            soup = bs.BeautifulSoup(page, features="html.parser")
            static_rule = re.compile(r'.*data-original=.*')
            gif_rule = re.compile(r'.*\.gif"')
            img_list = soup.find_all("img")
            static_img_list = filter(lambda x: static_rule.match(str(x)), img_list)
            gif_img_list = filter(lambda x: gif_rule.match(str(x)), img_list)
            static_img_list = [str(item) for item in static_img_list]
            gif_img_list = [str(item) for item in gif_img_list]

            # img_list = list(img_list)
            for item in static_img_list:
                if item:
                    if len(item.split("data-original=")) > 1:
                        imgs.append(item.split('data-original="')[1].split(" data-w=")[0])
            for item in gif_img_list:
                if item:
                    if len(item.split("src=")) > 1:
                        imgs.append(item.split('src="')[1].split(".gif")[0] + ".gif")

            imgs = [item.split("?")[0] for item in imgs]
            print(imgs)
            await get_img(imgs)


async def get_img(urls):
    # urls=["https://i10.hoopchina.com.cn/hupuapp/bbs/673/212583948208673/thread_212583948208673_20180912151811_s_72906_w_623_h_516_42285.jpg"]
    async with aiohttp.ClientSession(connector_owner=True) as session:
        for index, url in enumerate(urls):

            async with session.get(URL(url, encoded=True), verify_ssl=False) as res:
                suffix = url.split(".")[4]
                print(url)
                page = await res.read()
                with open(os.path.join(IMG_DIR, str(index) + "." + suffix), "wb") as f:
                    f.write(page)


async def fetch(urls):
    async with aiohttp.ClientSession() as session:
        for url in urls:
            async with session.get(url) as res:
                page = await res.text()
                print(page)





if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = get_pages(BASIC_URL)
    loop.run_until_complete(tasks)
    loop.close()
    # main()