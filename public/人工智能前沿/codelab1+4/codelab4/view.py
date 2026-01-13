import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def analyze_and_visualize_results():
    """
    Loads, analyzes, and visualizes the performance results from RFR, PLS, and PLS (Max2) models.
    """
    # --- 1. 文件路径定义 ---
    # 确保这些CSV文件与本脚本在同一个目录下
    rfr_file = 'rfr_r2.csv'
    pls_file = 'pls_r2.csv'
    max2_file = 'pls_max2_r2_scores.csv'

    # 检查文件是否存在
    files_to_check = [rfr_file, pls_file, max2_file]
    for f in files_to_check:
        if not os.path.exists(f):
            print(f"错误：找不到文件 '{f}'。请确保所有CSV文件都在脚本所在的目录中。")
            return

    # --- 2. 数据加载与预处理 ---
    try:
        # 加载RFR基础模型结果
        rfr_df = pd.read_csv(rfr_file, header=0, names=['Assay_ID', 'R2_Score'])
        
        # 加载PLS（全谱）模型结果
        pls_df = pd.read_csv(pls_file, header=0, names=['Assay_ID', 'R2_Score'])
        
        # 加载PLS（Max2优化）模型结果，并剔除无效值
        max2_df_raw = pd.read_csv(max2_file, header=0, names=['Assay_ID', 'R2_Score'])
        max2_df = max2_df_raw[max2_df_raw['R2_Score'] != -999].copy()
        
        print("数据加载成功！")

    except Exception as e:
        print(f"读取CSV文件时出错: {e}")
        print("请确保CSV文件格式正确：第一行为表头，第二行开始为数据，第一列为模型名，第二列为R²值。")
        return

    # 提取R²分数用于分析
    rfr_scores = rfr_df['R2_Score']
    pls_scores = pls_df['R2_Score']
    max2_scores = max2_df['R2_Score']

    # --- 3. 性能指标统计分析 ---
    results = {
        'RFR (Baseline)': rfr_scores,
        'PLS (Full Profile)': pls_scores,
        'PLS (Max2 Optimized)': max2_scores
    }

    print("\n" + "="*50)
    print("                模型性能统计分析")
    print("="*50)
    for name, scores in results.items():
        print(f"\n方法: {name}")
        print("-" * (len(name) + 7))
        print(f"  有效模型总数: {len(scores)}")
        print(f"  R² 中位数:    {scores.median():.4f}")
        print(f"  R² 平均值:    {scores.mean():.4f}")
        print(f"  成功模型数 (R² > 0.3): { (scores > 0.3).sum() }")

    # --- 4. 可视化 ---

    # 图一：累积分布图 (与论文档案风格类似)
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(12, 8))

    for name, scores in results.items():
        # 降序排列R²值
        sorted_scores = np.sort(scores)[::-1]
        plt.plot(np.arange(len(sorted_scores)), sorted_scores, marker='.', linestyle='-', label=f'{name} ({len(scores)} models)')

    # 添加参考线
    plt.axhline(y=0.3, color='r', linestyle='--', label='Success Threshold (R² = 0.3)')
    plt.axhline(y=0.0, color='gray', linestyle=':', label='Baseline (R² = 0.0)')

    plt.title('pQSAR Model Performance Comparison (Cumulative Distribution)', fontsize=16)
    plt.xlabel('Number of Models (Ranked by Performance)', fontsize=12)
    plt.ylabel('R² Score', fontsize=12)
    plt.legend(fontsize=10)
    plt.ylim(-1, 1) # 设定Y轴范围以便观察
    
    # 保存图像
    cumulative_plot_path = 'pQSAR_Performance_Cumulative.png'
    plt.savefig(cumulative_plot_path)
    print(f"\n累积分布图已保存至: {cumulative_plot_path}")
    plt.show()


    # 图二：箱形图 (Box Plot)
    plt.figure(figsize=(10, 7))
    
    data_to_plot = [rfr_scores, pls_scores, max2_scores]
    labels = ['RFR (Baseline)', 'PLS (Full Profile)', 'PLS (Max2 Optimized)']
    
    plt.boxplot(data_to_plot, labels=labels, patch_artist=True, showfliers=False) # showfliers=False 隐藏异常值点，使图形更清晰
    
    plt.title('Distribution of R² Scores by Model Type', fontsize=16)
    plt.ylabel('R² Score', fontsize=12)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.axhline(y=0.0, color='gray', linestyle=':')
    
    # 保存图像
    boxplot_path = 'pQSAR_Performance_Boxplot.png'
    plt.savefig(boxplot_path)
    print(f"箱形图已保存至: {boxplot_path}")
    plt.show()


if __name__ == '__main__':
    analyze_and_visualize_results()