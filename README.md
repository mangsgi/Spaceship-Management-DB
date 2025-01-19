# ✈ 우주선 종합 관리 시스템
* 2024-2 Database Term Project Spaceship Management Database System
* 개발기간: 2024.11 ~ 2024.12

<br>

## 🚀 프로젝트 개요
* 우주선 종합 관리 시스템은 우주 여행과 우주선 운영 및 관리를 지원하기 위해 설계된 데이터베이스입니다.
* **관리자, 조종사, 정비사, 고객**이 **우주선, 비행 일정, 유지보수 일정 및 기록을 포함한 우주선 종합 관리**에 대한 접근 및 관리할 수 있도록 설계되었습니다.

<br>

## 🎯 기술 스택
* **Backend**: <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" /> 
* **Frontend**: <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" /> <img src="https://img.shields.io/badge/Svelte-FF3E00?style=for-the-badge&logo=svelte&logoColor=white" />
* **Database**: <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
* **ORM 및 데이터 검증 라이브러리**: <img src="https://img.shields.io/badge/SQLAlchemy-00758F?style=for-the-badge&logoColor=white" /> <img src="https://img.shields.io/badge/Pydantic-231F20?style=for-the-badge&logoColor=white" />

<br>

## 🤼 팀 소개

|      김명석       |          이승재         |                                                                                                               
| :------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------: |
|   <img width="160px" src="https://avatars.githubusercontent.com/mangsgi" />    |                      <img width="160px" src="https://avatars.githubusercontent.com/Ea3124" />    |
|   UI/Design 개발   |  ML/DL 개발  |
|   [@mangsgi](https://github.com/mangsgi)   |    [@Ea3124](https://github.com/Ea3124)  |
| 부산대학교 정보컴퓨터공학부 3학년 | 부산대학교 정보컴퓨터공학부 3학년 |

<br>

## 👨‍👩‍👧‍👧 사용자 역할
### 관리자
* 새로운 비행 일정을 계획하고 기존 일정을 수정 또는 취소할 수 있다.
* 비행 일정에 필요한 가용가능한 조종사를 할당할 수 있다. 더불어, 조종사의 라이선스 취득 현황과 상태를 관리한다.
* 우주선의 상태를 모니터링하고 유지보수 일정을 조정하며 정비사를 할당하여 유지보수를 진행한다.
### 조종사
* 우주선의 운항을 책임지므로 비행과 관련한 업무를 수행하는 역할
* 자신에게 할당된 비행 일정을 조회하여 스케줄을 관리하고, 라이선스를 확인하여 항공 안전 규정을 준수하고 면허 및 인증 상태를 유지한다.
### 고객
* 우주선을 이용하여 목적지로 이동하는 사용자
* 원하는 비행을 검색하고 좌석을 예약할 수 있고, 예약한 좌석에 대한 조회 및 예약 변경 등을 수행할 수 있다.
* 연락처 등의 개인정보를 스스로 관리 및 변경할 수 있다.
### 정비사
* 우주선의 유지보수와 수리를 담당하는 역할
* 우주선의 상태를 조회할 수 있다.
* 정기적인 점검과 필요 시 수리를 수행 및 기록한다.

<br>

## 📺 화면 구성 (예시)
### ⭐️ 초기 화면
<div align="center">
  <img src="https://github.com/user-attachments/assets/dae0436f-55bb-4b99-b68d-07a26dd9f33c" width=70%/>
</div>

### ⭐️ 역할 선택 및 로그인
<div align="center">
  <img src="https://github.com/user-attachments/assets/5fd87be0-bc57-48b1-9f49-d61a79bc75c3" width=70%/>
</div>

### ⭐️ 역할별 업무 (조종사)
<div align="center">
  <img src="https://github.com/user-attachments/assets/75bacc98-2c69-4714-b66e-e508f20aa60a" width=70%/>
</div>

### ⭐️ 비행 일정 조회 (조종사)
<div align="center">
  <img src="https://github.com/user-attachments/assets/4420d22d-1d8e-485a-af15-6c3853183305" width=70%/>
</div>

### ⭐️ 개인정보 수정 (조종사)
<div align="center">
  <img src="https://github.com/user-attachments/assets/96e36409-3fde-4547-98f9-003e411e9410" width=70%/>
</div>

---
## 🛠️ 설치 및 실행 가이드
### 1. 리포지토리 클론
```bash
git clone https://github.com/mangsgi/Spaceship-Management-DB.git
```
### 2. 의존성 설치
```bash
pip install -r requirements.txt
```
### 3. 환경 변수 설정
```bash
DATABASE_URL = "postgresql://<user_id>:<db_port>@<db_url>/<db_name>"
```
### 4. DB 초기화 (선택)
```bash
# Database reset
DROP DATABASE <db_name>;

# Database creation
CREATE DATABASE <db_name> OWNER <user_id> TABLESPACE <tablespace_name>;
```
* Backend 폴더 내 initial_database_postgreSQL.txt 명령어 실행

### 5. 실행
```bash
# if you want to execute backend
cd backend
uvicorn main:app --port 8000

# if you want to execute frontend
cd frontend
npm run dev
```
