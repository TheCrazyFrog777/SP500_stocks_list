import pandas as pd
import requests
from io import StringIO

#取得上市公司股票清單
res = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
html_content = StringIO(res.text)
df = pd.read_html(html_content)[0]

# 設定column名稱
df.columns = df.iloc[0]
# 刪除第一行
df = df.iloc[2:]

# 先移除row，再移除column，超過三個NaN則移除
df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)

df[['Ticker', '公司名稱']] = df['有價證券代號及名稱'].str.split('　', expand=True)

# 刪除不再需要的 "原始欄位"
df = df.drop(columns=['有價證券代號及名稱'])

# 重新排列欄位順序，將 'Ticker' 和 '公司名稱' 移到最左邊
df = df[['Ticker', '公司名稱'] + [col for col in df.columns if col not in ['Ticker', '公司名稱']]]

# 設定index
df = df.set_index("Ticker")

print(df)

df.to_csv("TW_stocks.csv", encoding="utf-8-sig")