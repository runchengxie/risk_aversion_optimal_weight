import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 添加中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 1. 参数设置
st.title("均值-方差优化可视化")
st.write("""
调整 **风险厌恶系数 (\(\lambda\))** 来查看优化结果如何变化！
""")

# 投资组合参数
mu_risky = 0.08  # 风险资产预期收益
sigma_risky = 0.2  # 风险资产的标准差
r_f = 0.03  # 无风险收益率

# 设置风险厌恶系数范围
lambda_value = st.slider("风险厌恶系数 (\(\lambda\))", 0.1, 10.0, 1.0, step=0.1)

# 2. 定义函数
def optimize_portfolio(mu_risky, sigma_risky, r_f, lambda_value):
    # 计算风险资产的最优权重
    w_risky = (mu_risky - r_f) / (lambda_value * sigma_risky**2)
    w_risky = max(min(w_risky, 1.0), 0.0)  # 保证权重在 [0, 1] 范围内
    w_risk_free = 1 - w_risky  # 无风险资产权重
    return w_risky, w_risk_free

# 计算权重
w_risky, w_risk_free = optimize_portfolio(mu_risky, sigma_risky, r_f, lambda_value)

# 计算目标函数值
portfolio_return = r_f + w_risky * (mu_risky - r_f)
portfolio_risk = w_risky * sigma_risky
objective_value = portfolio_return - (lambda_value / 2) * (portfolio_risk**2)

# 3. 显示结果
st.write(f"**风险资产权重:** {w_risky:.2f}")
st.write(f"**无风险资产权重:** {w_risk_free:.2f}")
st.write(f"**目标函数值:** {objective_value:.4f}")
st.write(f"**组合预期收益:** {portfolio_return:.4f}")
st.write(f"**组合风险 (标准差):** {portfolio_risk:.4f}")

# 4. 可视化
x = np.linspace(0.1, 10, 100)  # 不同的风险厌恶系数
y = [optimize_portfolio(mu_risky, sigma_risky, r_f, l)[0] for l in x]  # 风险资产权重变化

fig, ax = plt.subplots()
ax.plot(x, y, label="风险资产权重", color="blue")
ax.axhline(1.0, color="gray", linestyle="--", label="权重=1.0")
ax.axhline(0.0, color="red", linestyle="--", label="权重=0.0")
ax.set_xlabel("风险厌恶系数 (λ)")
ax.set_ylabel("风险资产权重")
ax.set_title("风险资产权重随 λ 变化")
ax.legend()

# Add vertical line to show current lambda value
ax.axvline(lambda_value, color="green", linestyle=":", label=f"当前 λ = {lambda_value}")
ax.legend()

# Clear previous plots to prevent memory issues
plt.close()

st.pyplot(fig)
