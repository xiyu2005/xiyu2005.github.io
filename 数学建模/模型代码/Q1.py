import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import random
import matplotlib.colors as mcolors
# 中文显示设置
# 请确保您的环境已安装 SimHei 字体，或者替换为您可用的中文字体

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号



def load_data_from_excel(excel_path):
    """
    从指定的Excel文件加载节点和线路数据。

    参数:
    excel_path (str): Excel文件的路径。

    返回:
    tuple: (nodes_df, lines_df)
           nodes_df (pd.DataFrame): 包含节点负荷信息的DataFrame。
                                    预期列: '有功P/kW' (从 "有功P/kW" 读取，"No."列被忽略，顺序决定节点ID)。
           lines_df (pd.DataFrame): 包含线路拓扑信息的DataFrame。
                                    预期列: '编号', '起点', '终点', '长度/km', '电阻/Ω', '电抗/Ω'。
    """

    # 读取表1 (节点数据)
    nodes_df = pd.read_excel(excel_path, sheet_name='表1', usecols=["有功P/kW"])

    # 读取表2 (线路数据)
    lines_df = pd.read_excel(excel_path, sheet_name='表2')
    expected_line_cols = ['编号', '起点', '终点', '长度/km', '电阻/Ω', '电抗/Ω']

    print(f"成功从 '{excel_path}' 加载数据。")
    return nodes_df, lines_df



