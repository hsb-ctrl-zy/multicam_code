import numpy as np

def outlier_iqr(data, *cols, n = 1.5, drop = False):
    df = data.copy()
    whis_dict = {}

    for col in cols:
        try:
            q_1, q_3 = np.percentile(df[col], [25, 75])
            iqr = q_3 - q_1

            upper_whis = q_3 + (n * iqr)
            lower_whis = q_1 - (n * iqr)

            print(f'''
                지정된 컬럼의 이름: {col},
                상단 경계: {upper_whis},
                하단 경계 {lower_whis}''')

            upper_flag = df[col] > upper_whis
            lower_flag = df[col] < lower_whis
            upper_n = len( df.loc[upper_flag, ] )
            lower_n = len( df.loc[lower_flag, ] )
            print(f'상단 경계를 벗어나는 데이터의 개수: {upper_n}, 하단 경계를 벗어나는 데이터의 개수: {lower_n}')
            whis_df = df.loc[upper_flag|lower_flag, ]
            whis_dict[col] = whis_df

            if drop:
                df = df.loc[ ~(upper_flag | lower_flag), ]
            else:
                df.loc[upper_flag, col] = upper_whis
                df.loc[lower_flag, col] = lower_whis

        except Exception as e:
            print(f'Error: {e}')
    
    return df, whis_dict