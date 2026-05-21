class Bank():
    total_cost = 0
    user_cnt = 0

    def __init__(self, _name, _birth, _cost = 0): # _log = []):
        self.name = _name
        self.birth = _birth
        self.cost = _cost
        self.log = []
        Bank.total_cost += _cost
        Bank.user_cnt += 1
    
    def add_cost(self, _c):
        self.cost += _c
        dict_data = {
            'type' : '입금',
            'cost' : _c,
            'total_cost': self.cost
        }
        Bank.total_cost += _c
        self.log.append(dict_data)
        print(f'입금이 완료되었습니다. 현재의 잔액은 {self.cost} 원 입니다.')
    
    def sub_cost(self, _c):
        if self.cost >= _c:
            self.cost -= _c
            dict_data = {
            'type' : '출금',
            'cost' : _c,
            'total_cost': self.cost
            }
            Bank.total_cost -= _c
            self.log.append(dict_data)
            print(f'출금이 완료되었습니다. 현재의 잔액은 {self.cost} 원 입니다.')
            return 1
        else:
            print('잔액이 부족합니다.')
            return 0

    def user_info(self):
        print(f'이름: {self.name}, 나이: {self.birth}, 잔액: {self.cost}')

# -----------------------------------------------------------------------

class User(Bank):

    work_type ={
        'A': 11000,
        'B': 15000,
        'C': 20000
    }

    item_list = {
        '텀블러' : 50000,
        '스위치' : 730000,
        '거치대' : 20000,
        '헤드셋' : 520000,
        '노트북' : 2000000
    }


    def __init__(self, _name, _birth, _cost):
        super().__init__(_name, _birth, _cost)
        self.items = []

    def work(self, _type, _time):
        
        if _type in User.work_type:
            amount = User.work_type[_type] * _time

            super().add_cost(amount)
        
        else:
            raise  ValueError('저장되어 있는 일의 종류가 아닙니다.')

    def buy_item(self, _item):
        try:
            sub_res = super().sub_cost(User.item_list[_item])
            if sub_res:
                self.items.append(_item)
                print('구매 성공')
            else:
                print('구매 실패')
        
        except Exception as e:
            print(type(e).__name__)
            print(e)
            print('물건의 정보가 없습니다.')

    def user_info(self):
        print(f"""이름: {self.name}, 나이: {self.birth}, 잔액: {self.cost}, 구매한 물건의 목록: {self.items}""")

# -----------------------------------------------------------------------------------------------------------

# 모듈은 변수, 함수, 클래스의 모음 : py 파일로 생성

test_vari = "모듈 안의 변수 데이터"

def func_1(a, b):
    return a + b