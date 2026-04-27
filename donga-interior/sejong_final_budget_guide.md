# 동아 인테리어 예산표 지침

이 문서는 [sejong_final_budget.html](C:/sky/project/codex-life/donga-interior/sejong_final_budget.html) 운영 기준입니다.

기준 작업 폴더:

- `C:\sky\project\codex-life\donga-interior`

## 0. 수정 기준 원칙

이 문서를 수정할 때는 **항상 사용자가 마지막으로 직접 수정해둔 실제 HTML 파일 상태를 기준으로 작업합니다.**

- 먼저 현재 [sejong_final_budget.html](C:/sky/project/codex-life/donga-interior/sejong_final_budget.html) 파일 내용을 확인합니다.
- 이전 대화에서 기억한 값이나 예전 버전을 기준으로 덮어쓰지 않습니다.
- 사용자가 HTML 안에서 직접 바꿔둔 금액, 문구, 배치, 상태값이 있으면 그 상태를 유지한 채 필요한 부분만 수정합니다.
- 특히 `구매 필요항목`은 항상 **현재 HTML 파일 안의 실제 항목과 값**을 기준으로 수정합니다.

간단히 말해, **예전 대화 내용보다 현재 파일에 실제로 들어 있는 상태를 우선 기준으로 삼습니다.**

## 1. 문서 목적

이 문서는 아래를 한 화면에서 함께 관리하기 위한 대시보드입니다.

- 공사비 총액과 지급 상태
- 생활 준비 비용
- 전체 필요 비용

## 2. 현재 화면 구조

현재 문서는 아래 순서로 구성됩니다.

1. 상단 제목
2. 요약 카드 3개
3. 공사비 지급 현황
4. 구매 상태 요약
5. 구매 필요항목

## 3. 데이터 구조

현재 문서는 **HTML 표를 직접 데이터 원본으로 사용하지 않고**, 스크립트 하단의 JSON 배열을 원본으로 사용합니다.

구성:

- `constructionData`
  - 공사비 지급 현황 데이터
- `purchaseData`
  - 구매 필요항목 데이터

즉, 앞으로는 항목과 값 수정이 필요할 때 아래 두 배열을 우선 기준으로 보고 작업합니다.

## 4. 상단 카드 구조

상단 카드는 모두 같은 구조를 따릅니다.

- 상단: `metric-label`
- 중앙: `metric`
- 하단: `metric-sub`

카드 종류:

- `공사비`
- `생활 준비 비용`
- `전체 비용`

## 5. 공사비 JSON

공사비는 `constructionData` 배열에서 관리합니다.

각 항목 필드:

- `id`
- `label`
- `date`
- `amountManwon`
- `route`
- `status`

상태 값:

- `paid`
- `planned`

## 6. 구매 JSON

구매 항목은 `purchaseData` 배열에서 관리합니다.

각 항목 필드:

- `id`
- `category`
- `item`
- `memo`
- `expectedManwon`
- `actualWon`
- `status`
- `purchaseDate`
- `paymentRoute`

상태 값:

- `planned`
- `purchased`
- `skip`

## 7. 연동 규칙

현재 화면은 아래 방식으로 연동됩니다.

- JSON 데이터로 표를 렌더링
- 사용자가 입력값을 바꾸면 해당 JSON 값을 즉시 갱신
- JSON이 바뀌면 카드, 요약표, 합계가 함께 다시 계산됨

즉, **표와 카드가 따로 노는 구조가 아니라 JSON 한 곳을 기준으로 전부 연결**되어 있습니다.

## 8. 문자 인코딩 규칙

이 프로젝트의 HTML, Markdown, 텍스트 파일은 모두 `UTF-8` 기준으로 유지합니다.

특히 아래 항목은 항상 확인합니다.

- HTML 안의 한글 제목, 본문, 버튼 문구
- JavaScript 문자열
- JavaScript 주석
- Markdown 문서 본문

한글이 깨진 상태를 발견하면 부분 수정으로 덧대지 말고, UTF-8 기준으로 다시 저장하고 확인합니다.

## 9. 인쇄 규칙

문서의 `인쇄` 버튼을 누르면:

1. `구매 필요항목` 상세표가 숨겨짐
2. 브라우저 인쇄 창이 열림
3. 인쇄가 끝나면 화면 상태가 돌아옴

즉, 인쇄본에는 너무 긴 하단 상세표를 넣지 않고 상단 요약 중심으로 출력합니다.

## 10. 수정 후 체크리스트

- 상단 카드 3개의 금액과 하단 문구가 정상 계산되는지
- 모바일에서 `select` 박스 내용이 잘리지 않는지
- `구매 상태 요약`이 실제 JSON 값과 같은지
- 인쇄 버튼을 누르면 상세표가 숨겨지는지
- 한글이 깨지지 않는지

## 11. GitHub Pages 메모

저장소:

- [codex-life](https://github.com/haneul486/codex-life)

Pages 주소:

- [https://haneul486.github.io/codex-life/](https://haneul486.github.io/codex-life/)

루트의 `index.html`이 실제 예산표 파일로 연결합니다.
