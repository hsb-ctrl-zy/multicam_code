import os
import pandas as pd

def data_load(file_path,
              file_ext = 'csv',
              output_type = 'concat',
              engine = 'utf-8'):
    # 파일 path에 '/' 추가
    file_path += '/'
    file_list = os.listdir(file_path)

    # 파일 목록이 file_ext와 다른 확장자가 포함되어있을 수 있다.
        # ext에 따라서 filter: 마지막이 file_ext와 같다면 리스트에 유지, 아니면 제거
    
    file_list = [x for x in file_list if x.endswith(file_ext)]
    # 다른 방법
    # file_list2 = []
    # for x in file_list:
        # if x.endswith(file_ext):
            # file_list2.append(x)

    # output_type이 concat이라면 빈 데이터 프레임을 생성
    if output_type == 'concat':
        result = pd.DataFrame()
    elif output_type == 'global':
        # 전역변수에서 사용할 넘버 생성
        vari_cnt = 1
    else:
        raise ValueError('output_type에는 concat, global만 선택이 가능합니다.')

    # 파일을 로드
    for file_name in file_list:
        if file_ext == 'csv':
            df = pd.read_csv(file_path + file_name, encoding=engine)
        elif file_ext == 'json':
            df = pd.read_json(file_path + file_name, encoding=engine)
        elif file_ext == 'xml':
            df = pd.read_xml(file_path + file_name, encoding=engine)
        elif file_ext in ['xlsx', 'xls']:
            df = pd.read_excel(file_path + file_name)
            # read_excel() 함수는 encoding 매개변수가 존재하지 않는다.
        else:
            raise ValueError('file_ext에는 csv, json, xml, excel 확장자만 선택이 가능합니다.')
    
        # output_type에 따라 결합, 전역변수 저장
        if output_type == 'concat':
            result = pd.concat([result, df])
        else:
            globals()[f'df_{vari_cnt}'] = df.copy()
            print(f'df_{vari_cnt} 전역 변수가 생성')
            vari_cnt += 1

    # 결과를 되돌려준다
    try:
        return result
    except:
        print('전역 변수 생성 완료')