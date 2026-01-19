import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import random
# 假设 DistributionNetworkRiskModel 类保存在 Q1.py 文件中
from Q1 import DistributionNetworkRiskModel, load_data_from_excel  # 假设 load_data_from_excel 也在 Q1.py 中
SEED = 42 # 保证结果可复现
random.seed(SEED)
np.random.seed(SEED)
# 中文显示设置
try:
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
except Exception as e:
    print(f"设置中文字体失败（不影响核心计算）：{e}")


def save_results_to_txt(results_data, filename, folder_name="results"):
    """
    保存结果到txt文件，并组织在独立文件夹中。
    参数:
    results_data: 要保存的结果数据 (可以是DataFrame, dict, 或其他可转换为str的对象)
    filename: 文件名 (例如 "analysis_summary.txt")
    folder_name: 文件夹名称 (例如 "问题2结果")
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    filepath = os.path.join(folder_name, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        if isinstance(results_data, pd.DataFrame):
            f.write(results_data.to_string())
        elif isinstance(results_data, dict):
            for key, value in results_data.items():
                f.write(f"{key}: {value}\n")
        else:
            f.write(str(results_data))
    print(f"结果已保存到: {filepath}")


def analyze_dg_capacity_impact(excel_file_path="A题附件.xlsx", results_base_folder="问题2结果"):
    """
    分析分布式能源容量对系统风险的影响
    以0.3I为步长，从初始容量I增加到3I
    """
    nodes_df_from_excel, lines_df_from_excel = None, None
    if callable(load_data_from_excel) and \
            load_data_from_excel.__code__.co_code != compile("pass", "<string>", "exec").co_code:
        try:
            nodes_df_from_excel, lines_df_from_excel = load_data_from_excel(excel_file_path)
            if nodes_df_from_excel is None or lines_df_from_excel is None:
                print("从Excel加载数据失败，将使用内置的示例数据。")
                raise FileNotFoundError
        except Exception as e:
            print(f"从Excel文件 '{excel_file_path}' 加载数据时出错: {e}。将使用内置示例数据。")
            nodes_df_from_excel, lines_df_from_excel = None, None  # Ensure fallback
    else:
        print("load_data_from_excel 函数为 pass 或不可调用，将使用内置示例数据。")


    # 初始化模型时，确保节点数量与feeder_regions定义匹配
    # (此逻辑应在 DistributionNetworkRiskModel 的 __init__ 或数据加载后执行更佳)
    try:
        # 创建临时模型以访问feeder_regions（这会导致打印"网络模型初始化完成"两次）
        temp_model_for_config = DistributionNetworkRiskModel(nodes_df_from_excel, lines_df_from_excel, n_simulations=1)
        max_node_in_feeders = 0
        if temp_model_for_config.feeder_regions:
            for region_nodes in temp_model_for_config.feeder_regions.values():
                if region_nodes:
                    max_node_in_feeders = max(max_node_in_feeders, max(region_nodes))

        if len(nodes_df_from_excel) < max_node_in_feeders:
            print(
                f"警告: 节点数据行数 {len(nodes_df_from_excel)} 少于馈线定义最大节点 {max_node_in_feeders}。将补充缺失节点。")
            nodes_df_from_excel = pd.concat([
                nodes_df_from_excel,
                pd.DataFrame({'有功P/kW': [0] * (max_node_in_feeders - len(nodes_df_from_excel))})
            ], ignore_index=True)
    except Exception as e_temp_model:
        print(f"创建临时模型检查节点数量时出错: {e_temp_model}。可能影响后续节点相关的操作。")

    # 使用可能已调整的 nodes_df_from_excel 初始化主模型
    model = DistributionNetworkRiskModel(nodes_df_from_excel, lines_df_from_excel, n_simulations=10000)

    # 初始DG容量 I (单个DG点的基准容量)
    base_capacity_per_dg_unit = 300  # kW

    # 设置分布式能源位置
    dg_locations_config = {  # DG ID: {'node': node_id}
        "DG1": {'node': 13}, "DG2": {'node': 18},
        "DG3": {'node': 22}, "DG4": {'node': 29},
        "DG5": {'node': 32}, "DG6": {'node': 39},
        "DG7": {'node': 48}, "DG8": {'node': 59}
    }

    # 容量因子范围
    capacity_factors = [1.0, 1.3, 1.6, 1.9, 2.2, 2.5, 2.8, 3.0]

    results_log = {
        'capacity_factor': [], 'total_dg_capacity_kw': [],
        'load_loss_risk_cost': [], 'overload_risk_cost': [],
        'system_risk_cost': []
    }

    print("\n开始分析不同DG容量下的系统风险演变...")
    for factor in capacity_factors:
        current_total_dg_capacity_all_units = 0
        dg_data_for_model_this_factor = {}  # 构建当前因子下的DG配置
        for dg_id, loc_info in dg_locations_config.items():
            current_dg_unit_capacity = base_capacity_per_dg_unit * factor
            dg_data_for_model_this_factor[dg_id] = {
                'node': loc_info['node'],
                'capacity': current_dg_unit_capacity
            }
            current_total_dg_capacity_all_units += current_dg_unit_capacity

        print(f"\n--- 计算容量因子: {factor:.1f} (总DG容量: {current_total_dg_capacity_all_units:.0f} kW) ---")

        # 设置当前容量的DG数据到模型实例
        # 假设 model.set_dg_data 会正确更新模型内部的DG配置
        if callable(model.set_dg_data) and \
                model.set_dg_data.__code__.co_code != compile("pass", "<string>", "exec").co_code:
            model.set_dg_data(dg_data_for_model_this_factor)
        else:  # 如果 set_dg_data 是 pass, 则手动设置 model.dg_data_config
            model.dg_data_config = dg_data_for_model_this_factor
            print("提示: model.set_dg_data 为 pass, 已手动设置 model.dg_data_config")
            # 需要确保模型内部的图节点DG信息也得到更新（如果set_dg_data原本负责此事）
            for dg_id_iter, info_iter in model.dg_data_config.items():
                node_id_iter, capacity_iter = info_iter.get('node'), info_iter.get('capacity')
                if model.G.has_node(node_id_iter):
                    model.G.nodes[node_id_iter]['dg_nominal_capacity_kw'] = model.G.nodes[node_id_iter].get(
                        'dg_nominal_capacity_kw', 0) + capacity_iter  # 或者直接设为capacity_iter，取决于set_dg_data的逻辑
                    model.G.nodes[node_id_iter]['is_dg_node'] = True

        # 调用模型中的风险计算方法

        # ll_risk_value 是一个浮点数
        # ol_risk_details 是一个字典
        # system_risk_details 是一个字典，包含了ll和ol的详细结果及总和

        # 与调用结构一致
        ll_risk_value = model.calculate_load_loss_risk()
        ol_risk_details = model.calculate_overload_risk()

        # 从详细结果中提取用于记录和打印的数值
        current_ll_risk_cost = ll_risk_value if isinstance(ll_risk_value, (float, int)) else 0.0
        current_ol_risk_cost = ol_risk_details.get('average_total_overload_risk', 0.0) if isinstance(ol_risk_details,
                                                                                                     dict) else 0.0

        # 计算当前的总系统风险成本
        current_system_risk_cost = current_ll_risk_cost + current_ol_risk_cost

        # (或者，如果Q1.py中的calculate_system_risk已正确实现并考虑了上述返回类型)
        # system_risk_details = model.calculate_system_risk()
        # current_ll_risk_cost = system_risk_details.get('load_loss_details', {}).get('average_total_load_loss_risk', 0.0)
        # current_ol_risk_cost = system_risk_details.get('overload_details', {}).get('average_total_overload_risk', 0.0)
        # current_system_risk_cost = system_risk_details.get('total_system_risk_cost', current_ll_risk_cost + current_ol_risk_cost)

        # 记录结果
        results_log['capacity_factor'].append(factor)
        results_log['total_dg_capacity_kw'].append(current_total_dg_capacity_all_units)
        results_log['load_loss_risk_cost'].append(current_ll_risk_cost)
        results_log['overload_risk_cost'].append(current_ol_risk_cost)
        results_log['system_risk_cost'].append(current_system_risk_cost)

        print(f"  失负荷风险成本: {current_ll_risk_cost:.2f}")
        print(f"  过负荷风险成本: {current_ol_risk_cost:.2f}")
        print(f"  系统总风险成本: {current_system_risk_cost:.2f}")

    results_df = pd.DataFrame(results_log)

    if not os.path.exists(results_base_folder):
        os.makedirs(results_base_folder)

    results_df.to_csv(os.path.join(results_base_folder, 'dg_capacity_risk_evolution.csv'), index=False)
    print(f"\n风险演变结果已保存到: {os.path.join(results_base_folder, 'dg_capacity_risk_evolution.csv')}")

    report_summary_lines = [
        "=== 分布式能源容量对系统风险的影响分析报告 ===",
        f"\n1. 基本参数:",
        f"   - 单个DG点初始容量 (I): {base_capacity_per_dg_unit} kW",
        f"   - DG数量: {len(dg_locations_config)}",
        f"   - 容量变化因子范围: {capacity_factors[0]:.1f} 到 {capacity_factors[-1]:.1f}",
        f"\n2. 风险分析结果汇总:",
        results_df.to_string(),
    ]
    if not results_df.empty and 'system_risk_cost' in results_df.columns and results_df[
        'system_risk_cost'].notna().any():
        min_risk_idx = results_df['system_risk_cost'].idxmin()
        min_risk_row = results_df.loc[min_risk_idx]
        report_summary_lines.extend([
            f"\n3. 分析结论:",
            f"   - 最优容量因子 (系统风险最低): {min_risk_row['capacity_factor']:.1f}",
            f"   - 对应总DG容量: {min_risk_row['total_dg_capacity_kw']:.0f} kW",
            f"   - 最小系统风险成本: {min_risk_row['system_risk_cost']:.2f}",
            f"     - 对应失负荷风险成本: {min_risk_row['load_loss_risk_cost']:.2f}",
            f"     - 对应过负荷风险成本: {min_risk_row['overload_risk_cost']:.2f}",
        ])
    else:
        report_summary_lines.append("\n3. 分析结论: 未能确定最优风险点 (结果为空或缺少有效风险数据)。")

    save_results_to_txt("\n".join(report_summary_lines), 'dg_capacity_risk_analysis_summary.txt',
                        folder_name=results_base_folder)

    plt.figure(figsize=(12, 8))
    plt.plot(results_log['capacity_factor'], results_log['load_loss_risk_cost'], 'b-o', label='失负荷风险成本')
    plt.plot(results_log['capacity_factor'], results_log['overload_risk_cost'], 'r-s', label='过负荷风险成本')
    plt.plot(results_log['capacity_factor'], results_log['system_risk_cost'], 'g-^', label='系统总风险成本')
    plt.xlabel('DG容量因子 (I = 初始容量)')
    plt.ylabel('风险成本值')
    plt.title('分布式能源容量对配电系统风险成本的影响演变')
    plt.grid(True)
    plt.legend()
    plt.xticks(capacity_factors)
    plt.savefig(os.path.join(results_base_folder, 'dg_capacity_risk_evolution_plot.png'), dpi=300)
    print(f"风险演变图已保存到: {os.path.join(results_base_folder, 'dg_capacity_risk_evolution_plot.png')}")
    plt.close()

    # (可选) 调用 analyze_feeder_risks
    # print("\n开始分析各馈线风险...")
    # analyze_feeder_risks(model, dg_locations_config, base_capacity_per_dg_unit, capacity_factors, results_base_folder)

    return results_df


def analyze_feeder_risks(model, dg_locations, base_capacity, capacity_factors, results_base_folder="问题2结果"):
    """
    (占位符/简化) 分析不同DG容量下各馈线的风险变化。
    """
    print("警告: analyze_feeder_risks 函数中的馈线风险分配是简化的，仅用于演示结构。")
    feeder_risks_log = {
        'capacity_factor': [], 'feeder1_risk_placeholder': [],
        'feeder2_risk_placeholder': [], 'feeder3_risk_placeholder': []
    }

    for factor in capacity_factors:
        dg_data_for_model = {}
        for dg_id, loc_info in dg_locations.items():
            dg_data_for_model[dg_id] = {'node': loc_info['node'], 'capacity': base_capacity * factor}

        if callable(model.set_dg_data) and \
                model.set_dg_data.__code__.co_code != compile("pass", "<string>", "exec").co_code:
            model.set_dg_data(dg_data_for_model)
        else:
            model.dg_data_config = dg_data_for_model
            # Manually update graph if set_dg_data is pass
            for dg_id_iter, info_iter in model.dg_data_config.items():
                node_id_iter, capacity_iter = info_iter.get('node'), info_iter.get('capacity')
                if model.G.has_node(node_id_iter):
                    model.G.nodes[node_id_iter]['dg_nominal_capacity_kw'] = model.G.nodes[node_id_iter].get(
                        'dg_nominal_capacity_kw', 0) + capacity_iter
                    model.G.nodes[node_id_iter]['is_dg_node'] = True

        system_risk_results = model.calculate_system_risk()
        total_system_risk = system_risk_results.get('total_system_risk_cost', 0.0)

        f1_risk = total_system_risk * 0.40
        f2_risk = total_system_risk * 0.35
        f3_risk = total_system_risk * 0.25

        feeder_risks_log['capacity_factor'].append(factor)
        feeder_risks_log['feeder1_risk_placeholder'].append(f1_risk)
        feeder_risks_log['feeder2_risk_placeholder'].append(f2_risk)
        feeder_risks_log['feeder3_risk_placeholder'].append(f3_risk)

    feeder_risks_df = pd.DataFrame(feeder_risks_log)
    feeder_risks_df.to_csv(os.path.join(results_base_folder, 'feeder_risk_analysis_simplified.csv'), index=False)
    save_results_to_txt(feeder_risks_df, 'feeder_risk_analysis_simplified.txt', folder_name=results_base_folder)

    plt.figure(figsize=(12, 8))
    plt.plot(feeder_risks_log['capacity_factor'], feeder_risks_log['feeder1_risk_placeholder'], 'b-o',
             label='馈线1风险 (占位符)')
    plt.plot(feeder_risks_log['capacity_factor'], feeder_risks_log['feeder2_risk_placeholder'], 'r-s',
             label='馈线2风险 (占位符)')
    plt.plot(feeder_risks_log['capacity_factor'], feeder_risks_log['feeder3_risk_placeholder'], 'g-^',
             label='馈线3风险 (占位符)')
    plt.xlabel('DG容量因子 (I = 初始容量)');
    plt.ylabel('风险值 (占位符)')
    plt.title('分布式能源容量对各馈线风险的影响 (简化占位符)');
    plt.grid(True);
    plt.legend()
    plt.xticks(capacity_factors)
    plt.savefig(os.path.join(results_base_folder, 'feeder_risk_analysis_simplified_plot.png'), dpi=300)
    plt.close()
    print(f"馈线风险分析 (简化版) 结果已保存到 '{results_base_folder}' 文件夹。")


if __name__ == "__main__":
    excel_data_file = "A题附件.xlsx"
    main_results_folder = "问题2分析结果"
    results_dataframe = analyze_dg_capacity_impact(excel_file_path=excel_data_file,
                                                   results_base_folder=main_results_folder)

    if results_dataframe is not None:
        print("\nDG容量影响分析完成。结果摘要:")
        print(results_dataframe[['capacity_factor', 'total_dg_capacity_kw', 'system_risk_cost']])
    else:
        print("\nDG容量影响分析未能生成有效结果。")
