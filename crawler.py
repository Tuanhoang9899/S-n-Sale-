import json
import datetime

# --- CẤU HÌNH API SÀN & ACCESS (THAY THÔNG TIN THẬT CỦA BẠN KHI CÓ) ---
SHOPEE_APP_ID = "YOUR_SHOPEE_APP_ID"
SHOPEE_SECRET = "YOUR_SHOPEE_SECRET"
ACCESS_TRADE_API_KEY = "YOUR_ACCESSTRADE_API_KEY"

def map_category(raw_category_name):
    """
    Hàm ánh xạ (Mapping): Gom các tên danh mục rườm rà từ sàn
    về 3 nhóm danh mục chuẩn hiển thị trên website của bạn.
    """
    name = raw_category_name.lower()
    if any(k in name for k in ["điện tử", "phụ kiện", "tai nghe", "sạc", "chuột", "bàn phím", "công nghệ"]):
        return "Công nghệ & Phụ kiện"
    elif any(k in name for k in ["gia dụng", "bếp", "nồi", "hút bụi", "bình giữ nhiệt", "nhà cửa"]):
        return "Gia dụng thông minh"
    elif any(k in name for k in ["thời trang", "áo", "quần", "mỹ phẩm", "skincare", "kính", "serum"]):
        return "Thời trang & Làm đẹp"
    else:
        return "Công nghệ & Phụ kiện" # Nhóm mặc định nếu không khớp

def fetch_shopee_deals():
    """
    Kết nối Shopee Affiliate Open API hoặc Data Feed để lấy sản phẩm.
    (Dưới đây là cấu trúc dữ liệu mẫu chuẩn hóa khớp với Frontend của bạn)
    """
    print("Đang quét dữ liệu từ Shopee Affiliate API...")

    # Thực tế bạn sẽ dùng requests.get() gọi vào API của Shopee ở đoạn này
    raw_shopee_data = [
        {
            "id": 1,
            "platform": "Shopee",
            "shopBadge": "Mall",
            "raw_cat": "Thiết Bị Điện Tử & Phụ Kiện",
            "title": "Tai nghe Bluetooth Gaming TWS siêu trễ thấp chống ồn chủ động ANC",
            "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&h=600&fit=crop",
            "price": 199000,
            "avgPrice30d": 340000,
            "originalPrice": 450000,
            "discount": 56,
            "sold": "1.2k",
            "rating": 4.9,
            "freeship": True,
            "cashback": True,
            "rawUrl": "https://shopee.vn/product/123/456"
        },
        {
            "id": 5,
            "platform": "Shopee",
            "shopBadge": "Mall",
            "raw_cat": "Đồ Gia Dụng Nhà Bếp",
            "title": "Nồi chiên không dầu điện tử dung tích lớn 6L cảm ứng",
            "image": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=600&h=600&fit=crop",
            "price": 890000,
            "avgPrice30d": 1350000,
            "originalPrice": 1800000,
            "discount": 51,
            "sold": "850",
            "rating": 5.0,
            "freeship": True,
            "cashback": True,
            "rawUrl": "https://shopee.vn/product/444/555"
        }
    ]
    return raw_shopee_data

def fetch_tiktok_deals():
    """
    Lấy dữ liệu TikTok Shop qua Data Feed từ mạng Affiliate (VD: Accesstrade)
    """
    print("Đang quét dữ liệu từ TikTok Shop Data Feed...")

    raw_tiktok_data = [
        {
            "id": 2,
            "platform": "TikTok",
            "shopBadge": "Mall",
            "raw_cat": "Thiết bị di động & Phụ kiện",
            "title": "Sạc dự phòng không dây từ tính 10000mAh sạc nhanh 22.5W",
            "image": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=600&h=600&fit=crop",
            "price": 245000,
            "avgPrice30d": 390000,
            "originalPrice": 520000,
            "discount": 53,
            "sold": "2.1k",
            "rating": 4.8,
            "freeship": True,
            "cashback": False,
            "rawUrl": "https://shop.tiktok.com/view/product/789"
        },
        {
            "id": 8,
            "platform": "TikTok",
            "shopBadge": "Top Shop",
            "raw_cat": "Thời Trang Nam Nữ",
            "title": "Áo khoác gió bomber unisex form rộng phong cách Hàn Quốc",
            "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&h=600&fit=crop",
            "price": 149000,
            "avgPrice30d": 240000,
            "originalPrice": 350000,
            "discount": 57,
            "sold": "3.4k",
            "rating": 4.8,
            "freeship": True,
            "cashback": True,
            "rawUrl": "https://shop.tiktok.com/view/product/999"
        }
    ]
    return raw_tiktok_data

def main():
    print("=== BẮT ĐẦU QUÉT VÀ CHUẨN HÓA DỮ LIỆU SĂN SALE ===")

    # 1. Thu thập dữ liệu từ các sàn
    all_raw_deals = fetch_shopee_deals() + fetch_tiktok_deals()

    processed_deals = []
    for deal in all_raw_deals:
        # 2. Áp dụng hàm chuẩn hóa danh mục động
        deal["category"] = map_category(deal.pop("raw_cat"))

        # 3. Bộ lọc chất lượng: Chỉ giữ sản phẩm giảm giá >= 50% và đánh giá >= 4.8★
        if deal["discount"] >= 50 and deal["rating"] >= 4.8:
            processed_deals.append(deal)

    # Sắp xếp các deal có mức giảm % sâu nhất lên đầu danh sách
    processed_deals.sort(key=lambda x: x["discount"], reverse=True)

    output_payload = {
        "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_deals": len(processed_deals),
        "deals": processed_deals
    }

    # 4. Xuất ra file deals.json để Frontend đọc
    filename = "deals.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, ensure_ascii=False, indent=4)

    print(f"Thành công! Đã xử lý và xuất {len(processed_deals)} deal chuẩn vào file '{filename}'.")

if __name__ == "__main__":
    main()