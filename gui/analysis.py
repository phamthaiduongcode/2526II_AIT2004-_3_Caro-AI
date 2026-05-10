import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_results(csv_path="logs/benchmark_results.csv"):
    if not os.path.exists(csv_path):
        print("Chưa có dữ liệu benchmark. Hãy chạy tests/benchmark.py trước!")
        return

    df = pd.read_csv(csv_path)
    os.makedirs('experiments', exist_ok=True)
    
    # Tách dữ liệu theo thuật toán
    # Lưu ý: CSV của chúng ta ghi Algorithm theo dạng "Minimax_StateName"
    df['Algo_Type'] = df['Algorithm'].apply(lambda x: 'Minimax' if 'Minimax' in x else 'AlphaBeta')
    df['State'] = df['Algorithm'].apply(lambda x: x.split('_', 1)[1] if '_' in x else x)

    # Vẽ biểu đồ so sánh số Nodes Visited (lấy trung bình nếu có nhiều lần chạy)
    pivot_df = df.groupby(['State', 'Algo_Type'])['Nodes_Visited'].mean().unstack()
    pivot_df.plot(kind='bar', figsize=(10, 6))
    
    plt.title('So sánh số trạng thái đã duyệt (Nodes Visited)')
    plt.ylabel('Số lượng Nodes')
    plt.xlabel('Trạng thái bàn cờ')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('experiments/nodes_comparison.png')
    print("Đã lưu biểu đồ tại experiments/nodes_comparison.png")

if __name__ == "__main__":
    plot_results()