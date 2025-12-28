# Notion MCP 서버 - Data Source 권한 문제 해결 가이드

## 문제 원인

사용자의 Notion 데이터베이스 스키마 조회 결과:

```
❌ Failed to create calendar event: Name is not a property that exists. 
   Date is not a property that exists.
```

**근본 원인**: 
1. Notion이 새로운 "data source" 구조를 사용하고 있음
2. Integration이 메인 데이터베이스 뷰는 볼 수 있지만, 실제 데이터를 저장하는 data source에는 접근 권한이 없음
3. 따라서 속성(properties)을 읽거나 쓸 수 없음

## 해결 방법

### 옵션 1: Data Source 권한 부여 (권장)

1. **Notion 앱** 열기
2. 문제가 있는 데이터베이스로 이동
3. 우측 상단 **"..."** (더보기) 메뉴 클릭
4. **"Connections"** 또는 **"연결"** 선택
5. Integration이 이미 연결되어 있어도, **다시 확인하고 "Allow access to underlying database"** 같은 옵션 체크
6. 저장

### 옵션 2: 새 데이터베이스 생성 (테스트용)

간단한 테스트를 위해 새 데이터베이스를 만들어 사용:

1. Notion에서 **새 페이지** 생성
2. **/table** 입력하여 **테이블 데이터베이스** 생성
3. 컬럼 추가:
   - **이름** (Title 타입) - 이것이 기본 제목 컬럼
   - **날짜** (Date 타입)
4. 데이터베이스 우측 상단 **"Share"** → Integration 연결
5. 새 데이터베이스 ID를 `.env` 파일에 업데이트

### 옵션 3: 현재 데이터베이스의 실제 속성 이름 확인

사용자가 Notion에서 직접 확인하여 알려주기:

1. 데이터베이스를 열고 컬럼 이름 확인
2. 제목 컬럼 이름은? (예: "Name", "제목", "Title" 등)
3. 날짜 컬럼 이름은? (예: "Date", "날짜", "일정" 등)
4. 그 정보로 코드 수정

## 다음 단계

위 방법 중 하나를 선택하거나, 현재 데이터베이스의 **실제 속성 이름**을 알려주시면 코드를 수정하겠습니다.
