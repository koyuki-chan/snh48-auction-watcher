import requests
from bs4 import BeautifulSoup
from src.logger import log_error,log_info
from src.db import insert_goods_data,get_max_goods_id,get_goods_data
from time import sleep
URL = "https://shop.48.cn/pai"
PAGE_URL = "https://shop.48.cn/pai?pageNum={}"

def check_auction():
    auction_data_dict = {}
    page = 0            # Start From 0
    max_db_id = get_max_goods_id()

    try:
        log_info("開始爬取拍賣數據...")
        
        while True:
            url = PAGE_URL.format(page)     
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            goods_items = soup.select(".gs_xx") 
            
            if not goods_items:
                break
                
            for item in goods_items:
                link = item.select_one('.gs_1 a')['href']
                item_id = link.split('/')[-1]

                auction_data = {}
                for i in range(1,4):
                    class_name = f"gs_{i}"
                    element = item.select_one(f'.{class_name}')
                    auction_data[class_name] = element.text.strip()
                
                img_url = item.select_one('.gs_1 img')['src'] if item.select_one('.gs_1 img') else None
                current_price = item.select_one('.gs_4 .jg').text.strip() if item.select_one('.gs_4 .jg') else None
                bid_count = item.select_one('.gs_6 .icon.ic_cj').text.strip() if item.select_one('.gs_6 .icon.ic_cj') else None
                
                # 獲取競價狀態
                auction_status = None
                spans = item.select('.gs_6 span')
                if len(spans) > 1:
                    auction_status = spans[1].text.strip().replace("竞价状态：", "").strip()
                
                if max_db_id == 0 and auction_status == "已结束":
                    log_info("數據庫目前沒有數據，且抓取到已經結束的產品。")
                    tmp = {
                    'id': item_id, 
                    'name': auction_data.get('gs_2', "未知商品"),
                    'img_url': img_url,
                    'current_price': current_price,
                    'bid_count': bid_count,
                    'auction_status': auction_status
                    }
                    insert_goods_data(tmp)
                    return auction_data_dict
                auction_data_dict[item_id] = {
                    'id': item_id, 
                    'name': auction_data.get('gs_2', "未知商品"),
                    'img_url': img_url,
                    'current_price': current_price,
                    'bid_count': bid_count,
                    'auction_status': auction_status
                }

                existing_data = get_goods_data(item_id)
                if existing_data:
                    if existing_data['auction_status'] == "已结束":
                        log_info(f"發現已存在的已結束商品（{item_id}），停止爬取。")
                        return auction_data_dict
                insert_goods_data(auction_data_dict[item_id])
            log_info(f"第 {page} 頁獲取 {len(goods_items)} 項拍賣數據")
            page +=1
        
        log_info(f"所有頁面爬取完成，總共獲取 {len(auction_data_dict)} 項拍賣數據")
        return auction_data_dict
                
    except Exception as e:
        log_error(f"爬取拍賣數據時發生錯誤: {e}")
        return {}
