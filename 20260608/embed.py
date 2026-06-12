from konlpy.tag import Komoran
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer

def tokenize(text):
    # konlpy 설치하고 토큰화 객체 생성 시 JDK 필요 (최신 버전에서 문제 발생)
    # Komoran이 사용 가능한 경우와 불가능한 경우
    try:
        komoran = Komoran()
        allow_pos = ['NNP', 'NNG', 'VV', 'VA', 'SL', 'MAG']
        tokens = []
        for word, pos in komoran.pos(text):
            if pos in allow_pos:
                tokens.append(word)
    except Exception as e:
        print('Komoran 사용 불가:', e)
        tokens = text.split()
    
    return tokens

docs = [
    '오늘 날씨가 좋다 여행 가고 싶다',
    '기온이 너무 올라서 아무것도 하기 싫다',
    '수업이 너무 지루하고 졸리다',
    '음식이 너무 맛이 없고 서비스도 별로다',
    '영화가 너무 재미있어서 시간이 가는 줄 몰랐다'
]

def global_vari_set(docs):
    tokens = []
    for doc in docs:
        token = tokenize(doc)
        tokens.append(token)

    w2v = Word2Vec(
        sentences = tokens,
        vector_size = 100,
        window = 5,
        min_count = 1,
        epochs = 100,
        sg = 1,
        workers = 2,
        seed = 42
    )

    global wv
    wv = w2v.wv

    tfidf_vec = TfidfVectorizer(
        tokenizer = tokenize,
        lowercase = False
    ).fit(docs)

    # word2vec에서는 단어의 이름을 가지고 단위 벡터 생성
    # idf 값들도 단어에 따라서 추출하기 편하게 만들기 위해서 dict 형태로 데이터 생성

    global idf_weight
    idf_weight = dict(zip(
        tfidf_vec.get_feature_names_out(),
        tfidf_vec.idf_
    ))

    return tokens

# 문장을 입력값으로 단위 벡터의 평균을 구하는 함수
def sent_embed_mean(token):
    # token: 토큰화된 하나의 문장
    vector = []
    for word in token:
        if word in wv.index_to_key:
        # Word2Vec에서 학습된 단어 사전에 word가 존재한다면
        # vector 리스트에 해당 단어의 단위 벡터를 추가
            vector.append(wv[word])
        
    # 만약 새로운 문장의 단어들이 Word2Vec에서 사전에 학습된 단어 사전에 존재하지 않는 경우
        # vector 값이 빈 리스트
    if vector:
        result = np.mean(vector, axis = 0)
    else:
        # vector가 존재하지 않는 경우에는 영행렬을 생성
        result = np.zeros(wv.vector_size)
    
    return result


# 단어별 단위 벡터의 평균 값과 idf 역수의 값들을 곱하여 새로운 벡터를 생성
def sent_embed_wv_idf(token):
    # 단어별 단위벡터
    vector = []
    # idf 값
    idf = []

    for word in token:
        if word in wv.key_to_index and word in idf_weight:
            vector.append(wv[word]*idf_weight[word])
            idf.append(idf_weight[word])
            # 각 단어별 단위 벡터에 idf를 곱한 값 → vector의 합산과 idf의 합산을 나눠준다. (평균을 구하는 방식)

    if vector:
        result = np.sum(vector, axis = 0) / (np.sum(idf) + 1e-9)
    else:
        result = np.zeros(wv.vector_size)
    
    return result


# 데이터 train, test 분할 / 생성된 모델을 매개변수로 받아서 학습, 예측 후 평가 지표 출력

def run_model(X, y, model, test_size = 0.2, stratify = None):
    # X: 독립 변수
    # y: 종속 변수
    # model: 사용할 모델
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size = test_size, stratify = stratify, random_state = 42
    )

    # 인자로 받은 모델을 이용해서 학습
    model.fit(X_train, y_train)
    # 학습된 모델을 이용하여 예측값을 생성
    pred = model.predict(X_test)

    result = classification_report(y_test, pred)
    print(result)


# 학습된 모델에서 예측 값들을 되돌려 받는 함수 생성
# embedding 기법 선택: w2v 만을 이용한 평균, w2v+idf 혼합한 벡터 평균

# 매개변수 3개 : 새로운 데이터(문장들), 학습된 모델, 벡터화 타입
def predict_sentence_list(
        sentences, model, vec_type = 'wv'
):
    # sentences: 문장들의 리스트
    # model: 학습된 모델
    # vec_type: 'wv' 또는 'idf' 값을 받는다.
    # 문장들을 토큰화 → tokenize 함수 호출하여 결과를 받아온다.

    X_test = []

    for sentence in sentences:
        token = tokenize(sentence)
        # 하나의 문장이 토큰화가 진행 되었으면 벡터화 함수에 데이터를 대입
        if vec_type == 'wv':
            vec = sent_embed_mean(token)
        elif vec_type == 'idf':
            vec = sent_embed_wv_idf(token)
        else:
            print('vec_type이 맞지 않습니다')
            return ''
        X_test.append(vec)  # 독립변수 생성 완료
    
    preds = model.predict(X_test)
    result = []
    
    for sentence, pred in zip(sentences, preds):
        label = '긍정' if pred == 1 else '부정'
        result.append([sentence, label])
    return result

if __name__ == '__main__':

    docs = [
        '오늘 날씨가 좋다 여행 가고 싶다',
        '기온이 너무 올라서 아무것도 하기 싫다',
        '수업이 너무 지루하고 졸리다',
        '음식이 너무 맛이 없고 서비스도 별로다',
        '영화가 너무 재미있어서 시간이 가는 줄 몰랐다'
    ]

    target = [1, 0, 0, 0, 1]
    tokens = global_vari_set(docs)
    print(tokens)
    print(wv)
    print(idf_weight)