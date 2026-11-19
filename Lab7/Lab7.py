import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data = np.loadtxt("Bank_Customer.csv",skiprows=1,dtype=str,delimiter=',')

'''
Your work
非數值型資料需轉換成數值型資料 (country, gender)
去除掉無意義的特徵類別 (customer_id)
標準化特徵 (StandardScaler)
'''
# 欄位：0 customer_id, 1 credit_score, 2 country, 3 gender, 4 age, 5 tenure,
#       6 balance, 7 products_number, 8 credit_card, 9 active_member,
#       10 estimated_salary, 11 churn

# 1. country：沒有大小順序，用 One-Hot Encoding 拆成多個 0/1 欄位
countries = np.unique(data[:, 2])                      # ['France' 'Germany' 'Spain']
country_onehot = (data[:, 2][:, None] == countries).astype(float)

# 2. gender：只有兩種值，轉成 0/1
gender = (data[:, 3] == "Male").astype(float)[:, None]   # Male=1, Female=0

# 3. 去除 customer_id（第 0 欄），其餘數值欄位轉成 float
numeric = data[:, [1, 4, 5, 6, 7, 8, 9, 10]].astype(float)

features = np.hstack([numeric, country_onehot, gender])
label = data[:, 11].astype(float)[:, None]               # churn：是否流失

# 4. 標準化特徵（label 不做標準化）
features = StandardScaler().fit_transform(features)

pre_data = np.hstack([features, label])

np.savetxt("Bank_Customer_Preprocessed.csv", pre_data, delimiter=",")


from sklearn.linear_model import LogisticRegression
# 決策分類器
clf = LogisticRegression()

'''
Your work
切割 data 為 x_train, x_test, y_train, y_test
請學習 train_test_split 的使用方法
'''
x = pre_data[:, :-1]   # 特徵
y = pre_data[:, -1]    # 標籤 churn

# 70% 訓練、30% 測試；stratify 讓兩邊流失比例一致；random_state 固定結果
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=42, stratify=y)

# 使用訓練集來訓練我們的分類器
clf.fit(x_train, y_train)
# 測試資料集中進行預測
pred = clf.predict(x_test)

#print (pred) # 預測分類，即客戶是否流失
#print (y_test) # 分類
print (str(accuracy_score(pred, y_test)*100 ) + "% ")   # 預測精度
