import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import random
# 假设 DistributionNetworkRiskModel 类保存在 Q1.py 文件中
# 并假设 load_data_from_excel 也在其中或可被导入
from Q1 import DistributionNetworkRiskModel, load_data_from_excel

# 中文显示设置
try:
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
except Exception as e:
    print(f"设置中文字体失败（不影响核心计算）：{e}")


def save_results_to_file(data_to_save, filename, folder_name="灵敏度与误差分析结果", format_type="txt"):
    """
    保存结果到文件 (txt 或 csv)，并组织在独立文件夹中。
    参数:
    data_to_save: 要保存的结果数据 (可以是DataFrame, dict, 或其他可转换为str的对象)
    filename: 文件名 (例如 "sensitivity_line_fault_rate.txt")
    folder_name: 文件夹名称
    format_type: "txt" 或 "csv" (csv仅对DataFrame有效)
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    filepath = os.path.join(folder_name, filename)

    if format_type == "csv" and isinstance(data_to_save, pd.DataFrame):
        data_to_save.to_csv(filepath, index=False, encoding='utf-8-sig')
    else:  # Default to txt
        with open(filepath, 'w', encoding='utf-8') as f:
            if isinstance(data_to_save, pd.DataFrame):
                f.write(data_to_save.to_string())
            elif isinstance(data_to_save, dict):
                for key, value in data_to_save.items():
                    f.write(f"{key}: {value}\n")
            else:
                f.write(str(data_to_save))
    print(f"结果已保存到: {filepath}")


def run_sensitivity_analysis_on_parameter(
        base_nodes_df, base_lines_df,
        dg_locations_config, base_dg_capacity_per_unit, fixed_dg_capacity_factor,
        parameter_name_to_vary, parameter_values,
        n_simulations_for_sensitivity, results_base_folder,
        analysis_label  # 用于文件名和图表标题
):
    """
    对模型中的单个参数进行灵敏度分析。

    参数:
    base_nodes_df, base_lines_df: 基础的节点和线路数据。
    dg_locations_config: DG的位置配置。
    base_dg_capacity_per_unit: 单个DG点的基础容量 (I)。
    fixed_dg_capacity_factor: 在本次灵敏度分析中固定的DG容量因子 (例如，分析其他参数时，DG容量保持在 I 或 2I)。
    parameter_name_to_vary (str): DistributionNetworkRiskModel 实例中要改变的属性名。
    parameter_values (list): 要测试的参数值列表。
    n_simulations_for_sensitivity (int): 每次参数变化时运行的蒙特卡洛模拟次数。
    results_base_folder (str): 保存结果的根文件夹。
    analysis_label (str): 用于标识本次分析的标签。
    """
    print(f"\n--- 开始对参数 '{parameter_name_to_vary}' 进行灵敏度分析 ({analysis_label}) ---")

    results_log = {
        'parameter_value': [],
        'load_loss_risk_cost': [],
        'overload_risk_cost': [],  # This will be the total overload risk (curtailment + physical)
        'system_risk_cost': []
    }

    # 准备固定的DG配置 (基于 fixed_dg_capacity_factor)
    fixed_dg_data_for_model = {}
    for dg_id, loc_info in dg_locations_config.items():
        fixed_dg_data_for_model[dg_id] = {
            'node': loc_info['node'],
            'capacity': base_dg_capacity_per_unit * fixed_dg_capacity_factor
        }

    for p_value in parameter_values:
        print(f"  测试参数 '{parameter_name_to_vary}' = {p_value}")

        # 每次参数变化时重新实例化模型，以确保参数正确应用
        # (特别是那些在 __init__ 或 _build_network 中使用的参数)
        model_instance = DistributionNetworkRiskModel(
            base_nodes_df.copy(),  # 使用副本以防意外修改
            base_lines_df.copy(),
            n_simulations=n_simulations_for_sensitivity
        )

        # 设置/修改被分析的参数
        if hasattr(model_instance, parameter_name_to_vary):
            setattr(model_instance, parameter_name_to_vary, p_value)
            # 如果改变的参数影响网络构建（如line_failure_rate_per_km），需要重新构建网络
            # 当前模型在__init__中调用_build_network，所以重新实例化已处理此情况
            if parameter_name_to_vary == 'line_failure_rate_per_km':  # 特殊处理，因为它影响边的属性
                model_instance.G = model_instance._build_network()  # 确保使用更新后的故障率
        else:
            print(f"警告: 参数 '{parameter_name_to_vary}' 不是模型已知属性，跳过此值的设置。")
            # continue # 或者引发错误

        # 设置固定的DG配置
        if callable(model_instance.set_dg_data) and \
                model_instance.set_dg_data.__code__.co_code != compile("pass", "<string>", "exec").co_code:
            model_instance.set_dg_data(fixed_dg_data_for_model)
        else:
            model_instance.dg_data_config = fixed_dg_data_for_model
            # 手动更新图节点 (如果set_dg_data为pass)
            for dg_id_iter, info_iter in model_instance.dg_data_config.items():
                node_id_iter, capacity_iter = info_iter.get('node'), info_iter.get('capacity')
                if model_instance.G.has_node(node_id_iter):
                    model_instance.G.nodes[node_id_iter]['dg_nominal_capacity_kw'] = model_instance.G.nodes[
                                                                                         node_id_iter].get(
                        'dg_nominal_capacity_kw', 0) + capacity_iter
                    model_instance.G.nodes[node_id_iter]['is_dg_node'] = True

        # 运行风险计算
        ll_risk_results = model_instance.calculate_load_loss_risk()
        ol_risk_results = model_instance.calculate_overload_risk()

        current_ll_risk = ll_risk_results.get('average_total_load_loss_risk', 0.0) if isinstance(ll_risk_results,
                                                                                                 dict) else (
            ll_risk_results if isinstance(ll_risk_results, (float, int)) else 0.0)
        current_ol_risk = ol_risk_results.get('average_total_overload_risk', 0.0) if isinstance(ol_risk_results,
                                                                                                dict) else 0.0
        current_sys_risk = current_ll_risk + current_ol_risk

        results_log['parameter_value'].append(p_value)
        results_log['load_loss_risk_cost'].append(current_ll_risk)
        results_log['overload_risk_cost'].append(current_ol_risk)
        results_log['system_risk_cost'].append(current_sys_risk)

        print(f"    系统风险: {current_sys_risk:.2f} (失负荷: {current_ll_risk:.2f}, 过负荷: {current_ol_risk:.2f})")

    results_df = pd.DataFrame(results_log)

    # 保存结果
    folder_path = os.path.join(results_base_folder, f"sensitivity_{parameter_name_to_vary.replace('.', '_')}")
    save_results_to_file(results_df, f"sensitivity_results_{analysis_label}.csv", folder_name=folder_path,
                         format_type="csv")
    save_results_to_file(results_df.describe(), f"sensitivity_summary_{analysis_label}.txt", folder_name=folder_path)

    # 绘制结果
    plt.figure(figsize=(10, 6))
    plt.plot(results_df['parameter_value'], results_df['load_loss_risk_cost'], 'b-o', label='失负荷风险成本')
    plt.plot(results_df['parameter_value'], results_df['overload_risk_cost'], 'r-s', label='过负荷风险成本')
    plt.plot(results_df['parameter_value'], results_df['system_risk_cost'], 'g-^', label='系统总风险成本')
    plt.xlabel(f"参数 '{parameter_name_to_vary}' 的值")
    plt.ylabel('风险成本值')
    plt.title(f"参数 '{parameter_name_to_vary}' 对系统风险的灵敏度 ({analysis_label})")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(folder_path, f"sensitivity_plot_{analysis_label}.png"), dpi=300)
    plt.close()
    print(f"灵敏度分析图表已保存到 '{folder_path}' 文件夹。")
    return results_df


def discuss_error_analysis_approaches(results_base_folder):
    """
    讨论误差分析的方法和考虑因素。
    """
    discussion = [
        "=== 误差分析讨论 ===",
        "误差分析旨在评估模型结果的不确定性和可靠性，其来源可能包括：",
        "1. 输入数据不确定性:",
        "   - 故障率: 通常是统计估计值，本身带有置信区间。可进行参数扰动分析。",
        "   - 负荷预测误差: 实际负荷与模型输入负荷的偏差。",
        "   - DG出力预测误差: DG出力受天气等随机因素影响，预测模型存在误差。",
        "   - 经济参数不确定性: 如停电损失成本、削减成本等可能随市场、政策变化。",
        "   方法: 对关键输入参数赋予概率分布（而非点估计），通过多次模拟（如嵌套蒙特卡洛）传播不确定性，得到风险值的概率分布或置信区间。",
        "",
        "2. 模型结构不确定性 (模型简化带来的误差):",
        "   - 潮流计算简化: 当前模型采用基于辐射状假设的潮流估算，与精确的交流潮流计算结果存在差异，尤其在环网或复杂网络中。",
        "     改进: 与专业潮流工具（如Pandapower）的结果进行对比验证，评估简化模型的适用范围和误差大小。",
        "   - 元件故障模型简化: 如未考虑故障的多种模式、修复时间分布等。",
        "   - DG出力模型简化: 如未使用更精确的Beta分布、Weibull分布或考虑时序相关性。",
        "   - 联络线转供逻辑简化: 实际转供受更多运行约束和保护策略影响。",
        "   方法: 通过与更详细、更精确的模型进行对比，或针对特定简化假设进行专项分析（例如，比较不同潮流计算方法下的风险差异）。",
        "",
        "3. 蒙特卡洛模拟收敛性误差:",
        "   - 模拟次数不足可能导致结果不稳定，不同运行批次结果差异较大。",
        "   方法: 进行收敛性分析，即逐步增加模拟次数 (N_simulations)，观察风险均值和方差的变化。当结果稳定在可接受范围内时，认为模拟已收敛。",
        "   (下面的 'run_simulation_count_stability_analysis' 函数即为此目的)",
        "",
        "4. 参数校准误差:",
        "   - 模型中的许多参数（如故障率、成本系数）需要通过历史数据或行业标准进行校准，校准过程本身可能引入误差。",
        "   方法: 采用历史数据进行回溯测试（back-testing），评估模型的预测能力。",
        "",
        "误差分析的输出:",
        "   - 风险值的置信区间或概率分布。",
        "   - 对模型结果稳健性的评估。",
        "   - 识别对结果不确定性贡献最大的因素，指导数据采集和模型改进的优先方向。",
    ]
    save_results_to_file("\n".join(discussion), "error_analysis_discussion.txt", folder_name=results_base_folder)


def run_simulation_count_stability_analysis(
        base_nodes_df, base_lines_df,
        dg_locations_config, base_dg_capacity_per_unit, fixed_dg_capacity_factor,
        simulation_counts, results_base_folder
):
    """
    分析不同蒙特卡洛模拟次数对风险结果稳定性的影响。
    """
    print("\n--- 开始分析模拟次数对结果稳定性的影响 ---")
    analysis_label = "n_simulations_stability"
    results_log = {
        'n_simulations': [],
        'system_risk_cost_run1': [],
        'system_risk_cost_run2': [],
        'system_risk_cost_run3': [],  # 运行3次以观察波动
        'avg_system_risk': [],
        'std_dev_system_risk': []
    }

    fixed_dg_data_for_model = {}
    for dg_id, loc_info in dg_locations_config.items():
        fixed_dg_data_for_model[dg_id] = {
            'node': loc_info['node'],
            'capacity': base_dg_capacity_per_unit * fixed_dg_capacity_factor
        }

    for n_sim in simulation_counts:
        print(f"  测试模拟次数: {n_sim}")
        current_run_risks = []
        for run_idx in range(3):  # Perform 3 independent runs for each n_sim
            # 重要的：确保每次独立运行有不同的随机序列，除非是想测试种子的效果
            # 如果之前设置了全局种子，这里可能需要重新打乱或不设置
            # random.seed(None) # 取消固定种子，或使用不同的种子
            # np.random.seed(None)

            model_instance = DistributionNetworkRiskModel(
                base_nodes_df.copy(), base_lines_df.copy(), n_simulations=int(n_sim)  # n_sim must be int
            )
            # DG data must be set for each instance
            if callable(model_instance.set_dg_data) and \
                    model_instance.set_dg_data.__code__.co_code != compile("pass", "<string>", "exec").co_code:
                model_instance.set_dg_data(fixed_dg_data_for_model)
            else:
                model_instance.dg_data_config = fixed_dg_data_for_model
                for dg_id_iter, info_iter in model_instance.dg_data_config.items():
                    node_id_iter, capacity_iter = info_iter.get('node'), info_iter.get('capacity')
                    if model_instance.G.has_node(node_id_iter):
                        model_instance.G.nodes[node_id_iter]['dg_nominal_capacity_kw'] = model_instance.G.nodes[
                                                                                             node_id_iter].get(
                            'dg_nominal_capacity_kw', 0) + capacity_iter
                        model_instance.G.nodes[node_id_iter]['is_dg_node'] = True

            system_risk_details = model_instance.calculate_system_risk()
            current_run_risks.append(system_risk_details)

        results_log['n_simulations'].append(n_sim)
        results_log['system_risk_cost_run1'].append(current_run_risks[0])
        results_log['system_risk_cost_run2'].append(current_run_risks[1])
        results_log['system_risk_cost_run3'].append(current_run_risks[2])
        results_log['avg_system_risk'].append(np.mean(current_run_risks))
        results_log['std_dev_system_risk'].append(np.std(current_run_risks))
        print(f"    N_sim={n_sim}: Avg Risk={np.mean(current_run_risks):.2f}, Std Dev={np.std(current_run_risks):.2f}")

    results_df = pd.DataFrame(results_log)
    folder_path = os.path.join(results_base_folder, f"stability_{analysis_label}")
    save_results_to_file(results_df, f"stability_results_{analysis_label}.csv", folder_name=folder_path,
                         format_type="csv")

    plt.figure(figsize=(12, 7))
    plt.errorbar(results_df['n_simulations'], results_df['avg_system_risk'],
                 yerr=results_df['std_dev_system_risk'], fmt='-o', capsize=5,
                 label='平均系统风险 (带标准差)')
    plt.plot(results_df['n_simulations'], results_df['system_risk_cost_run1'], 'r:x', label='运行1风险')
    # plt.plot(results_df['n_simulations'], results_df['system_risk_cost_run2'], 'g--s', label='运行2风险')
    # plt.plot(results_df['n_simulations'], results_df['system_risk_cost_run3'], 'm-.^', label='运行3风险')
    plt.xlabel('蒙特卡洛模拟次数 (N_simulations)')
    plt.ylabel('系统总风险成本值')
    plt.title('模拟次数对系统风险结果稳定性的影响')
    plt.xscale('log')  # X轴使用对数刻度可能更好看
    plt.grid(True, which="both", ls="-")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(folder_path, f"stability_plot_{analysis_label}.png"), dpi=300)
    plt.close()
    print(f"模拟次数稳定性分析图表已保存到 '{folder_path}' 文件夹。")
    return results_df


if __name__ == "__main__":
    # --- 基本配置 ---
    excel_data_file = "A题附件.xlsx"
    main_results_folder = "灵敏度与误差分析结果"
    if not os.path.exists(main_results_folder):
        os.makedirs(main_results_folder)

    # 加载基础数据
    base_nodes_df, base_lines_df = None, None
    if callable(load_data_from_excel) and \
            load_data_from_excel.__code__.co_code != compile("pass", "<string>", "exec").co_code:
        try:
            base_nodes_df, base_lines_df = load_data_from_excel(excel_data_file)
        except Exception as e_load:
            print(f"从Excel文件 '{excel_data_file}' 加载数据时出错: {e_load}。")

    if base_nodes_df is None or base_lines_df is None:
        print(
            "错误: 无法加载基础节点和线路数据，灵敏度分析中止。请确保 'A题附件.xlsx' 存在且格式正确，或者 'load_data_from_excel' 函数已正确实现。")
    else:
        # 确保节点数据行数与馈线区域定义的最大节点号匹配 (与Q2分析类似)
        try:
            _temp_model_config = DistributionNetworkRiskModel(base_nodes_df, base_lines_df, n_simulations=1)
            max_node_in_feeders = 0
            if _temp_model_config.feeder_regions:
                for region_nodes in _temp_model_config.feeder_regions.values():
                    if region_nodes: max_node_in_feeders = max(max_node_in_feeders, max(region_nodes))
            if len(base_nodes_df) < max_node_in_feeders:
                print(
                    f"警告: 负荷数据行数 {len(base_nodes_df)} 少于馈线定义最大节点 {max_node_in_feeders}。补充缺失节点。")
                base_nodes_df = pd.concat(
                    [base_nodes_df, pd.DataFrame({'有功P/kW': [0] * (max_node_in_feeders - len(base_nodes_df))})],
                    ignore_index=True)
        except Exception as e_init_temp:
            print(f"创建临时模型以检查配置时出错: {e_init_temp}")

        # 定义DG配置 (与Q2分析类似，用于设定一个基准场景)
        base_dg_capacity_per_unit_for_sa = 300  # kW
        fixed_dg_capacity_factor_for_sa = 1.0  # 分析其他参数时，DG容量固定为 I
        dg_locations_config_for_sa = {
            "DG1": {'node': 13}, "DG2": {'node': 18}, "DG3": {'node': 22}, "DG4": {'node': 29},
            "DG5": {'node': 32}, "DG6": {'node': 39}, "DG7": {'node': 48}, "DG8": {'node': 59}
        }

        # --- 运行灵敏度分析 ---
        # 示例1: 对线路单位长度故障率进行灵敏度分析
        run_sensitivity_analysis_on_parameter(
            base_nodes_df, base_lines_df,
            dg_locations_config_for_sa, base_dg_capacity_per_unit_for_sa, fixed_dg_capacity_factor_for_sa,
            parameter_name_to_vary='line_failure_rate_per_km',
            parameter_values=np.linspace(0.001, 0.005, 5),  # 例如，从0.001到0.005变化
            n_simulations_for_sensitivity=500,  # 灵敏度分析时用的模拟次数，可适当减少以加快速度
            results_base_folder=main_results_folder,
            analysis_label="线路故障率"
        )

        # 示例2: 对DG削减成本进行灵敏度分析
        run_sensitivity_analysis_on_parameter(
            base_nodes_df, base_lines_df,
            dg_locations_config_for_sa, base_dg_capacity_per_unit_for_sa, fixed_dg_capacity_factor_for_sa,
            parameter_name_to_vary='dg_curtailment_cost_per_kw',
            parameter_values=np.array([0.1, 0.2, 0.3, 0.4, 0.5]),
            n_simulations_for_sensitivity=500,
            results_base_folder=main_results_folder,
            analysis_label="DG削减成本"
        )

        # 示例3: 对线路过载成本系数c_k进行灵敏度分析
        run_sensitivity_analysis_on_parameter(
            base_nodes_df, base_lines_df,
            dg_locations_config_for_sa, base_dg_capacity_per_unit_for_sa, fixed_dg_capacity_factor_for_sa,
            parameter_name_to_vary='line_overload_cost_coefficient_ck',
            parameter_values=np.array([0.5, 1.0, 1.5, 2.0, 2.5]),
            n_simulations_for_sensitivity=500,
            results_base_folder=main_results_folder,
            analysis_label="线路过载成本系数"
        )

        # --- 误差分析讨论与模拟次数稳定性 ---
        discuss_error_analysis_approaches(main_results_folder)

        run_simulation_count_stability_analysis(
            base_nodes_df, base_lines_df,
            dg_locations_config_for_sa, base_dg_capacity_per_unit_for_sa, fixed_dg_capacity_factor_for_sa,
            simulation_counts=[100, 200, 500, 1000, 2000, 5000],  # 测试不同的模拟次数
            results_base_folder=main_results_folder
        )

        print("\n灵敏度与误差分析（初步）完成。")

