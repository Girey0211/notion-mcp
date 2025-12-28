# Notion MCP Server

UV와 [fastmcp](https://gofastmcp.com/)를 사용하여 Notion API와 통합된 Model Context Protocol (MCP) 서버입니다.

이 서버는 Claude Desktop과 같은 MCP 클라이언트에서 Notion의 캘린더 데이터베이스와 리스트 데이터베이스에 데이터를 직접 삽입할 수 있도록 해줍니다.

## 기능

- ✅ **캘린더 이벤트 추가**: Notion 캘린더 DB에 새로운 이벤트 생성
- ✅ **리스트 아이템 추가**: Notion 리스트 DB에 작업/항목 생성
- 🔒 **환경 변수 기반 보안**: API 토큰을 안전하게 관리
- 🔌 **Claude Desktop 연동**: STDIO 전송으로 간편한 로컬 통합
- ⚡ **빠른 설치**: UV를 통한 간편한 종속성 관리

## 필수 요구사항

- Python 3.10 이상
- [UV](https://docs.astral.sh/uv/) 패키지 매니저
- Notion 계정 및 Integration

## 설치

### 1. UV 설치 (아직 설치하지 않은 경우)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 또는 Homebrew
brew install uv
```

### 2. 프로젝트 종속성 설치

```bash
cd /Users/mac/Documents/workspace/notion-mcp
uv sync
```

## Notion 설정

### 1. Notion Integration 생성

1. [Notion Integrations](https://www.notion.so/my-integrations) 페이지로 이동
2. **"New integration"** 클릭
3. 이름을 입력하고 생성
4. **"Internal Integration Secret"** (API Token) 복사

### 2. 데이터베이스 공유

1. Notion에서 캘린더 데이터베이스와 리스트 데이터베이스를 엽니다
2. 각 데이터베이스에서 **"Share"** → **"Add connections"** 클릭
3. 방금 생성한 Integration을 선택

### 3. Database ID 찾기

데이터베이스 URL에서 Database ID를 확인할 수 있습니다:
```
https://www.notion.so/workspace/<database_id>?v=...
```
`<database_id>` 부분을 복사하세요.

### 4. 환경 변수 설정

```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일을 편집하여 값 입력
# NOTION_API_TOKEN=your_actual_token
# NOTION_CALENDAR_DB_ID=your_calendar_db_id
# NOTION_LIST_DB_ID=your_list_db_id
```

## 사용법

### Claude Desktop과 연동

Claude Desktop의 설정 파일을 수정하여 서버를 등록할 수 있습니다.

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "notion": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/mac/Documents/workspace/notion-mcp",
        "run",
        "python",
        "-m",
        "notion_mcp.server"
      ],
      "env": {
        "NOTION_API_TOKEN": "your_notion_token",
        "NOTION_CALENDAR_DB_ID": "your_calendar_db_id",
        "NOTION_LIST_DB_ID": "your_list_db_id"
      }
    }
  }
}
```

Claude Desktop을 재시작하면 Notion MCP 서버가 자동으로 연결됩니다.

> **참고**: `.env` 파일 대신 Claude Desktop 설정의 `env` 필드에 환경 변수를 직접 입력해야 합니다.

### 직접 서버 실행 (테스트용)

```bash
uv run python -m notion_mcp.server
```

서버는 STDIO 모드로 실행되어 표준 입출력을 통해 MCP 클라이언트의 연결을 대기합니다.

## MCP 도구

### `add_calendar_event`

캘린더 데이터베이스에 이벤트를 추가합니다.

**파라미터**:
- `title` (필수): 이벤트 제목
- `date` (필수): ISO 형식 날짜 (YYYY-MM-DD) 또는 datetime (YYYY-MM-DDTHH:MM:SS)
- `description` (선택): 이벤트 설명

**예시**:
```python
add_calendar_event(
    title="팀 미팅",
    date="2025-12-10",
    description="Q4 계획 논의"
)
```

### `add_list_item`

리스트 데이터베이스에 항목을 추가합니다.

**파라미터**:
- `title` (필수): 항목 제목
- `status` (선택, 기본값: "Not Started"): 상태
- `priority` (선택, 기본값: "Medium"): 우선순위
- `description` (선택): 항목 설명

**예시**:
```python
add_list_item(
    title="코드 리뷰",
    status="In Progress",
    priority="High",
    description="PR #123 검토"
)
```

## 데이터베이스 스키마 참고

이 서버는 다음과 같은 일반적인 Notion 데이터베이스 구조를 가정합니다:

### 캘린더 DB
- **Name** (Title): 이벤트 제목
- **Date** (Date): 이벤트 날짜

### 리스트 DB
- **Name** (Title): 작업 제목
- **Status** (Status): 작업 상태
- **Priority** (Select): 우선순위

> **중요**: 데이터베이스의 속성 이름이 다르면 `src/notion_mcp/notion_client.py` 파일을 수정해야 할 수 있습니다.

## 개발

### 프로젝트 구조

```
notion-mcp/
├── src/
│   └── notion_mcp/
│       ├── __init__.py
│       ├── server.py           # MCP 서버 메인
│       └── notion_client.py    # Notion API 헬퍼
├── pyproject.toml              # 프로젝트 설정
├── .env.example                # 환경 변수 템플릿
└── README.md
```

### 코드 수정

Notion 데이터베이스의 속성명이 다를 경우, `src/notion_mcp/notion_client.py`의 `properties` 딕셔너리를 수정하세요.

## 문제 해결

### "NOTION_API_TOKEN environment variable is required" 오류

`.env` 파일이 올바르게 설정되었는지 확인하세요.

### "Failed to create calendar event: Object not found" 오류

- Database ID가 올바른지 확인
- Integration이 해당 데이터베이스에 접근 권한이 있는지 확인 (Share 설정)

### 속성 관련 오류

Notion 데이터베이스의 실제 속성명과 코드의 속성명이 일치하는지 확인하세요. Notion 데이터베이스에서 속성명을 확인하고 필요시 코드를 수정하세요.

## 라이선스

MIT

## 참고 자료

- [FastMCP Documentation](https://gofastmcp.com/)
- [Notion API Documentation](https://developers.notion.com/)
- [UV Documentation](https://docs.astral.sh/uv/)
