# proposal-ops (A안 monorepo)

## 구조
- `apps/api` - FastAPI API
- `apps/worker` - Celery worker
- `apps/web` - web scaffold (정적 페이지 + 간단 서버)
- `contracts/schemas` - JSON Schemas (single source of truth)
- `docs` - 운영/설계 문서

## 시작
```bash
cp .env.example .env
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
그 후 브라우저에서 `http://localhost:3000` 으로 접속하면 현재 스캐폴딩 화면을 볼 수 있습니다.