class DistributionNetworkRiskModel:
    def __init__(self, nodes_data, lines_data,n_simulations=1000):
        """
        初始化配电网风险模型

        参数:
        nodes_data (pd.DataFrame): 包含节点负荷信息的DataFrame, 列: '有功P/kW'
        lines_data (pd.DataFrame): 包含线路拓扑信息的DataFrame, 列: '起点', '终点', '长度/km', '电阻/Ω', '电抗/Ω'
        """
        self.nodes_data = nodes_data
        self.lines_data = lines_data
        self.n_simulations = n_simulations

        # 记录节点的负荷功率
        self.node_loads = {}
        for i, row in nodes_data.iterrows():
            self.node_loads[i + 1] = row['有功P/kW']

        # 定义节点分类
        self.node_categories_map = {}
        residential_nodes = [1, 2, 3, 4, 5, 6, 8, 10, 13, 15, 17, 19, 20, 22, 23, 24, 25, 26, 28, 30, 35, 37, 39, 41,
                             43, 44, 46, 48, 50, 51, 52, 54, 55, 57, 59, 60, 62]
        commercial_nodes = [11, 16, 27, 31, 33, 34, 38, 42, 49, 53, 56]
        government_nodes = [9, 21, 29, 36, 45, 58, 61]  # 政府和机构
        office_nodes = [7, 12, 14, 18, 32, 40, 47]  # 办公和建筑

        for node_id in range(1, len(self.nodes_data) + 1):  # 遍历所有可能的节点ID
            if node_id in residential_nodes:
                self.node_categories_map[node_id] = "居民"
            elif node_id in commercial_nodes:
                self.node_categories_map[node_id] = "商业"
            elif node_id in government_nodes:
                self.node_categories_map[node_id] = "政府机构"
            elif node_id in office_nodes:
                self.node_categories_map[node_id] = "办公建筑"
            else:
                self.node_categories_map[node_id] = "未知类别"  # 为未分类的节点指定默认类别

        # 记录DG的位置和容量
        self.dg_data = {}

        # 系统参数
        self.feeder_capacity = 2200
        self.feeder_current_limit = 220
        self.voltage = 10

        # 故障率
        self.dg_failure_rate = 0.005
        self.load_failure_rate = 0.005
        self.switch_failure_rate = 0.002
        self.line_failure_rate_per_km = 0.002

        # 记录联络开关信息,包括了联络线的额定功率容量
        self.tie_switches = {
            "S13-1": {'nodes': (13, 23), 'capacity_kw': 2200},
            "S29-2": {'nodes': (29, 43), 'capacity_kw': 2200},
            "S62-3": {'nodes': (62, 1), 'capacity_kw': 2200}
        }
        self.default_tie_line_capacity_kw = 1000

        # 记录变电站出线开关
        self.substation_switches = {
            "CB1": 1,
            "CB2": 23,
            "CB3": 43
        }

        # 定义馈线区域
        self.feeder_regions = {
            "Feeder1": list(range(1, 23)),
            "Feeder2": list(range(23, 43)),
            "Feeder3": list(range(43, 63))
        }

        # CDF 参数
        self.interruption_duration_hours = 1.0
        self.use_linear_cdf = True  # 是否启用CDF计算
        self.linear_cdf_weights = {  # 元/kW for the specified duration (e.g., 1 hour)
            "居民": 1.0, "商业": 5.0, "政府机构": 3.0,
            "办公建筑": 4.0, "未知类别": 0.5
        }
        self.nonlinear_cdf_params = {
            "居民": {'a': 0.5, 'b': 1.2, 'c': 10, 't_crit': 2.0},
            "商业": {'a': 2.0, 'b': 1.1, 'c': 50, 't_crit': 1.0},
            "政府机构": {'a': 1.0, 'b': 1.0, 'c': 30, 't_crit': 1.5},
            "办公建筑": {'a': 1.5, 'b': 1.15, 'c': 40, 't_crit': 1.0},
            "未知类别": {'a': 0.1, 'b': 1.0, 'c': 1, 't_crit': 4.0},
        }

        # 过负荷参数设定
        self.dg_curtailment_cost_per_kw = 0.2  # 元/kW (示例)
        self.line_rated_current_a = 220.0  # A, 线路额定电流
        self.line_overload_threshold_factor = 1.1 #过载电流
        self.line_overload_cost_coefficient_ck = 1.0  # 示例 c_k for overload consequence
        self.power_factor_assumed = 0.95  # 用于标准电流计算（如果需要）


        self.G = self._build_network()
        print("网络模型初始化完成 (含节点分类和风险参数)。")



    def _build_network(self):
        """构建配电网络图"""
        G = nx.Graph()

        for i in range(len(self.nodes_data)):
            node_id = i + 1
            node_category = self.node_categories_map.get(node_id, "未知类别")  # 获取节点类别
            G.add_node(node_id,
                       load=self.nodes_data.loc[i, '有功P/kW'],
                       category=node_category)  # 添加类别属性

        for index, row in self.lines_data.iterrows():

            start_node = int(row['起点'])
            end_node = int(row['终点'])
            length = float(row['长度/km'])
            resistance = float(row['电阻/Ω'])
            reactance = float(row['电抗/Ω'])



            G.add_edge(start_node, end_node,
                       id=row.get('编号', f'L{index}'),
                       length=length,
                       resistance_total=resistance,
                       reactance_total=reactance,
                       r_ohm_per_km=resistance / length if length > 0 else np.inf,
                       x_ohm_per_km=reactance / length if length > 0 else np.inf,
                       failure_rate=length * self.line_failure_rate_per_km)

        return G

    def _get_feeder_for_node(self, node_id):
        for name, nodes in self.feeder_regions.items():
            if node_id in nodes: return name
        return None

    def _get_substation_connection_node_for_feeder(self, feeder_name):
        mapping = {"Feeder1": "CB1", "Feeder2": "CB2", "Feeder3": "CB3"}
        cb_name = mapping.get(feeder_name)
        return self.substation_switches.get(cb_name) if cb_name else None

    def _get_feeder_current_status(self, feeder_name, current_G, failed_nodes_set, active_dgs_scenario_capacity):
        """ 计算电流负载, DG, 以及一条馈线的可用容量. """
        feeder_total_load_kw = 0
        feeder_active_dg_kw = 0
        if feeder_name not in self.feeder_regions: return 0, 0, 0  # Load, DG, T_available

        for node_id in self.feeder_regions[feeder_name]:
            if current_G.has_node(node_id) and node_id not in failed_nodes_set:
                feeder_total_load_kw += self.G.nodes[node_id].get('load', 0)  # Use original load for demand
                # Check DG contribution from active DGs
                for dg_id, dg_info in self.dg_data.items():
                    if dg_info['node'] == node_id and active_dgs_scenario_capacity.get(dg_id, 0) > 0:
                        feeder_active_dg_kw += active_dgs_scenario_capacity[dg_id]

        net_load_on_feeder = feeder_total_load_kw - feeder_active_dg_kw
        t_available = 0
        if net_load_on_feeder >= 0:  # Net load or load equals DG
            t_available = self.feeder_capacity - net_load_on_feeder
        else:  # Net generation on this feeder (DG > Load)
            t_available = self.feeder_capacity  # Can supply up to its rated capacity to others

        return feeder_total_load_kw, feeder_active_dg_kw, max(0, t_available)

    def _calculate_scenario_consequence(self, final_unserved_loads_per_node):
        scenario_total_cost = 0
        for node_id, unserved_kw in final_unserved_loads_per_node.items():
            if unserved_kw > 0 and self.G.has_node(node_id):  # Ensure node exists in original graph for category
                category = self.G.nodes[node_id].get('category', "未知类别")
                Lj = unserved_kw
                tj = self.interruption_duration_hours

                if self.use_linear_cdf:
                    Wj = self.linear_cdf_weights.get(category, self.linear_cdf_weights["未知类别"])
                    scenario_total_cost += Wj * Lj
                else:
                    params = self.nonlinear_cdf_params.get(category, self.nonlinear_cdf_params["未知类别"])
                    aj, bj, cj, t_crit_j = params['a'], params['b'], params['c'], params['t_crit']
                    cost_at_node = Lj * (aj * (tj ** bj) + cj * (1 if tj > t_crit_j else 0))
                    scenario_total_cost += cost_at_node
        return scenario_total_cost

    def calculate_load_loss_risk(self):
        """
        计算失负荷风险 (基于蒙特卡洛模拟)
        R_LL = E[C_LL,scenario] = (1/N_sim) * sum(C_LL,i for i in N_sim)
        """
        total_scenario_consequences_sum = 0.0

        for _ in range(self.n_simulations):
            current_G_scenario = self.G.copy()  # 本场景的图表

            # --- 1. 模拟组件故障 ---
            active_dgs_this_scenario = {}  # {dg_id: capacity_kw if active else 0}
            for dg_id, dg_info in self.dg_data.items():
                if random.uniform(0, 1) < self.dg_failure_rate:
                    active_dgs_this_scenario[dg_id] = 0  # DG failed
                else:
                    active_dgs_this_scenario[dg_id] = dg_info['capacity']

            failed_lines_this_scenario = []
            for u, v, data in self.G.edges(data=True):  # 遍历图以获取故障率
                if random.uniform(0, 1) < data['failure_rate']:
                    failed_lines_this_scenario.append((u, v))
            for u, v in failed_lines_this_scenario:  # 应用于情景图
                if current_G_scenario.has_edge(u, v): current_G_scenario.remove_edge(u, v)

            failed_tie_switches_this_scenario = set()
            for ts_name in self.tie_switches.keys():
                if random.uniform(0, 1) < self.switch_failure_rate:
                    failed_tie_switches_this_scenario.add(ts_name)

            failed_substation_switches_this_scenario = set()
            for cb_name in self.substation_switches.keys():
                if random.uniform(0, 1) < self.switch_failure_rate:
                    failed_substation_switches_this_scenario.add(cb_name)

            failed_load_nodes_this_scenario = set()
            for node_id in self.G.nodes():
                is_dg_node = any(dg_info['node'] == node_id for dg_info in self.dg_data.values())
                if not is_dg_node:  # 非dg的负载消耗节点
                    if random.uniform(0, 1) < self.load_failure_rate:
                        failed_load_nodes_this_scenario.add(node_id)

            # --- 2. 网络拓扑分析和初始负载损耗 ---
            active_substation_sources = {self.substation_switches[cb] for cb in self.substation_switches
                                         if cb not in failed_substation_switches_this_scenario
                                         and current_G_scenario.has_node(self.substation_switches[cb])}

            if not active_substation_sources:  # Total blackout if all sources fail
                unserved_loads_dict = {nid: data['load'] for nid, data in self.G.nodes(data=True)
                                       if nid not in failed_load_nodes_this_scenario and data.get('load', 0) > 0}
                total_scenario_consequences_sum += self._calculate_scenario_consequence(unserved_loads_dict)
                continue

            components = list(nx.connected_components(current_G_scenario))
            scenario_initial_total_unserved_kw = 0
            islands_requiring_supply = []  # [{'nodes': set, 'initial_unserved_kw': float, 'original_loads_in_island': dict}]

            main_grid_nodes_connected_to_substation = set()
            for comp in components:
                if any(src_node in comp for src_node in active_substation_sources):
                    main_grid_nodes_connected_to_substation.update(comp)

            for comp_nodes in components:
                is_part_of_main_grid = any(node in main_grid_nodes_connected_to_substation for node in comp_nodes)

                if not is_part_of_main_grid:  # This component is an island
                    island_load_demand_kw = 0
                    island_active_dg_supply_kw = 0
                    original_loads_map_in_island = {}

                    for node_id in comp_nodes:
                        if node_id in failed_load_nodes_this_scenario: continue  # Failed load node has no demand

                        original_load = self.G.nodes[node_id].get('load', 0)
                        if original_load > 0:
                            island_load_demand_kw += original_load
                            original_loads_map_in_island[node_id] = original_load

                        for dg_id, dg_info in self.dg_data.items():
                            if dg_info['node'] == node_id and active_dgs_this_scenario.get(dg_id, 0) > 0:
                                island_active_dg_supply_kw += active_dgs_this_scenario[dg_id]

                    unserved_in_island = max(0, island_load_demand_kw - island_active_dg_supply_kw)
                    if unserved_in_island > 0:
                        scenario_initial_total_unserved_kw += unserved_in_island
                        islands_requiring_supply.append({
                            'nodes': comp_nodes,
                            'initial_unserved_kw': unserved_in_island,
                            'original_loads_in_island': original_loads_map_in_island
                        })

            if scenario_initial_total_unserved_kw == 0:
                total_scenario_consequences_sum += 0.0
                continue

            # --- 3. Load Transfer via Tie Switches ---
            # Calculate available capacity from healthy, connected feeders
            healthy_feeders_supply_capacity = {}  # {feeder_name: T_available_kw}
            for feeder_name_iter in self.feeder_regions.keys():
                sub_conn_node = self._get_substation_connection_node_for_feeder(feeder_name_iter)
                if sub_conn_node and sub_conn_node in main_grid_nodes_connected_to_substation:  # Feeder is healthy and connected
                    _, _, t_avail = self._get_feeder_current_status(feeder_name_iter, current_G_scenario,
                                                                    failed_load_nodes_this_scenario,
                                                                    active_dgs_this_scenario)
                    healthy_feeders_supply_capacity[feeder_name_iter] = t_avail

            final_unserved_loads_dict_scenario = {}  # {node_id: unserved_kw}
            for island in islands_requiring_supply:  # Initialize with all island loads as unserved
                for node_id, load_val in island['original_loads_in_island'].items():
                    final_unserved_loads_dict_scenario[node_id] = load_val

            # Attempt transfer for each island based on its initial_unserved_kw
            for island in sorted(islands_requiring_supply, key=lambda x: x['initial_unserved_kw'],
                                 reverse=True):  # Prioritize larger unserved
                l_fault_for_this_island = island['initial_unserved_kw']
                if l_fault_for_this_island <= 0: continue

                possible_transfers = []  # [{'from_feeder': str, 'T_avail_at_source_feeder': float, 'tie_capacity': float, 'tie_name': str}]
                for ts_name, ts_data in self.tie_switches.items():
                    if ts_name in failed_tie_switches_this_scenario: continue

                    n1, n2 = ts_data['nodes']
                    island_node, healthy_main_grid_node = None, None
                    if n1 in island['nodes'] and n2 in main_grid_nodes_connected_to_substation:
                        island_node, healthy_main_grid_node = n1, n2
                    elif n2 in island['nodes'] and n1 in main_grid_nodes_connected_to_substation:
                        island_node, healthy_main_grid_node = n2, n1

                    if healthy_main_grid_node:
                        source_feeder_name = self._get_feeder_for_node(healthy_main_grid_node)
                        if source_feeder_name and source_feeder_name in healthy_feeders_supply_capacity:
                            t_avail_from_feeder = healthy_feeders_supply_capacity[source_feeder_name]
                            s_tie_max = ts_data.get('capacity_kw', self.default_tie_line_capacity_kw)
                            if t_avail_from_feeder > 0 and s_tie_max > 0:
                                possible_transfers.append({
                                    'from_feeder': source_feeder_name,
                                    'T_avail_at_source_feeder': t_avail_from_feeder,
                                    'tie_capacity': s_tie_max,
                                    'tie_name': ts_name
                                })

                if not possible_transfers: continue

                sum_T_available_via_ties = sum(pt['T_avail_at_source_feeder'] for pt in
                                               possible_transfers)  # This should be sum of min(T_avail_feeder, S_tie)
                # Correct sum_T_available should be sum of what each path can *actually* offer up to its own limits
                sum_potential_supply_for_proportional = sum(
                    min(pt['T_avail_at_source_feeder'], pt['tie_capacity']) for pt in possible_transfers)

                total_transferred_to_this_island = 0
                if sum_potential_supply_for_proportional > 0:
                    for pt_info in sorted(possible_transfers,
                                          key=lambda x: min(x['T_avail_at_source_feeder'], x['tie_capacity']),
                                          reverse=True):  # Prioritize stronger paths
                        # Max this path can offer before proportional split
                        max_this_path_can_give = min(pt_info['T_avail_at_source_feeder'], pt_info['tie_capacity'])

                        # Proportional allocation based on what *this path* can give relative to sum of what *all paths* can give
                        share_of_fault = (
                                                     max_this_path_can_give / sum_potential_supply_for_proportional) * l_fault_for_this_island

                        t_actual_for_this_path = min(max_this_path_can_give, share_of_fault)

                        # Ensure not to transfer more than remaining fault for the island
                        t_actual_for_this_path = min(t_actual_for_this_path,
                                                     l_fault_for_this_island - total_transferred_to_this_island)

                        if t_actual_for_this_path > 0:
                            healthy_feeders_supply_capacity[pt_info['from_feeder']] -= t_actual_for_this_path
                            total_transferred_to_this_island += t_actual_for_this_path

                # Distribute total_transferred_to_this_island among nodes in this island
                if total_transferred_to_this_island > 0:
                    current_total_unserved_in_island = sum(
                        final_unserved_loads_dict_scenario.get(nid, 0) for nid in island['nodes'])
                    if current_total_unserved_in_island > 0:  # Should be same as l_fault_for_this_island initially
                        for node_id_in_island in island[
                            'original_loads_in_island'].keys():  # Iterate only nodes that had load
                            original_node_load = island['original_loads_in_island'][node_id_in_island]
                            # Distribute proportionally to original load that was unserved
                            # The unserved load for this node is currently final_unserved_loads_dict_scenario[node_id_in_island]
                            if final_unserved_loads_dict_scenario.get(node_id_in_island, 0) > 0:
                                proportion_of_island_unserved = final_unserved_loads_dict_scenario[
                                                                    node_id_in_island] / current_total_unserved_in_island
                                reduction_for_node = proportion_of_island_unserved * total_transferred_to_this_island
                                final_unserved_loads_dict_scenario[node_id_in_island] -= reduction_for_node
                                if final_unserved_loads_dict_scenario[
                                    node_id_in_island] < 0.001:  # Threshold for floating point
                                    final_unserved_loads_dict_scenario[node_id_in_island] = 0.0

            # --- 4. Calculate Consequence for this Scenario ---
            scenario_consequence = self._calculate_scenario_consequence(final_unserved_loads_dict_scenario)
            total_scenario_consequences_sum += scenario_consequence

        # --- Final Risk Calculation ---
        if self.n_simulations > 0:
            average_load_loss_risk = total_scenario_consequences_sum / self.n_simulations
        else:
            average_load_loss_risk = 0.0

        return average_load_loss_risk

    def _get_subtree_net_load(self, graph, root_node, current_node, visited_dfs, current_G_nodes_data):
        """ Helper for radial power flow: calculates net load of subtree. """
        visited_dfs.add(current_node)
        node_data = current_G_nodes_data.get(current_node)
        if not node_data: return 0

        # Net load at this specific node
        subtree_net_load = node_data.get('load', 0) - node_data.get('p_dg_actual_kw', 0)

        for neighbor in graph.neighbors(current_node):
            # Check if neighbor is part of the same feeder and not visited (to avoid going back up)
            # This simple DFS assumes a tree structure for the feeder from the root
            if neighbor not in visited_dfs and self._get_feeder_for_node(neighbor) == self._get_feeder_for_node(
                    root_node):
                subtree_net_load += self._get_subtree_net_load(graph, root_node, neighbor, visited_dfs,
                                                               current_G_nodes_data)
        return subtree_net_load

    def calculate_overload_risk(self):
        """
        计算过负荷风险 (基于蒙特卡洛模拟)，结合经济性削减和物理过载。
        返回一个包含详细风险指标的字典。
        """
        total_scenario_curtailment_costs_sum = 0.0
        total_scenario_physical_overload_costs_sum = 0.0
        scenarios_with_any_physical_overload_count = 0

        if not hasattr(self, 'dg_data') or not self.dg_data:
            self.dg_data = {}

        # Initialize accumulators for per-component risk metrics
        aggregated_curtailment_cost_per_feeder = {f_name: 0.0 for f_name in self.feeder_regions.keys()}
        aggregated_physical_overload_cost_per_line = {edge_data['id']: 0.0 for u, v, edge_data in
                                                      self.G.edges(data=True)}
        line_overload_counts = {edge_data['id']: 0 for u, v, edge_data in self.G.edges(data=True)}

        # Denominator for standard current calculation (Amps if Pk in kW, Vl in kV)
        # Not used if using I = 0.1 * Pk(kW)
        # sqrt3_v_pf = np.sqrt(3) * self.voltage * self.power_factor_assumed
        # if abs(sqrt3_v_pf) < 1e-9: sqrt3_v_pf = 1e-9 # Avoid division by zero

        for i_sim in range(self.n_simulations):
            # --- Scenario Setup: Node data for this simulation ---
            current_G_nodes_data_scenario = {
                nid: {'load': data.get('load', 0),
                      'p_dg_nominal_kw': 0.0,  # Nominal output based on random factor
                      'p_dg_actual_kw': 0.0}  # Actual output after curtailment
                for nid, data in self.G.nodes(data=True)
            }

            # Simulate nominal DG outputs for this scenario
            scenario_dg_nominal_outputs_map = {}  # {dg_id: nominal_output_kw}
            for dg_id, dg_config in self.dg_data.items():
                # DG出力波动通过蒙特卡洛模拟生成 (e.g., 50-100% of capacity)
                # This is P_dg,i in S_i = P_dg,i - L_i
                nominal_output = random.uniform(0.5 * dg_config.get('capacity', 0), dg_config.get('capacity', 0))
                scenario_dg_nominal_outputs_map[dg_id] = nominal_output
                node_id_for_dg = dg_config.get('node')
                if node_id_for_dg in current_G_nodes_data_scenario:
                    current_G_nodes_data_scenario[node_id_for_dg]['p_dg_nominal_kw'] += nominal_output
                    # Initially, actual is same as nominal, will be reduced by curtailment
                    current_G_nodes_data_scenario[node_id_for_dg]['p_dg_actual_kw'] += nominal_output

            # --- Economic Optimization Stage (DG Curtailment) ---
            scenario_curtailment_cost_this_sim = 0.0

            for feeder_name in self.feeder_regions.keys():
                feeder_nodes = self.feeder_regions.get(feeder_name, [])
                if not feeder_nodes: continue

                # 1. Calculate S_i = P_dg,i - L_i for this feeder
                feeder_total_nominal_dg_kw = 0
                feeder_total_load_kw = 0
                for node_id in feeder_nodes:
                    node_data = current_G_nodes_data_scenario.get(node_id, {})
                    feeder_total_load_kw += node_data.get('load', 0)
                    feeder_total_nominal_dg_kw += node_data.get('p_dg_nominal_kw', 0)

                surplus_on_feeder_s_i = feeder_total_nominal_dg_kw - feeder_total_load_kw

                if surplus_on_feeder_s_i > 0:  # Feeder has surplus DG
                    # 2. Calculate P_exportable,i
                    exportable_total_from_feeder_i = 0
                    for ts_name, ts_config in self.tie_switches.items():
                        n1_ts, n2_ts = ts_config['nodes']
                        # Check if this tie switch connects the current feeder_name to an adjacent one
                        node_on_this_feeder = None
                        node_on_adj = None
                        if n1_ts in feeder_nodes and self._get_feeder_for_node(
                                n2_ts) != feeder_name and self.G.has_node(n2_ts):
                            node_on_this_feeder, node_on_adj = n1_ts, n2_ts
                        elif n2_ts in feeder_nodes and self._get_feeder_for_node(
                                n1_ts) != feeder_name and self.G.has_node(n1_ts):
                            node_on_this_feeder, node_on_adj = n2_ts, n1_ts

                        if not node_on_adj: continue  # Tie switch not relevant or adj node invalid

                        adj_feeder_name = self._get_feeder_for_node(node_on_adj)
                        if not adj_feeder_name: continue

                        # Adjacent feeder's remaining capacity: 2.2MW - (Load_k - DG_k)
                        # Load_k and DG_k are for the *adjacent* feeder k
                        adj_feeder_load_total_kw = 0
                        adj_feeder_nominal_dg_total_kw = 0  # Use nominal DG of adjacent feeder
                        for adj_node_id in self.feeder_regions.get(adj_feeder_name, []):
                            adj_node_data = current_G_nodes_data_scenario.get(adj_node_id, {})
                            adj_feeder_load_total_kw += adj_node_data.get('load', 0)
                            adj_feeder_nominal_dg_total_kw += adj_node_data.get('p_dg_nominal_kw',
                                                                                0)  # Nominal DG on adj feeder

                        adj_feeder_net_load_for_receiving_calc = adj_feeder_load_total_kw - adj_feeder_nominal_dg_total_kw
                        # If adj_feeder_net_load_for_receiving_calc is negative, it means adj feeder has surplus, cannot receive much.
                        # If positive, it's a net load.
                        # Remaining capacity of adjacent feeder to *receive* power
                        adj_feeder_receiving_capacity = max(0,
                                                            self.feeder_capacity - adj_feeder_net_load_for_receiving_calc)

                        s_k_max_tie_capacity = ts_config.get('capacity_kw', self.default_tie_line_capacity_kw)
                        can_export_via_this_tie = min(s_k_max_tie_capacity, adj_feeder_receiving_capacity)
                        exportable_total_from_feeder_i += can_export_via_this_tie

                    # 3. Calculate P_curtail,i
                    p_curtail_on_feeder_i = max(0, surplus_on_feeder_s_i - exportable_total_from_feeder_i)

                    if p_curtail_on_feeder_i > 0:
                        # 4. Calculate C_OL,i (curtailment cost for this feeder in this scenario)
                        curtailment_cost_on_feeder_i = p_curtail_on_feeder_i * self.dg_curtailment_cost_per_kw
                        scenario_curtailment_cost_this_sim += curtailment_cost_on_feeder_i
                        aggregated_curtailment_cost_per_feeder[
                            feeder_name] += curtailment_cost_on_feeder_i  # Accumulate for averaging

                        # Distribute curtailment P_curtail_on_feeder_i among DGs on this feeder_name
                        if feeder_total_nominal_dg_kw > 0:  # Avoid division by zero
                            for node_id_in_f in feeder_nodes:
                                node_data_in_f = current_G_nodes_data_scenario.get(node_id_in_f)
                                if node_data_in_f and node_data_in_f.get('p_dg_nominal_kw', 0) > 0:
                                    dg_nominal_at_node = node_data_in_f['p_dg_nominal_kw']
                                    # Proportion of curtailment for this DG based on its nominal output
                                    curtailment_for_this_dg_at_node = (
                                                                                  dg_nominal_at_node / feeder_total_nominal_dg_kw) * p_curtail_on_feeder_i

                                    # Reduce p_dg_actual_kw
                                    current_G_nodes_data_scenario[node_id_in_f][
                                        'p_dg_actual_kw'] -= curtailment_for_this_dg_at_node
                                    if current_G_nodes_data_scenario[node_id_in_f]['p_dg_actual_kw'] < 0:
                                        current_G_nodes_data_scenario[node_id_in_f]['p_dg_actual_kw'] = 0.0

            total_scenario_curtailment_costs_sum += scenario_curtailment_cost_this_sim

            # --- Physical Safety Verification Phase (using actual DG outputs after curtailment) ---
            scenario_physical_overload_cost_this_sim = 0.0
            is_any_line_overloaded_this_sim = False
            line_flows_kw_scenario = {}

            for f_name, f_nodes_list in self.feeder_regions.items():
                root_node = self._get_substation_connection_node_for_feeder(f_name)
                if not root_node or not self.G.has_node(root_node): continue
                try:
                    feeder_graph_view = self.G.subgraph(f_nodes_list)
                    if not feeder_graph_view.has_node(root_node): continue
                    dfs_tree_edges = list(nx.dfs_edges(feeder_graph_view, source=root_node))
                    for u_parent, v_child in dfs_tree_edges:
                        visited_for_subtree = set()
                        # _get_subtree_net_load now uses 'p_dg_actual_kw' from current_G_nodes_data_scenario
                        power_flow_on_line = self._get_subtree_net_load(self.G, root_node, v_child,
                                                                        visited_for_subtree,
                                                                        current_G_nodes_data_scenario)
                        line_flows_kw_scenario[tuple(sorted((u_parent, v_child)))] = abs(power_flow_on_line)
                except Exception as e_flow:
                    pass

            for u, v, edge_data in self.G.edges(data=True):
                line_id_tuple_uv = tuple(sorted((u, v)))
                line_actual_id_str = edge_data['id']
                p_k_kw = line_flows_kw_scenario.get(line_id_tuple_uv, 0.0)

                if p_k_kw < 0.01: continue

                # Current calculation as per thesis: I_k = 100 * P_k (MW) = 0.1 * P_k (kW)
                i_k_amps = 0.1 * p_k_kw

                threshold_current = self.line_overload_threshold_factor * self.line_rated_current_a  # 1.1 * I_rated

                if i_k_amps > threshold_current:
                    is_any_line_overloaded_this_sim = True
                    if line_actual_id_str not in line_overload_counts: line_overload_counts[line_actual_id_str] = 0
                    line_overload_counts[line_actual_id_str] += 1

                    # Harm: C_OL,k = c_k * ( (I_k - 1.1*I_rated) / (1.1*I_rated) )^2
                    relative_excess_over_threshold = (
                                                                 i_k_amps - threshold_current) / threshold_current if threshold_current > 0 else (
                        float('inf') if i_k_amps > 0 else 0)
                    consequence_k = self.line_overload_cost_coefficient_ck * (relative_excess_over_threshold ** 2)
                    scenario_physical_overload_cost_this_sim += consequence_k

                    if line_actual_id_str not in aggregated_physical_overload_cost_per_line:
                        aggregated_physical_overload_cost_per_line[line_actual_id_str] = 0.0
                        aggregated_physical_overload_cost_per_line[line_actual_id_str] += consequence_k

            total_scenario_physical_overload_costs_sum += scenario_physical_overload_cost_this_sim
            if is_any_line_overloaded_this_sim:
                scenarios_with_any_physical_overload_count += 1

        # --- Final Risk Calculation ---
        avg_curtailment_cost, avg_physical_overload_cost, overall_P_OL = 0.0, 0.0, 0.0
        avg_curtailment_cost_per_feeder_final = {f: 0.0 for f in self.feeder_regions.keys()}
        avg_physical_overload_cost_per_line_final = {edge_data['id']: 0.0 for u, v, edge_data in
                                                     self.G.edges(data=True)}
        line_overload_frequency_final = {edge_data['id']: 0.0 for u, v, edge_data in self.G.edges(data=True)}

        if self.n_simulations > 0:
            avg_curtailment_cost = total_scenario_curtailment_costs_sum / self.n_simulations
            avg_physical_overload_cost = total_scenario_physical_overload_costs_sum / self.n_simulations
            overall_P_OL = scenarios_with_any_physical_overload_count / self.n_simulations

            avg_curtailment_cost_per_feeder_final = {f: c / self.n_simulations for f, c in
                                                     aggregated_curtailment_cost_per_feeder.items()}
            avg_physical_overload_cost_per_line_final = {l_id: c / self.n_simulations for l_id, c in
                                                         aggregated_physical_overload_cost_per_line.items()}
            line_overload_frequency_final = {l_id: f / self.n_simulations for l_id, f in line_overload_counts.items()}

        return {
            'average_total_overload_risk': avg_curtailment_cost + avg_physical_overload_cost,
            'average_curtailment_cost': avg_curtailment_cost,
            'average_physical_overload_cost': avg_physical_overload_cost,
            'P_OL_system_overload_probability': overall_P_OL,
            'average_curtailment_cost_per_feeder': avg_curtailment_cost_per_feeder_final,
            'average_physical_overload_cost_per_line': avg_physical_overload_cost_per_line_final,
            'line_overload_frequency': line_overload_frequency_final
        }

    def generate_overload_risk_report(self, overload_risk_results):
        """
        生成过负荷风险报告的文本 (简化版)。
        """
        report_lines = ["=" * 25 + " 过负荷风险分析报告 (简化版) " + "=" * 25]
        report_lines.append(f"总模拟次数: {self.n_simulations}")
        report_lines.append("-" * 70)
        report_lines.append(
            f"平均总物理过载成本 (风险): {overload_risk_results.get('average_physical_overload_cost', 0.0):.2f} (成本单位/年)")
        report_lines.append(
            f"系统过载概率 (P_OL - 至少一条线路过载的场景比例): {overload_risk_results.get('P_OL_system_overload_probability', 0.0) * 100:.2f}%")
        report_lines.append("-" * 70)

        # DG削减部分已移除
        # report_lines.append("\n--- DG削减风险详情 (按馈线) ---")
        # report_lines.append("  (在此简化版计算中未考虑DG削减成本)")
        # report_lines.append("-" * 70)

        report_lines.append("\n--- 线路物理过载风险详情 ---")
        cost_per_line = overload_risk_results.get('average_physical_overload_cost_per_line', {})
        freq_per_line = overload_risk_results.get('line_overload_frequency', {})

        overloaded_lines_details = []
        for line_id_str, avg_cost in cost_per_line.items():
            line_display_name = f"线路 {line_id_str}"
            current_freq = freq_per_line.get(line_id_str, 0)
            # Display if there's any cost or any overload occurrence
            if avg_cost > 0.001 or current_freq > 0:  # Use a small threshold for cost display
                overloaded_lines_details.append({
                    'name': line_display_name,
                    'avg_cost': avg_cost,
                    'freq': current_freq * 100
                })

        if not overloaded_lines_details:
            report_lines.append("  在此模拟中未检测到显著的线路物理过载。")
        else:
            # Sort by frequency first, then by average cost for tie-breaking
            sorted_overloaded_lines = sorted(overloaded_lines_details, key=lambda x: (x['freq'], x['avg_cost']),
                                             reverse=True)
            report_lines.append("  高风险线路 (按过载频率和平均成本排序):")
            for detail in sorted_overloaded_lines[:10]:  # Display top 10 or so
                report_lines.append(
                    f"  - {detail['name']}: 平均过载成本 = {detail['avg_cost']:.2f}, 过载频率 = {detail['freq']:.2f}%")
        report_lines.append("-" * 70)

        report_lines.append("\n报告生成完毕。")
        return "\n".join(report_lines)

    def generate_comprehensive_risk_report(self, system_risk_results):
        """
        生成综合风险报告的文本。
        """
        report_lines = ["=" * 30 + " 综合风险评估报告 " + "=" * 30]
        report_lines.append(f"总模拟次数: {self.n_simulations}")
        report_lines.append("=" * 80)
        report_lines.append(
            f"系统总平均风险成本: {system_risk_results.get('total_system_risk_cost', 0.0):.2f} (成本单位/年)")
        report_lines.append("=" * 80)

        # --- 失负荷风险部分 ---
        ll_details = system_risk_results.get('load_loss_details', {})
        report_lines.append("\n" + "=" * 28 + " 失负荷风险详情 " + "=" * 28)
        if not ll_details or ll_details.get('average_total_load_loss_risk', -1) < 0:  # Check if it was calculated
            report_lines.append("  失负荷风险未计算或计算被跳过。")
        else:
            report_lines.append(
                f"平均总失负荷风险成本: {ll_details.get('average_total_load_loss_risk', 0.0):.2f} (成本单位/年)")
            report_lines.append(f"平均未服务功率 (EENS proxy): {ll_details.get('average_EENS_kw', 0.0):.2f} kW")
            # 可以根据 calculate_load_loss_risk 返回的更详细内容在这里添加，例如：
            # report_lines.append(f"  - 主要导致失负荷的故障类型频率: ...")
            # report_lines.append(f"  - 平均孤岛形成频率: ...")
        report_lines.append("=" * 80)

        # --- 过负荷风险部分 (使用 generate_overload_risk_report 的内容) ---
        ol_details = system_risk_results.get('overload_details', {})
        if not ol_details:
            report_lines.append("\n" + "=" * 28 + " 过负荷风险详情 " + "=" * 28)
            report_lines.append("  过负荷风险未计算或计算被跳过。")
        else:
            # Append the already formatted overload report part
            # Create a temporary string from generate_overload_risk_report
            temp_overload_report = self.generate_overload_risk_report(ol_details).splitlines()
            # Skip the header and simulation count from the sub-report if already printed
            report_lines.extend(temp_overload_report[3:])  # Start after the simulation count line of sub-report

        report_lines.append("\n" + "=" * 80)
        report_lines.append("综合报告生成完毕。")
        return "\n".join(report_lines)
    def set_dg_data(self, dg_data):
        """
        设置分布式能源数据
        """
        self.dg_data = dg_data
        for dg_id, info in dg_data.items():
            node_id = info.get('node')
            capacity = info.get('capacity')
            if self.G.has_node(node_id):
                if 'dg_capacity' not in self.G.nodes[node_id]:
                    self.G.nodes[node_id]['dg_capacity'] = 0
                self.G.nodes[node_id]['dg_capacity'] += capacity
                self.G.nodes[node_id]['is_dg_node'] = True
            else:
                print(f"警告: DG {dg_id} 配置的节点 {node_id} 在网络中不存在。")
        print("DG数据已设置。")


    def calculate_system_risk(self):
        """
        计算系统总风险
        """
        # 计算失负荷风险
        load_loss_risk = self.calculate_load_loss_risk()

        # 计算过负荷风险
        overload_risk = self.calculate_overload_risk()

        # 计算系统总风险
        system_risk = load_loss_risk + overload_risk['average_total_overload_risk']

        # 存储详细结果
        self.detailed_results = {
            '失负荷风险': load_loss_risk,
            '过负荷风险': overload_risk,
            '系统总风险': system_risk
        }

        # 保存详细结果
        #self._save_detailed_results()

        return system_risk

    def draw_network_topology(self, save_path="network_topology.png", risk_visualization_data=None):
        # (This function remains largely the same, but will use the simplified risk_visualization_data)
        if not self.G or self.G.number_of_nodes() == 0: print("网络图为空，无法绘制。"); return
        plt.figure(figsize=(20, 16))
        try:
            pos = nx.spring_layout(self.G, k=0.7, iterations=80, seed=42)
        except Exception as e:
            print(f"布局出错: {e}. 尝试随机布局。"); pos = nx.random_layout(self.G)

        node_colors_map = {"居民": "skyblue", "商业": "lightcoral", "政府机构": "lightgoldenrodyellow",
                           "办公建筑": "plum", "未知类别": "lightgray"}
        node_colors = []
        node_sizes = []

        for n in self.G.nodes():
            is_sub = any(n == cb_n for cb_n in self.substation_switches.values())
            is_dg = self.G.nodes[n].get('is_dg_node', False)
            if is_sub:
                node_colors.append('darkred'); node_sizes.append(900)
            elif is_dg:
                node_colors.append('forestgreen'); node_sizes.append(750)
            else:
                node_colors.append(
                    node_colors_map.get(self.G.nodes[n].get('category', "未知类别"), "lightgray")); node_sizes.append(
                    600)

        nx.draw_networkx_nodes(self.G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.95,
                               edgecolors='black', linewidths=0.7)

        edge_colors = []
        edge_widths = []
        default_edge_color = 'dimgray'
        default_edge_width = 1.5
        all_risk_values_for_norm = []

        if risk_visualization_data and 'average_physical_overload_cost_per_line' in risk_visualization_data:
            line_risks = risk_visualization_data['average_physical_overload_cost_per_line']
            # Use line_overload_frequency for coloring if cost is often zero but frequency is high
            # Or, use a combined metric. For now, sticking to cost for color intensity.
            all_risk_values_for_norm = [r for r in line_risks.values() if
                                        r > 0.001]  # Only consider non-negligible risks for scaling

            norm = None
            cmap = None
            if all_risk_values_for_norm:
                min_risk, max_risk = min(all_risk_values_for_norm), max(all_risk_values_for_norm)
                if abs(max_risk - min_risk) < 1e-6: max_risk = min_risk + 0.01  # Avoid min=max for norm
                norm = mcolors.Normalize(vmin=min_risk, vmax=max_risk, clip=True)
                try:
                    cmap = plt.colormaps.get_cmap('YlOrRd')
                except AttributeError:
                    cmap = plt.cm.get_cmap('YlOrRd')

            for u, v, edge_data_nx in self.G.edges(data=True):
                line_actual_id = edge_data_nx['id']
                risk_val = line_risks.get(line_actual_id, 0.0)
                if risk_val > 0.001 and norm and cmap:
                    edge_colors.append(cmap(norm(risk_val)))
                    # Make width also proportional to normalized risk or frequency
                    freq_val_norm = risk_visualization_data.get('line_overload_frequency', {}).get(line_actual_id, 0)
                    edge_widths.append(
                        1.0 + 3.0 * (norm(risk_val) + freq_val_norm) / 2.0)  # Example combined metric for width
                else:
                    edge_colors.append(default_edge_color)
                    edge_widths.append(default_edge_width)
        else:
            edge_colors = [default_edge_color] * self.G.number_of_edges()
            edge_widths = [default_edge_width] * self.G.number_of_edges()

        nx.draw_networkx_edges(self.G, pos, alpha=0.7, edge_color=edge_colors, width=edge_widths)

        labels = {n: f"{n}\n{d.get('load', 0)}kW" + (f"\nDG:{d.get('dg_nominal_capacity_kw', 0)}kW" if d.get(
            'is_dg_node') else "") + f"\n({d.get('category', 'N/A')})" for n, d in self.G.nodes(data=True)}
        nx.draw_networkx_labels(self.G, pos, labels=labels, font_size=5,
                                bbox=dict(facecolor='white', alpha=0.7, pad=0.1, edgecolor='none'))

        plt.title('配电网拓扑结构与过负荷风险可视化 (简化版)', fontsize=40)
        plt.axis('off');
        plt.tight_layout()

        if risk_visualization_data and all_risk_values_for_norm and cmap and norm:
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            cbar = plt.colorbar(sm, orientation="horizontal", fraction=0.03, pad=0.02, aspect=30)
            cbar.set_label('线路平均物理过载成本风险 (成本单位/年)', fontsize=10)
            cbar.ax.tick_params(labelsize=8)

        try:
            folder = os.path.dirname(save_path)
            if folder and not os.path.exists(folder): os.makedirs(folder)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"网络拓扑图已保存到: {save_path}")
        except Exception as e:
            print(f"保存图像失败: {e}")
        # plt.show()


