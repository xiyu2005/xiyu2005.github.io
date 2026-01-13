#!/usr/bin/python

import preprocess
import os
if __name__ == '__main__':
    data_dir = os.path.join('..', 'data')
    filename = os.path.join(data_dir, 'ci7b00166_si_001.txt')
    # 建议使用 'realistic' 模式以复现论文结果
    experiment = preprocess.read_txt(filename, 'realistic')

    # --- 执行 pQSAR 完整流程 ---

    # 步骤 1: 训练所有单试验RFR模型, 并保存 (store=True)
    print("--- Building RFR Models (Step 1) ---")
    experiment.build_rfr_models(store=True)
    print("--- RFR Models Built ---")

    # 步骤 2: 基于RFR模型生成“活性谱”特征
    print("--- Generating RFR Features for Compounds (Profile Generation) ---")
    experiment.compound_rfr_features()
    print("--- RFR Features Generated ---")
    
    # 步骤 3: 使用“活性谱”特征训练最终的PLS模型, 并保存 (store=True)
    print("--- Building PLS Models (Step 2) ---")
    experiment.build_pls_models(store=True)
    print("--- PLS Models Built ---")

    print("\n--- Workflow Complete ---")
    #print("RFR model R2 scores:", experiment.r2s)
    #print("PLS model R2 scores:", experiment.pls_r2)