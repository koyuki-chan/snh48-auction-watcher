from src.db import fetch_all_goods
from src.logger import setup_loggers
from src.analyzer import analyze_auction_changes
from src.scraper import check_auction
setup_loggers()
old_data = fetch_all_goods()
new_data = check_auction()
print(old_data == new_data)

changes = analyze_auction_changes(old_data=old_data,new_data=new_data)
print(changes)


if changes['auction_ended']:
    for item_id, item in changes['auction_ended'].items():
        print(item)
    #     embed.add_field(name=f"商品 {item_id}", value="競拍已結束", inline=False)
    #     embed.set_image(url=item['img_url'])  # 添加圖片
    #     embed.add_field(name="出價數量", value=item['bid_count'], inline=True)
    #     embed.add_field(name="拍賣狀態", value=item['auction_status'], inline=True)
    # await channel.send(embed=embed)