# API Spec (v1)

- `GET /health`: 시스템 연결 상태
- `GET /cases?q=`: 케이스 목록
- `POST /cases`: 빈 케이스 생성 또는 멀티파트 파일과 함께 케이스 생성
- `GET /cases/{case_id}`: 케이스 상세(artifacts + 최근 runs)
- `POST /cases/{case_id}/artifacts`: 기존 케이스에 파일 업로드 추가
- `GET /runs?limit=&pipeline=&status=`: 실행 목록
- `POST /runs`: 파이프라인 실행 run 생성
- `GET /runs/{run_id}`: 진행률/산출물/상태 조회
