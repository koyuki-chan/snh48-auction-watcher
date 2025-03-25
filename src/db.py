import sqlite3
from src.logger import log_error,log_info

DB_NAME = 'goods_data.db'


def get_max_goods_id():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM goods")
        max_id = cursor.fetchone()[0]
        cursor.close()
        return max_id if max_id else 0
    except Exception as e:
        log_error(f"獲取最大 ID 時發生錯誤: {e}")
        return 0

def create_db():
    try:
        # 連接資料庫，如果資料庫不存在，會自動創建
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # 創建資料表（如果尚未存在），這裡將資料表名稱改為 'goods'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goods (
                id int PRIMARY KEY,
                name TEXT,
                img_url TEXT,
                current_price TEXT,
                bid_count TEXT,
                auction_status TEXT
            )
        ''')

        conn.commit()
        cursor.close()
        log_info("資料庫和資料表 'goods' 創建成功！")
    except Exception as e:
        log_error(f"資料庫初始化失敗: {e}")

def insert_goods_data(goods_data):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # 插入數據（如果資料已存在，則會更新）
        cursor.execute('''
            INSERT OR REPLACE INTO goods (id, name, img_url, current_price, bid_count, auction_status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            goods_data['id'],
            goods_data['name'],
            goods_data['img_url'],
            goods_data['current_price'],
            goods_data['bid_count'],
            goods_data['auction_status']
        ))
        
        # 提交變更並關閉資料庫連接
        conn.commit()
        cursor.close()
        log_info(f"商品 {goods_data['id']} 插入/更新成功！")
    except Exception as e:
        log_error(f"插入商品 {goods_data['id']} 時發生錯誤: {e}")

def fetch_all_goods():
    """獲取資料庫內所有商品數據"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM goods ORDER BY id ASC")
        rows = cursor.fetchall()
        cursor.close()
        goods_dict = {
            str(row[0]): {  # 以商品 ID 作為 key
                'id': str(row[0]),
                'name': row[1],
                'img_url': row[2],
                'current_price': row[3],
                'bid_count': row[4],
                'auction_status': row[5]
            }
            for row in rows
        }

        log_info(f"成功獲取 {len(rows)} 筆商品數據！")
        return goods_dict
    except Exception as e:
        log_error(f"獲取商品數據時發生錯誤: {e}")
        return {}

def delete_goods(item_id):
    """刪除指定 ID 的商品"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM goods WHERE id = ?", (item_id,))
        conn.commit()
        cursor.close()
        log_info(f"商品 {item_id} 刪除成功！")
    except Exception as e:
        log_error(f"刪除商品 {item_id} 時發生錯誤: {e}")