# Metabox

---

## 🚂 프로젝트 소개

### 사이트 컨셉

메가박스 홈페이지를 모티브로 한 사이트입니다. 사이트에 접속한 모든 유저들은 상영중인 영화리스트와 각 영화에 대한 사용자들의 포스트를 볼 수 있습니다. `메타박스` 회원은 예매를 할 수 있으며, 관람한 영화에 대해서 포스트를 작성할 수 있습니다.

### 개발기간

- 2021.09.13 - 2021.09.30

### 개발인원

- FrontEnd
  - 이송현, 김동준, 김영현
- BackEnd
  - 주종민, 윤현묵, 송치헌

### 시연영상

[영상 보러가기](https://www.youtube.com/watch?v=PkHOsGvFzec)

## 🛠 적용 기술 및 구현사항

---

### 실행환경

- MacOSX
- Ubuntu
- Conda 4.10.3 version
- Django 3.2.6 version
- MySQL 5.7 version
- mysqlclient 2.0.3 version
- Django-cors-headers 3.7.0 version

### 적용기술

- FrontEnd : html, styled-compnents, javascript, react
- BackEnd : Python, Django, MySQL

### 협업도구

- Slack
- Git & Github
- Trello
- Postman

### FrontEnd 구현기능

#### 김영현님

- `[MoviePost]` : pagination, 무비포스트 상세 modal
- `[MoviePostWrite]`, 이미지 파일을 포함한 포스트 작성, 50자 이내 제한
- `[Modal]` : 로그인/회원가입, 소셜 로그인/회원가입 
- `[Footer]` 
- 로고 디자인

#### 김동준님

- `[Nav]` : 기본 라우팅, 사이트맵, 검색 창 클릭 이벤트
- `[Main]` : 영화 리스트 pagination / 정렬 (평점/개봉일/보고싶어요)
- `[Details]` : radar, block, line 그래프를 이용하여 영화 주요 정보 표현
- `Libraries` : chart.js
#### 이송현님

- `[Booking]`
- 예매 화면의 상단 캘린더 로직
- 달력 아이콘 클릭 시, 테이블 형태의 캘린더 fold/unfold 로직 구현
- 메가박스의 빠른 예매 기본 프로세스와 동일한 로직 구현
- `Libraries` : date-fns, React Date Picker

### BackEnd 구현기능

#### 윤현묵님

- `[Movie]`
  - 영화 목록 조회 기능 구현
  - Pagenation
  - 영화 상세 정보 조회 기능 구현
  - 영화 찜 기능(좋아요 기능)
  - 영화 목록 정렬 및 검색 기능 구현(최신 순, 평점 순, 좋아요 순 등)

- `[DB Upload]`
  - CSV 파일을 이용한 Script DB Uploader 기능 구현

#### 주종민님

- `[User]`
  - `[Sign up]` : METABOX 회원가입 기능 구현
  - `[Sign in]` : 일반 로그인 기능
  - `[Social log in]` : 소셜 로그인(카카오 로그인) 기능 구현
  - `[JWT]` : Json Web Token 발급 및 토큰 만료 기능 구현

#### 송치헌님

- `[Booking]`
  - 상영 날짜, 영화, 영화관 별로 상영 시간을 필터링하는 기능 구현
  - 좌석 설정 기능 구현
  - 예매 내역 조회 기능 구현

- `[Authorization]`
  - python decorator를 이용한 인가 기능 구현(로그인 데코레이터)

#### 공통 구현기능

- `[MoviePost](영화 리뷰)`
  - 리뷰 작성 기능 구현(인가된 유저만 작성 가능)
  - 모든 리뷰 조회 기능 구현
  - 리뷰 정렬 기능 구현(최신 순, 공감 순)
  - Pagenation

## 📃 Reference

---

- 이 프로젝트는 [메가박스](https://www.megabox.co.kr/) 사이트를 참조하여 학습목적으로 만들었습니다
- 학습수준의 프로젝트로 만들었기 때문에 이 코드 및 데모영상을 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다