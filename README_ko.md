<p align="center">
  <img src="banner.svg" alt="Agent Skill Lab" width="100%"/>
</p>

<h3 align="center">AI가 막 짜는 코드, 이제 그만 — 시니어 수준의 개발 규율을 심어주는 플러그인</h3>

<p align="center">
  <a href="README.md">English</a> &bull;
  <a href="README_zh_TW.md">繁體中文</a> &bull;
  <a href="README_ja.md">日本語</a> &bull;
  <a href="README_de.md">Deutsch</a> &bull;
  <strong>한국어</strong>
</p>

<p align="center">
  <a href="#설치">30초 만에 설치</a> &bull;
  <a href="#플러그인-목록">플러그인 둘러보기</a> &bull;
  <a href="#기여하기">기여하기</a>
</p>

---

## 문제점

AI 코딩 에이전트, 분명 강력합니다. 하지만 규율 없이 풀어놓으면? 스펙은 무시하고, 테스트는 빼먹고, 실패한 명령을 무한 재시도하고, 문서 한 줄 없는 API를 쏟아냅니다. 배포는커녕 에이전트 뒷수습에 하루가 갑니다.

## 해결책

**Agent Skill Lab**은 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)용 플러그인 마켓플레이스로, 엔지니어링 모범 사례를 설치 가능한 스킬로 제공합니다. 스펙 우선 API 개발, 명령어 실행 위생, 구조화된 개발 로그, SQL DDL 규칙 — 각 플러그인이 시니어 개발자 수준의 기준을 에이전트에게 적용합니다.

## 설치

```bash
# 1. 마켓플레이스 추가 (최초 1회)
claude plugin marketplace add https://github.com/MattAtAIEra/Agent-Skill-Lab.git

# 2. 필요한 플러그인 설치
claude plugin install dev-discipline@agent-skill-lab
claude plugin install sql-ddl-convention@agent-skill-lab
claude plugin install skill-and-agent-authoring@agent-skill-lab
```

## 플러그인 목록

| 플러그인 | 스킬 | 적용 규율 |
|---------|------|----------|
| **dev-discipline** | `api-dev-workflow` `command-execution` `dev-log` | 스펙 우선 API 개발, 안전한 명령어 실행, 구조화된 개발 로그 |
| **sql-ddl-convention** | `sql-ddl-convention` | DDL 설계 표준 — 감사 컬럼, 인덱스, 네이밍 규칙, Mermaid ERD 생성 |
| **skill-and-agent-authoring** | `skill-and-agent-authoring` | 새 플러그인 작성을 위한 YAML 프론트매터 및 디렉토리 구조 가이드 |

### dev-discipline

에이전트의 개발 워크플로를 빈틈없이 관리하는 3가지 스킬:

- **api-dev-workflow** — 스펙 우선 개발을 강제합니다: API 스펙 작성 → 사용자 확인 → 구현 → 테스트 → Postman Collection & OpenAPI 문서 생성. 어떤 단계도 건너뛸 수 없습니다.
- **command-execution** — 무분별한 재시도를 차단합니다. 한 번 실행 → 결과 확인 → 원인 분석 → 다음 행동 결정. 작업 디렉토리 검증, 선행 조건 확인, 백그라운드 프로세스 관리를 포함합니다.
- **dev-log** — 각 개발 단계를 `doc/dev-log.md`에 자동으로 기록합니다. 수행 내용, 발견 사항, 현재 테스트 상태를 구조화된 항목으로 남깁니다.

### sql-ddl-convention

포괄적인 SQL DDL 규칙 세트:

- `BIGINT` 기본 키, 필수 감사 컬럼 (`creator`, `createDate`, `modifier`, `modifyDate`, `removed`)
- 외래 키 명명 규칙 `<tableName>_id`, FK 제약 조건 없음 (애플리케이션 레이어 책임)
- 인덱스 규칙, 기본 `NOT NULL`, `camelCase` 명명, ENUM 금지, 금액에 `FLOAT` 금지
- DDL 출력 시 Mermaid ER 다이어그램 자동 생성

### skill-and-agent-authoring

메타 플러그인: 새로운 스킬과 에이전트를 작성하기 위한 완전 가이드. YAML 프론트매터, 트리거 문구 관례, 디렉토리 구조, 도구 설정을 다룹니다.

## 프로젝트 구조

```
agent-skill-lab/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── dev-discipline/         # API 워크플로, 명령어 안전성, 개발 로그
│   ├── sql-ddl-convention/     # SQL DDL 표준 + Mermaid ERD
│   └── skill-and-agent-authoring/  # 플러그인 작성 가이드
├── banner.svg
└── README.md
```

## 기여하기

우리 팀만의 개발 규율이 있다면, 플러그인으로 만들어 공유해 보세요. PR 언제든 환영합니다.

1. 이 저장소를 포크
2. `plugins/your-plugin-name/` 아래에 플러그인 생성
3. **skill-and-agent-authoring** 플러그인을 포맷 가이드로 참고
4. PR 제출

## 라이선스

MIT

---

<p align="center">
  <sub>내가 지키는 기준, AI에게도 똑같이 요구하는 개발자를 위해.</sub>
</p>
