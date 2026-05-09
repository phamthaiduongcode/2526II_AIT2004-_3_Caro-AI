# Chi tiết kỹ thuật Dự án Caro AI

Tài liệu này cung cấp cái nhìn sâu hơn về cấu trúc, thuật toán và các lưu ý quan trọng dành cho nhà phát triển.

## 1. Chi tiết các Module

### `source/gomoku.py` (Logic bàn cờ)
- **Lớp `Board`**: Quản lý trạng thái bàn cờ bằng mảng 2 chiều.
- **Luật chơi**: Thắng khi có **đúng 4 quân liên tiếp** theo bất kỳ hướng nào (ngang, dọc, chéo). 
- **Không xét luật chặn hai đầu**: Đây là yêu cầu đặc thù của đề bài.
- **`get_legal_moves`**: Tối ưu hóa bằng cách chỉ xét các ô trống trong bán kính 2 ô xung quanh các quân đã đánh để giảm không gian trạng thái.

### `source/AI.py` (Bộ não AI)
- **`minimax`**: Thuật toán tìm kiếm đệ quy cơ bản.
- **`alpha_beta`**: Phiên bản cải tiến giúp cắt nhánh các vùng không gian không cần thiết khi $\beta \le \alpha$.
- **Hàm đánh giá (Heuristic)**: 
    - Sử dụng kỹ thuật "cửa sổ trượt" (Sliding Window) kích thước 4.
    - Gán điểm theo trọng số mũ (100, 1000, 100000) dựa trên số lượng quân cờ trong cửa sổ.
    - Ưu tiên phòng thủ bằng cách nhân hệ số cho điểm số của đối thủ.
- **Move Ordering**: Sắp xếp các nước đi ưu tiên từ tâm bàn cờ ra ngoài để tối ưu hóa việc cắt nhánh sớm cho Alpha-Beta.

### `source/utils.py` (Tiện ích)
- **`GameLogger`**: Ghi lại lịch sử thực nghiệm (Algorithm, Depth, Nodes, Time, Score) vào file CSV trong thư mục `logs/`. Dữ liệu này được dùng để vẽ biểu đồ so sánh.

### `source/benchmark.py` (Thực nghiệm)
- Chứa 5 kịch bản (Test Cases) từ bàn cờ trống đến các thế cờ hiểm.
- Dùng để chứng minh tính đúng đắn: Alpha-Beta phải trả về cùng kết quả với Minimax nhưng duyệt ít trạng thái hơn.

## 2. Luồng hoạt động của chương trình (Flow)

1. **Khởi tạo**: `play.py` khởi tạo đối tượng `Board` và `CaroAI`.
2. **Vòng lặp chính**:
    - Nếu là lượt Người: Nhận input -> `Board.make_move()` -> Kiểm tra thắng/thua.
    - Nếu là lượt AI:
        - `AI.get_move()` được gọi.
        - Thuật toán (Minimax/Alpha-Beta) duyệt cây trạng thái đến độ sâu quy định.
        - Mỗi bước thử nghiệm dùng `Board.make_move()` và `Board.undo_move()`.
        - Trả về nước đi tốt nhất.
    - **Ghi Log**: Thông tin nước đi được `GameLogger` lưu lại.
3. **Kết thúc**: Hiển thị kết quả thắng/thua hoặc hòa.

## 3. Các vấn đề Dev cần nắm vững (FAQ)

### Tại sao AI chạy chậm?
- Kiểm tra `depth` (độ sâu). Với Python, độ sâu 3-4 là giới hạn cho bàn cờ lớn nếu không tối ưu tốt.
- Kiểm tra hàm `get_legal_moves`. Nếu không giới hạn vùng tìm kiếm, số node sẽ tăng theo hàm mũ $O(b^d)$.

### Tại sao Alpha-Beta không nhanh hơn Minimax?
- Alpha-Beta chỉ hiệu quả nhất khi tìm thấy nước đi tốt nhất sớm. Nếu không có **Move Ordering** (sắp xếp nước đi), số node có thể vẫn tương đương Minimax.

### Lưu ý về luật "4 quân liên tiếp"
- Logic `check_win` hiện tại sẽ dừng ngay khi đếm đủ 4. Nếu trong thực tế người chơi đánh thành 5 quân, thuật toán vẫn ghi nhận là thắng tại quân thứ 4. Đây là điểm cần lưu ý khi giải trình với giảng viên về subset của chuỗi thắng.

### Cách đọc Log thực nghiệm
- Mở `logs/benchmark_results.csv` bằng Excel hoặc dùng thư viện Pandas để vẽ biểu đồ.
- Trọng tâm phân tích: Cột `Nodes_Visited` của Alpha-Beta phải nhỏ hơn đáng kể so với Minimax.

## 4. Các trường hợp biên (Edge Cases)
- **Bàn cờ đầy**: Hàm `check_win` trả về -1 (Hòa).
- **Nước đi đầu tiên**: AI được lập trình đánh vào giữa bàn cờ nếu là người đi đầu.
- **Chặn đối thủ**: Heuristic được tinh chỉnh để ưu tiên chặn chuỗi 3 của đối thủ hơn là tạo chuỗi 2 cho mình.