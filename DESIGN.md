# DESIGN

A안(monorepo) 기본 설계:
- `apps/api`: FastAPI + DB + MinIO API 계층
- `apps/worker`: Celery 기반 오케스트레이션
- `apps/web`: 프론트엔드 스캐폴딩
- `contracts/schemas`: JSON Schema 단일 진실원천
- `docs`: 운영/스펙 문서
