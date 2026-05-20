import pandas as pd

# ==========================================
# 1. 生成 人卡qc 报表: idcard_qc_M-2-1.csv
# ==========================================
data_idcard = {
    "backtrack_dt": ["2024-07-31", "2024-08-31", "2024-09-30"],
    "sample_count": [10000, 12000, 15000],
    "total_unique_cards": [35000, 43000, 54000],
    "avg_card_count": [3.5, 3.58, 3.6],
    "avg_eff_card_count": [2.8, 2.9, 3.0],
    "max_card_count": [25, 32, 28],
    "min_card_count": [0, 0, 0],
    "bucket_0_cnt": [500, 600, 700],
    "bucket_1_3_cnt": [4500, 5200, 6300],
    "bucket_4_10_cnt": [4200, 5100, 6600],
    "bucket_10_plus_cnt": [800, 1100, 1400],
    "p10_card": [1, 1, 1],
    "p25_card": [2, 2, 2],
    "p50_card": [3, 4, 4],
    "p75_card": [6, 6, 7],
    "p90_Card": [11, 12, 12]
}
df_idcard = pd.DataFrame(data_idcard)
df_idcard.to_csv("idcard_qc_M-2-1.csv", index=False, encoding="utf-8-sig")


# ==========================================
# 2. 生成 产品qc特征表1: multi_key_vars_qc1.csv
# ==========================================
# 数值型特征有统计值，文本/布尔型特征统计值留空 (符合实际生产的智能体风控检测)
data_vars_qc1 = {
    "column": ["mchntBussNmValid", "mchntBussAddrValid", "mchntNmEntConsistent", "total_loan_amt"],
    "non_null_count": [10000, 9800, 9500, 8500],
    "mean": ["", "", "", 154500.25],
    "variance": ["", "", "", 25004500.0],
    "stddev": ["", "", "", 5000.45],
    "min": ["", "", "", 1000.0],
    "max": ["", "", "", 1000000.0],
    "q_5": ["", "", "", 5000.0],
    "q_25": ["", "", "", 45000.0],
    "q_50": ["", "", "", 120000.0],
    "q_75": ["", "", "", 250000.0],
    "q_95": ["", "", "", 600000.0],
    "var_nm": ["mchnt_buss_nm_valid", "mchnt_buss_addr_valid", "mchnt_nm_ent_consistent", "total_loan_amt"],
    "chn_nm": ["商户经营名称验证", "商户经营地址验证", "商户名称企业一致性", "总借款金额"]
}
df_vars_qc1 = pd.DataFrame(data_vars_qc1)
df_vars_qc1.to_csv("multi_key_vars_qc1.csv", index=False, encoding="utf-8-sig")


# ==========================================
# 3. 生成 产品qc特征表2: multi_key_vars_qc2.csv
# ==========================================
data_vars_qc2 = {
    "backtrack_dt": ["2024-07-31", "2024-08-31", "2024-09-30"],
    "non_empty_count": [9500, 11400, 14250]
}
df_vars_qc2 = pd.DataFrame(data_vars_qc2)
df_vars_qc2.to_csv("multi_key_vars_qc2.csv", index=False, encoding="utf-8-sig")

print("三个测试 CSV 文件已全部生成完成！")