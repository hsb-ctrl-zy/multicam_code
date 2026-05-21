# SQL query문들을 저장 

# 회원 테이블 생성 쿼리문 하나 작성
create_query = """
    CREATE TABLE IF NOT EXISTS `user` (
        `id` varchar(32) primary key,
        `password` varchar(32) not null,
        `name` varchar(32)
    )
"""

# 로그인 조회 쿼리문 작성
# id, password를 이용하여 데이터가 존재하는가?
login_query = """
    SELECT *
    FROM `user`
    WHERE `id` = %s AND `password` = %s
"""

# 회원 가입 쿼리문
    # 아이디 중복 체크
    # id, password, name 입력하고 회원가입
id_check_query = """
    SELECT *
    FROM `user`
    WHERE `id` = %s
"""

signup_query = """
    INSERT INTO `user` VALUES (%s, %s, %s)
"""

# 모듈 생성 (app.py 사용)
    # → querys 안에 user 모듈
    # → 