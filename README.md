# Gaonbooks-finder

## 커밋 메시지 규약

| 키워드 | 설명 |
|---|---|
| feat | 새로운 기능 추가 |
| fix | 버그 수정 |
| docs | README, 주석 등 문서 수정 |
| style | 포메팅, 세미콜론 수정 |
| refactor | 코드 리팩토링(기능 변경 x) |
| test | 테스트 코드 작성 |
| chore | 빌드 수정, 패키지 업데이트 |
| perf | 성능 개선 |
| build | 빌드 관련 수정(docker, poetry) |
| ci | CI 설정(Github Action) |
| revert | 이전 커밋 되돌리기 |
| hotfix | 버그 처리 후 배포시 사용 |

## 풀스택 웹개발 계획

[참고자료](https://github.com/fastapi/full-stack-fastapi-template)

### 1. 백엔드 개발(테스트 코드 작성 필수)

- 데이터베이스 없이 엑셀 파일로만 구축
- 웹 메인페이지 개발
- 책 위치 검색 결과 반환 api 개발(/search?q=도서명)
- 전화번호 전달 api 개발(엑셀 파일에 쓰기)
- 품절처리, 해지 api 개발(txt 파일에 쓰기)

### 2. 프론트 개발

- 리액트(React) 개발
- API 연결

### 3. 로컬 배포 후 테스트

- 실제로 접속 가능한 방식인지 테스트

## 가온북스 책 찾기 프로그램

```text
start.sh 파일 실행
"excel" 폴더에 새로운 엑셀 파일 넣기
soldout 폴더에는 품절된 책 리스트 표시
(만약 재고가 다시 채워졌을 때는 해당 책 파일 지우기)
```
