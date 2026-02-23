# Ops Manual

1. `.env.example`를 참고해 `.env` 생성
2. `apps/web/.env.example`를 참고해 `apps/web/.env.local` 생성
3. `make up`으로 postgres/redis/minio 실행
4. API: `make api`
5. Worker: `make worker`
6. Web: `make web` 후 `http://localhost:3000` 접속
7. 테스트: `make test`
