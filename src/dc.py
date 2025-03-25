import discord
import asyncio
from discord import Embed
from src.logger import log_info, log_error
from src.scraper import check_auction
from src.analyzer import analyze_auction_changes
from src.db import fetch_all_goods


class AuctionBot:
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        self.client = discord.Client(intents=discord.Intents.default())

    async def send_discord_notification(self, changes):
        channel = self.client.get_channel(self.channel_id)
        
        if not channel:
            log_error("找不到指定的 Discord 頻道！")
            return

        # 發送新增的商品
        if changes['new_entries']:
            for item_id, item in changes['new_entries'].items():
                embed = Embed(title="🆕 新增拍賣商品", color=0x00ff00)
                embed.add_field(name="商品名稱", value=item['name'], inline=False)
                embed.add_field(name="起拍價", value=f"{item['current_price']} RMB", inline=False)
                embed.add_field(name="出價數量", value=item['bid_count'], inline=True)
                embed.add_field(name="拍賣狀態", value=item['auction_status'], inline=True)
                embed.add_field(name="查看商品", value=f"[點擊這裡](https://shop.48.cn/item/{item_id})", inline=False)

                if item.get('img_url'):  # 確保每個 embed 只設置一次圖片
                    embed.set_image(url=item['img_url'])

                await channel.send(embed=embed)

        # 發送價格上漲的商品
        if changes['price_increased']:
            for item_id, item in changes['price_increased'].items():
                embed = Embed(title="📈 拍賣價格上漲", color=0xffa500)
                embed.add_field(name="商品名稱", value=item['name'], inline=False)
                embed.add_field(name="原價", value=f"原價：{item['old_price']} RMB → 新價：{item['new_price']} RMB", inline=True)

                embed.add_field(name="出價數量", value=item['bid_count'], inline=True)
                embed.add_field(name="拍賣狀態", value=item['auction_status'], inline=True)
                embed.add_field(name="查看商品", value=f"[點擊這裡](https://shop.48.cn/item/{item_id})", inline=False)

                if item.get('img_url'):
                    embed.set_image(url=item['img_url'])

                await channel.send(embed=embed)

        # 發送競拍結束的商品
        if changes['auction_ended']:
            for item_id, item in changes['auction_ended'].items():
                embed = Embed(title=f"⏳ 競拍狀態更新 - 商品 {item_id}", color=0xff0000)
                auction_status = item.get('auction_status', '未知狀態')

                embed.add_field(name="商品名稱", value=item['name'], inline=False)
                embed.add_field(name="競拍狀態", value=auction_status, inline=True)
                embed.add_field(name="出價數量", value=item['bid_count'], inline=True)
                embed.add_field(name="查看商品", value=f"[點擊這裡](https://shop.48.cn/item/{item_id})", inline=False)

                if item.get('img_url'):
                    embed.set_image(url=item['img_url'])

            await channel.send(embed=embed)
    async def check_and_notify(self):
        while True:
            old_data = fetch_all_goods()
            new_data = check_auction()
            changes = analyze_auction_changes(old_data=old_data,new_data=new_data)
            await self.send_discord_notification(changes)
            await asyncio.sleep(300)  # 每 5 分鐘檢查一次

    def run(self):
        # 註冊事件
        @self.client.event
        async def on_ready():
            log_info(f"已登入 Discord：{self.client.user}")
            asyncio.create_task(self.check_and_notify())  # 開始自動檢查拍賣變化
        self.client.run(self.token)  # 啟動 bot