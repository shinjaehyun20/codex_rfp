# Schema Guide

모든 상태/아티팩트 계약은 `contracts/schemas`의 JSON Schema(v1)를 따른다.
- `additionalProperties: false`
- `required` 명시
- `type` / `schema_version`에 버전 포함

## 신규 도메인 스키마
- `customer.intent.snapshot.v1.schema.json`
  - 검색 데이터 기반 의도/여정/페르소나/생성형 AI 인사이트 스냅샷 표준.
  - 고객 응대 품질 개선과 마케팅 인사이트 리포트의 공통 계약으로 사용.
