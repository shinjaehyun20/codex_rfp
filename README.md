# proposal-ops (A안 monorepo)

## 구조
- `apps/api` - FastAPI API
- `apps/worker` - Celery worker
- `apps/web` - Next.js web app
- `contracts/schemas` - JSON Schemas (single source of truth)
- `docs` - 운영/설계 문서

## 시작
```bash
cp .env.example .env
cp apps/web/.env.example apps/web/.env.local
make up
```

## 개발
```bash
make api
make worker
make web
make test
```

## 프론트 화면 보기
```bash
make web
```
그 후 브라우저에서 `http://localhost:3000` 으로 접속합니다.

## Listening Mind 벤치마킹 개발안
- `docs/listening_mind_benchmark_mvp.md`
