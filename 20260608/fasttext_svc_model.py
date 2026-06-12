import pandas as pd
import numpy as np
from konlpy.tag import Komoran
from gensim.models import FastText
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

# 1. 토큰화 함수 설정 (Komoran 인스턴스를 외부에서 생성하여 속도 향상)
komoran = Komoran()
def tokenize(text):
    if not isinstance(text, str):
        return []
    allow_pos = ['NNP', 'NNG', 'VV', 'VA', 'SL', 'MAG']
    try:
        # 형태소 분석 후 허용된 품사만 추출
        return [word for word, pos in komoran.pos(text) if pos in allow_pos]
    except Exception:
        # 분석 실패 시 단순 공백 분할
        return text.split()

# 2. 문장 벡터 변환 함수 (단어 벡터의 평균 이용)
def get_sentence_mean_vector(tokens, ft_model):
    vectors = []
    for word in tokens:
        # FastText는 학습되지 않은 단어도 n-gram을 통해 벡터를 생성해줍니다.
        try:
            vectors.append(ft_model.wv[word])
        except KeyError:
            continue
            
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        # 단어가 하나도 없을 경우 영벡터 반환
        return np.zeros(ft_model.vector_size)

def main():
    # 데이터 경로 설정
    data_path = r'c:\Users\hkssn\바탕 화면\multicam\data\ratings_test.txt'
    
    if not os.path.exists(data_path):
        print(f"파일을 찾을 수 없습니다: {data_path}")
        return

    # 3. 데이터 로드 (id, document, label 구조)
    print("데이터 로딩 중...")
    df = pd.read_csv(data_path, sep='\t').dropna()
    
    # (선택 사항) 학습 속도를 위해 샘플링 (전체 5만건을 모두 사용하려면 아래 줄을 주석 처리하세요)
    # df = df.sample(5000, random_state=42)

    # 4. 토큰화 진행
    print("토큰화 진행 중...")
    df['tokens'] = df['document'].apply(tokenize)

    # 5. FastText 임베딩 학습
    print("FastText 모델 학습 중...")
    ft_model = FastText(
        sentences=df['tokens'],
        vector_size=100,
        window=5,
        min_count=2,
        sg=1, # Skip-gram 방식
        workers=4,
        seed=42
    )

    # 6. 문장을 벡터로 변환
    print("문장 벡터 생성 중...")
    X = np.array([get_sentence_mean_vector(t, ft_model) for t in df['tokens']])
    y = df['label'].values

    # 7. Train/Test 분할
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # 8. SVC 모델 생성 및 학습
    # 데이터 양이 많을 경우 kernel='linear'가 rbf보다 훨씬 빠릅니다.
    print("SVC 모델 학습 및 예측 중...")
    svc_model = SVC(kernel='linear', C=1.0)
    svc_model.fit(X_train, y_train)

    # 9. 결과 평가
    pred = svc_model.predict(X_test)
    print("\n[분류 결과 보고서]")
    print(classification_report(y_test, pred))

if __name__ == '__main__':
    main()