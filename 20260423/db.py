# 모듈을 생성할 때 중요한 부분
# 모듈은 독립적인 영역 -> 사용할 라이브러리를 load

import pymysql

# class 선언 
class MyDB:
    # 생성자 함수 (서버의 정보를 받아오기 위해 사용)
    def __init__(self,
                 host = '127.0.0.1',
                 port = 3306,
                 user = 'root',
                 password = '1234',
                 db = 'multicam'):
        # 서버의 정보를 인자로 받아와서 객체 내부에서 독립적인 변수에 저장
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    # 데이터베이스에 변화를 주는 함수 
    def commit(self):
        try:
            # DataBase에 데이터를 확정 (동기화)
            self.db_server.commit()
            # 서버와의 연결을 종료 ( 중요한 부분 )
            self.db_server.close()
            # close() 함수를 사용하더라도 self.db_server의 변수는 사라지지 않는다. 
            # 변수 자체를 제거 
            del self.db_server
        except:
            # 문제가 발생하는 이유는? -> 서버와의 연결이 되지 않은 경우 (self.db_server라는 변수에 데이터가 없거나 아예 존재하지 않는 경우)
            print( "데이터베이스 서버와의 연결이 되어있지 않습니다. sql_query() 함수를 호출하여 서버와의 연결을 해주세요" )
    
    def sql_query(self, query, *datas):
        # query : sql query문이 입력이되는 매개변수 
        # datas : query문에서 사용이 될 데이터의 목록

        # 문제점 : 서버의 재접속으로 commit 전의 데이터가 날아감. 
        # 이미 접속중인 경우 재접속 금지 (2026.04.20 update)
        # 해결 방법 self.db_server에 데이터가 존재한다면? -> 서버의 접속중이다. 
        try:
            self.db_server
            # 변수가 존재하지 않으면 NameError 발생 
            print('접속된 서버가 존재함')
        except:
            # 예외 상황이 발생하면 서버와 연결(self.db_server 라는 변수가 없을 시 실행)
            # DB_server와의 연결 
            self.db_server = pymysql.connect(
                host = self.host, 
                port = self.port, 
                user = self.user, 
                password = self.password, 
                db = self.db
            )
        # cursor 생성 
        cursor = self.db_server.cursor(pymysql.cursors.DictCursor)

        # self.변수명 // 변수명의 차이는?
            # self.변수 -> 독립적으로 객체 안에 저장이 되는 변수 ( 함수 호출 후에도 데이터가 존재 )
            # 변수 -> 함수 호출시 생성이 되고 함수가 종료가 되면 휘발성으로 사라짐
        try:
            # CUD의 경우에는 execute() 쿼리문을 커서에 질의 보낸다. R (select도 여기까지는 공통의 작업)
            # execute( query, () ) -> 호출 가능 
            # execute( query, (1,2,3) ) -> 호출 가능 
            cursor.execute(query, datas)
            # query가 select문이라면? 
            # select * from table // SELECT * FROM table, """   select * from table   """ -> 두가지의 경우 모두 참 
            # 좌측 공백을 제거 , 소문자를 통일 , 시작값이 select와 같은가 startwith()
            if query.lstrip().lower().startswith('select'):
                # 결과값을 받아온다. 
                result = cursor.fetchall()
            else:
                result = "Query OK!"
            return result
        except Exception as e:
            print('query문 execute중 에러')
            print(e)