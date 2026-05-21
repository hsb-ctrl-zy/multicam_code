# 모듈 안에 변수, 함수, 클래스

# 전역 변수 생성 (mod.py 파일 영역에서는 어디서든 사용 가능)
variable = 'Module Variable'

def module_func(a, b):
    result = a + b

    # a - b 데이터는 전역 변수(mod.py 영역의 전역 변수)에 저장
    globals()['func_res'] = a - b

    # 함수에서 특정 데이터를 되돌려준다
    return result

class Module_Class:
    
    # 클래스 변수
    class_variable = []

    def __init__(self, x):
        # self.x는 클래스에서 독립적으로 사용되는 독립 변수 생성
        self.x = x
        self.class_variable = Module_Class.class_variable
    
    def info(self):
        # 등록된 x의 데이터를 제곱하여 되돌려준다.
        return self.x ** 2
    