import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from gensim.models import Word2Vec, FastText

# Class 선언: Word2Vec을 GridSearchCV에 사용하기 위해서

class Word2VecVectorizer(BaseEstimator, TransformerMixin):
    # BaseEstimator: get_params, set_params와 같은 함수의 기능을 상속 받는다.
    # TransformerMixin: fit()과 transform() 함수만 선언하면 fit_transform() 함수를 이용 가능


    # 생성자 함수 → class가 생성될 때 기본적으로 사용할 변수들을 지정 (데이터 대입)
        # Word2Vec에서 사용할 인자값들을 생성자 함수에서 미리 받아온다.
    def __init__(
            self,                   # 자기 자신: 객체가 생성된 위치
            tokenizer = None,       # 토큰화 함수 (기본값은 None)
            vector_size = 100,      # 벡터화된 데이터의 차원의 수 지정
            min_count = 5,          # 전체 문서에서 최소 등장 횟수 지정
            window = 5,             # 중심 단어와 주변 단어들의 거리 제한
            sg = 1,                 # 단어 예측 방식 (0: CBOW, 1: skip-gram)
            epochs = 100,           # 반복 학습의 횟수
            workers = 1,            # 계산에 사용할 스레드의 수
            seed = 42,
            min_n = 2,
            max_n = 6,
            bucket = 2000000,
            type = 'w2v'
    ):
        self.tokenizer = tokenizer
        self.vector_size = vector_size
        self.min_count = min_count
        self.window = window
        self.sg = sg
        self.epochs = epochs
        self.workers = workers
        self.seed = seed
        self.min_n = min_n
        self.max_n = max_n
        self.bucket = bucket
        self.type = type
    
        # 모델과 단어 사전을 저장할 빈 공간 생성
            # 일반적인 문법: class 선언 시 self.변수(객체 변수)들은 생성자 함수에서 생성한다.
        self.model = None
        self.voca = None
    



    # 총 4개의 메서드를 생성: 토큰화, 학습, 문장 데이터를 평균 단위 벡터로 생성하는 함수, 변형
    # 토큰화 메서드
    def to_token(self, sentences):
        # sentences: 문장들의 목록
        # 만약에 토큰화 함수가 존재하지 않는다면: self.tokenizer가 None인 경우 → split()
        if self.tokenizer is None:
            result = []
            for sentence in sentences:
                token = list(sentence.split())
                result.append(token)
            # result = [[word for word in sentence.split()] for sentence in sentences]
        else:
            result = []
            for sentence in sentences:
                token = self.tokenizer(sentence)
                result.append(token)
            # result = [self.tokenizer(sentence) for sentence in sentences]
        return result
    

    # 학습 메서드: fit() 함수 생성
    # sklearn 안 모델들의 fit() 함수의 인자값들: 독립변수, 종속변수
    def fit(self, X, y):
        # X: 독립 변수 (문장 목록, 2차원 데이터)
        # y: 종속 변수 (1차원 데이터)
        # sentences: 토큰화된 문장 데이터
        sentences = self.to_token(X)
        # self.type이 Word2Vec이라면 Word2Vec에 학습
        if self.type == 'w2v':
            self.model = Word2Vec(
                sentences = sentences,
                vector_size = self.vector_size,
                window = self.window,
                min_count = self.min_count,
                sg = self.sg,
                epochs = self.epochs,
                workers = self.workers,
                seed = self.seed
            )
        
        elif self.type == 'ft':
            self.model = FastText(
                sentences = sentences,
                vector_size = self.vector_size,
                window = self.window,
                min_n = self.min_n,
                max_n = self.max_n,
                bucket = self.bucket,
                sg = self.sg,
                epochs = self.epochs,
                workers = self.workers,
                seed = self.seed
            )

        # 학습 모델이 생성되었으니 단어 사전에 데이터 입력
        self.voca = self.model.wv.key_to_index.keys()
        return self
    

    # 문장 벡터 생성하는 함수
    def doc_vec(self, token):
        # token: 토큰화된 문장 데이터 (1개의 문장)
        vectors = []
        for word in token:
            if word in self.model.wv:
                vec = self.model.wv[word]
                vectors.append(vec)
        # vectors 데이터가 존재하지 않는 경우 → 특정 문장에서 단어들이 단어 사전에 존재하지 않을 때
        if vectors:
            result = np.mean(vectors, axis = 0)
        else:
            result = np.zeros(self.model.vector_size)
        return result
    

    # 변형 함수 생성 (transform)
    # sklearn 안 모델들의 transform() 함수의 인자값: X_test
    def transform(self, X):
        # 토큰화
        sentences = self.to_token(X)
        # 벡터화(임베딩)
        result = []
        for token in sentences:
            vec = self.doc_vec(token)
            result.append(vec)
        return np.array(result)
    