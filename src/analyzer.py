from src.logger import log_info,log_error
from src.db import fetch_all_goods

def analyze_auction_changes(old_data,new_data):
    # old_data = {str(row[0]): {
    #     'id': row[0],
    #     'name': row[1],
    #     'img_url': row[2],
    #     'current_price': row[3],
    #     'bid_count': row[4],
    #     'auction_status': row[5]
    # } for row in fetch_all_goods()}  # ✅ 讀取資料庫中的舊數據
    
    new_entries = {}       
    price_increased = {}   
    auction_ended = {}     

    all_ids = set(old_data.keys()) | set(new_data.keys())
    
    for item_id in all_ids:
        old_item = old_data.get(item_id)
        new_item = new_data.get(item_id)

        if old_item is None:
            new_entries[item_id] = new_item
            continue

        if new_item is None:
            continue

        try:
            old_price = int(old_item['current_price'].replace("￥", "")) if old_item['current_price'] else 0
            new_price = int(new_item['current_price'].replace("￥", "")) if new_item['current_price'] else 0

            if new_price > old_price:
                price_increased[item_id] = {**old_item, **new_item}
                price_increased[item_id].update({
                    'old_price': old_price,
                    'new_price': new_price
                }) 
        except ValueError:
            log_error(f"商品 {item_id} 的價格格式錯誤，跳過比對")

        if old_item['auction_status'] != "已结束" and new_item['auction_status'] == "已结束":
            auction_ended[item_id] = {**old_item, **new_item}

    return {
        'new_entries': new_entries,
        'price_increased': price_increased,
        'auction_ended': auction_ended
    }
    
 