import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 数据集路径引入（相关性分析后选出五个一级自变量：'出口货物', '零售', '就业情况', '科研投入', '高新企业数量'）
data_dir = os.path.join(os.getcwd(), 'data')
economy_exit_factor_dir = os.path.join(data_dir, '出口货物')
economy_retail_factor_dir = os.path.join(data_dir, '零售')
population_emolpyment_factor_dir = os.path.join(data_dir, '就业情况')
SciTech_sciinput_factor_dir = os.path.join(data_dir, '科研投入')
SciTech_scifirm_factor_dir = os.path.join(data_dir, '高新企业数量')

#以年为索引，创建pearson系数最大的五个因素的数据集
merged_data = pd.merge(pd.merge(pd.merge(pd.merge(economy_exit_factor[['Year', 'economy_exit_factor']], # 定义出口货物数据列名为'economy_exit_factor'
                                          economy_retail_factor[['Year', 'economy_retail_factor']], # 定义零售数据列名为'economy_retail_factor'
                                          on='Year'),
                                 population_employment_factor[['Year', 'population_employment_factor']], # 定义就业情况数据列名为'population_employment_factor'
                                 on='Year'),
                        SciTech_sciinput_factor[['Year', 'SciTech_sciinput_factor']], # 定义科研投入数据列名为'SciTech_sciinput_factor'
                        on='Year'),
                       SciTech_scifirm_factor[['Year', 'SciTech_scifirm_factor']], # 定义高新企业数量数据列名为'SciTech_scifirm_facto'
                       on='Year')

# 加载GDP数据
gdp_data = pd.read_csv(os.path.join(data_dir, 'GDP'))
merged_data = pd.merge(merged_data, gdp_data[['Year', 'GDP']], on='Year')

# 选择自变量（因素）和因变量（GDP）
X = merged_data[['economy_exit_factor','economy_retail_factor','population_employment_factor','SciTech_sciinput_factor','SciTech_scifirm_factor']]  # 自变量（因素）
y = merged_data['GDP']  # 因变量（GDP）

# 将数据转换为DataFrame格式（便于查看和处理）
columns = ['economy_exit_factor', 'economy_retail_factor', 'population_employment_factor'，'SciTech_sciinput_factor', 'SciTech_scifirm_factor']
X_df = pd.DataFrame(X, columns=columns)
y_df = pd.Series(y, name='Target')

# 将数据集拆分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建线性回归模型并训练
model = LinearRegression()
model.fit(X_train, y_train)

# 使用模型进行预测
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# 评估模型性能（使用均方误差MSE和决定系数R^2评估拟合度）
train_mse = mean_squared_error(y_train, y_pred_train)
test_mse = mean_squared_error(y_test, y_pred_test)
train_r2 = r2_score(y_train, y_pred_train)
test_r2 = r2_score(y_test, y_pred_test)

print(f"训练集MSE: {train_mse}")
print(f"测试集MSE: {test_mse}")
print(f"训练集R^2: {train_r2}")
print(f"测试集R^2: {test_r2}")

# 输出模型的系数和截距
print(f"系数: {model.coef_}")
print(f"截距: {model.intercept_}")