# --- 模型使用示例 ---
if __name__ == "__main__":
    excel_file_path = "A题附件.xlsx"
    nodes_df, lines_df = load_data_from_excel(excel_file_path)

    if nodes_df is not None and lines_df is not None:
        # 临时的DistributionNetworkRiskModel实例以获取feeder_regions配置
        _temp_model = DistributionNetworkRiskModel(nodes_df, lines_df)
        max_node_in_feeders = 0
        if _temp_model.feeder_regions:  # 确保feeder_regions不为空
            for region_nodes in _temp_model.feeder_regions.values():
                if region_nodes:  # 确保region_nodes列表不为空
                    max_node_in_feeders = max(max_node_in_feeders, max(region_nodes))

        if len(nodes_df) < max_node_in_feeders:
            print(
                f"警告: 从Excel加载的负荷数据只有 {len(nodes_df)} 行，但馈线区域定义涉及到了节点 {max_node_in_feeders}。")
            missing_rows = max_node_in_feeders - len(nodes_df)
            if missing_rows > 0:
                print(f"为缺失的 {missing_rows} 个节点补充默认负荷为0。")
                nodes_df = pd.concat([nodes_df, pd.DataFrame({'有功P/kW': [0] * missing_rows})], ignore_index=True)

        model = DistributionNetworkRiskModel(nodes_df, lines_df,n_simulations=1000)  # 主要的实例化

        dg_example_data = {
            "DG1": {'node': 16, 'capacity': 300},
            "DG2": {'node': 22, 'capacity': 300},
            "DG3": {'node': 32, 'capacity': 300},
            "DG4": {'node': 35, 'capacity': 300},
            "DG5": {'node': 39, 'capacity': 300},
            "DG6": {'node': 48, 'capacity': 300},
            "DG7": {'node': 52, 'capacity': 300},
            "DG8": {'node': 55, 'capacity': 300},

        }
        model.set_dg_data(dg_example_data)

        results_folder = "problem1_results_risk_calc"
        if not os.path.exists(results_folder): os.makedirs(results_folder)

        model.draw_network_topology(save_path=os.path.join(results_folder, "network_topology_for_risk.png"))

        print("\n开始计算失负荷风险...")
        load_loss_risk_result = model.calculate_load_loss_risk()
        print(f"计算得到的平均失负荷风险 (R_LL): {load_loss_risk_result:.2f} (成本单位/年)")

        print("\n开始计算过负荷风险...")
        overload_risk_result = model.calculate_overload_risk()
        print(f"计算得到的平均过负荷风险 (R_OL): {overload_risk_result['average_total_overload_risk']:.2f} (成本单位/年)")

        print("\n生成过负荷风险报告...")
        report_content = model.generate_overload_risk_report(overload_risk_result)
        report_file_path = os.path.join(results_folder, "overload_risk_report.txt")
        with open(report_file_path, "w", encoding="utf-8") as f_report:
            f_report.write(report_content)
        print(f"过负荷风险报告已保存到: {report_file_path}")
        # print("\n--- 报告内容 ---")
        # print(report_content) # Optionally print report to console

        print(f"系统总风险为{load_loss_risk_result+overload_risk_result['average_total_overload_risk']:.2f}")
        print("\n生成风险可视化拓扑图...")
        model.draw_network_topology(
            save_path=os.path.join(results_folder, "network_topology_with_overload_risk.png"),
            risk_visualization_data=overload_risk_result
        )


    else:
        print("由于数据加载失败，模型初始化和风险计算未能执行。")


