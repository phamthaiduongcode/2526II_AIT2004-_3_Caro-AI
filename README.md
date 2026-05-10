# 2526II_AIT2004-_3_Caro-AI

Chương trình chơi cờ Caro (4 in a row) tích hợp trí tuệ nhân tạo sử dụng thuật toán Minimax và Alpha-Beta Pruning.

## 📌 Tính năng chính
- Chế độ chơi: Người đấu với Máy (Console).
- Thuật toán AI: Minimax và Alpha-Beta Pruning.
- Tối ưu hóa: Move Ordering (ưu tiên trung tâm) và giới hạn vùng tìm kiếm.
- Hệ thống Log: Tự động ghi lại thời gian chạy và số trạng thái đã xét ra file CSV.
- Benchmark: Công cụ đo đạc hiệu năng tự động trên các kịch bản mẫu.

## 🛠 Cài đặt
Yêu cầu: Python 3.8 trở lên.

```bash
# Clone project
git clone <link-repo>
cd 2526II_AIT2004-_3_Caro-AI
```

## 🚀 Hướng dẫn sử dụng

### 1. Chạy trò chơi (Chế độ Console & GUI)
Đây là file khởi đầu chính của dự án:
```bash
python play.py
```
*Lưu ý: Bạn nhập nước đi theo định dạng `hàng cột` (ví dụ: `4 4`).*

### 2. Chạy Benchmark thực nghiệm
Để so sánh hiệu năng giữa Minimax và Alpha-Beta:
```bash
python source/benchmark.py
```
Kết quả sẽ được hiển thị ngay trên màn hình và lưu vào `logs/benchmark_results.csv`.

## 📂 Cấu trúc thư mục
Vui lòng xem chi tiết tại file details.md để hiểu rõ chức năng của từng module và luồng hoạt động của chương trình.

---
*Dự án được thực hiện trong khuôn khổ môn học Cơ sở Trí tuệ nhân tạo - UET.*
