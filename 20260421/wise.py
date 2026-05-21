import pandas as pd
import time
from datetime import datetime

code_list = []
# 반복문을 생성하는데 반복 횟수는 명확하지 않다.
while True:
    input_code = input('종목 코드 6자리를 입력하시오. (입력값 종료 시 ENTER)')
    if len(input_code) == 6:
        code_list.append(input_code)
    
    # input_code가 존재하지 않는다면
    if not(bool(input_code)):
        break


now_str = datetime.now().strftime('%y%m%d')

for code in code_list:
    base_url = 'https://comp.wisereport.co.kr/company/c1010001.aspx?cmp_cd='
    df = pd.read_html(base_url+code, encoding='cp949')[3]
    df.to_csv(f"./{code} {now_str}.csv")

    # 시간의 딜레이
    time.sleep(1)