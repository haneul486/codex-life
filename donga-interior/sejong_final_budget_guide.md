# 동아 인테리어 예산표 작업 지침

## 기준 파일

- HTML 기준 파일: `C:\sky\project\codex-life\donga-interior\sejong_final_budget.html`
- 이 문서는 항상 **사용자가 마지막으로 직접 수정해둔 현재 HTML 파일 상태**를 기준으로 다시 작업한다.
- 예전 대화 내용보다 **실제 파일 안에 들어있는 내용**을 우선한다.
- 현관·중문 시공 요청서는 `C:\sky\project\codex-life\donga-interior\entrance_middle_door_request.html`에서 관리한다.
- 현관·중문 시공 요청서의 참고 이미지는 `donga-interior/img/web/entrance-request-01.png`부터 순번 파일로 관리한다.

## 문자 인코딩

- HTML, JavaScript 문자열, JavaScript 주석, Markdown 문서는 모두 `UTF-8`로 저장한다.
- 한글이 들어가는 파일을 수정한 뒤에는 제목, 표 헤더, 주석, JSON 문자열까지 깨짐이 없는지 확인한다.

## 데이터 관리 원칙

- 이 문서는 HTML 안의 정적 표를 직접 수정하는 방식이 아니라, **스크립트 하단 JSON 데이터**를 기준으로 렌더링한다.
- 값을 바꿔야 할 때는 먼저 JSON을 수정하고, 화면은 그 JSON에서 다시 그려지도록 유지한다.
- 현재 데이터 원본은 아래 3개다.
  - `scheduleData`: 진행 일정 마일스톤
  - `interiorRequestData`: 인테리어 사장님에게 추가 요청할 내용
  - `constructionData`: 공사비 지급 현황
  - `transferData`: 가족 간 돈 입출금 내역
  - `disposalData`: 이사 시 가전가구 폐기 목록
  - `purchaseData`: 구매 필요항목

## 진행 일정 규칙

- 진행 일정은 `scheduleData` 배열로 관리한다.
- 각 항목 구조:

```js
{
  name: "일정명",
  startDate: "YYYY-MM-DD",
  endDate: "YYYY-MM-DD 또는 빈 문자열",
  note: "보조 설명"
}
```

- 상단 `진행 일정` 영역은 이 JSON만 읽어서 렌더링한다.
- 이사 관련 일정은 같은 `scheduleData`에 기록하며, 상단 로드맵에도 포함하고 `이사 정리` 섹션에도 따로 표시한다.
- 날짜 표시는 브라우저에서 한국어 형식과 요일을 함께 보여준다.

## 인테리어 추가 요청 규칙

- 인테리어 사장님에게 추가로 요청하거나 확정받을 내용은 `interiorRequestData` 배열로 관리한다.
- 각 항목 구조:

```js
{
  title: "요청 또는 확인할 내용",
  note: "보조 설명",
  status: "pending 또는 completed",
  answer: "답변 또는 결정 내용",
  completedDate: "YYYY-MM-DD 또는 빈 문자열"
}
```

- `인테리어 사장님 추가 요청 사항` 섹션은 이 데이터만 읽어서 렌더링한다.
- 답변을 받은 항목은 `status: "completed"`로 표시하고, `answer`에 결정 내용을 적는다.
- 아직 확인할 항목은 `status`를 생략하거나 `"pending"`으로 둔다.

## 이사 폐기 목록 규칙

- 이사 시 버릴 가전가구 목록은 `disposalData` 배열로 관리한다.
- 각 항목 구조:

```js
{
  room: "공간명",
  items: ["폐기 품목", "폐기 품목 2개"]
}
```

- `이사 정리` 섹션의 `가전가구 폐기 목록` 표는 이 데이터만 읽어서 렌더링한다.
- 품목에 수량이 있으면 `"책꽂이 2개"`처럼 품목명 문자열에 함께 적는다.

## 공사비 규칙

- 공사비는 `constructionData` 배열에서 관리한다.
- 각 항목 구조:

```js
{
  stage: "계약금",
  amountWon: 3000000,
  status: "paid 또는 planned",
  date: "YYYY-MM-DD 또는 빈 문자열",
  route: "지급 경로",
  memo: "메모"
}
```

- 공사비 금액 단위는 모두 `원`이다.
- 상단 `공사비` 카드, `공사비 지급 현황` 표, 전체 비용 계산은 모두 이 JSON을 기준으로 연동된다.

## 구매 필요항목 규칙

- 구매 필요항목은 항상 **현재 HTML 파일 안의 실제 항목 목록**을 기준으로 작업한다.
- 구매 관련 변경 요청이 들어오면 먼저 `purchaseData` 배열의 항목 존재 여부와 값을 확인한 뒤 수정한다.
- 각 항목 구조:

```js
{
  category: "가전",
  name: "냉장고",
  expectedWon: 1650000,
  status: "planned 또는 purchased",
  actualWon: 0,
  purchaseDate: "",
  purchaseRoute: "",
  deliveryDate: "YYYY-MM-DD 또는 빈 문자열",
  deliveryType: "배송 또는 설치 또는 배송/설치",
  deliveryTime: "시간대 또는 빈 문자열",
  deliveryNote: "배송/설치 보조 메모",
  memo: ""
}
```

- `expectedWon`은 예상 금액이다.
- `actualWon`은 실제 결제 금액이다.
- 배송 또는 설치 일정이 있으면 `memo`에 섞어 쓰지 않고 `deliveryDate`, `deliveryType`, `deliveryTime`, `deliveryNote`에 나누어 기록한다.
- `deliveryDate`가 있는 구매 항목은 상단 `진행 일정` 캘린더에 자동으로 표시된다.
- 예상 금액과 실결제 금액은 모두 `원` 단위로 통일한다.
- 숫자 입력칸은 `1,650,000`처럼 3자리마다 쉼표가 보이도록 유지한다.
- `status`가 `purchased`이면 구매완료로 표시된다.
- `구매 상태 요약`은 예상 금액이 0보다 큰 항목만 표시한다.
- 이사집 비용은 같은 `purchaseData`에 기록하되, 화면에서는 `이사 정리` 섹션으로 따로 분리해서 표시한다.
- 엘리베이터 사용료, 공유기처럼 입주 준비를 위해 실제 지출한 일회성 구비 비용은 `생활` 카테고리의 `purchaseData`에 기록한다.
- 이미 지불한 구비 비용은 `status: "purchased"`, `actualWon`에 실제 금액, `purchaseDate`에 결제일, `purchaseRoute`에 `"지불완료"`처럼 기록한다.
- 가족 간 돈 입출금은 지출이 아니므로 `purchaseData`가 아니라 `transferData`에 기록한다.
- 같은 사건에 실제 지출과 가족 간 정산/송금이 함께 있으면, 실제 지출은 `purchaseData`에 넣고 정산 흐름은 `transferData`에 따로 남긴다.
- `transferData` 항목은 생활 준비 비용, 구매 상태 요약, 이사 지출 합계에 포함하지 않는다.

## 현관·중문 요청서 규칙

- 현관·중문 시공 요청서는 사장님에게 보여줄 중문 참고 사진만 노출한다.
- 현재 요청서 기준 이미지는 `donga-interior/img/entrance-middle-door/` 폴더의 원본 JPG 6장이다.
- 현관문 시트지, 중문 우드부분, 신발장 가운데 오픈장은 현재 `영림170 PWT1206-2 전사 루나내추럴`로 통일하는 기준이다.
- 이 기준이 바뀌면 예산표의 `interiorRequestData`, 자재 선택표의 해당 기록, 현관·중문 요청서 이미지를 함께 확인한다.

## 화면 구조

- 상단 헤더: 문서 제목, 브라우저 현재 날짜 기준일, 인쇄 버튼
- 상단 헤더 링크: 현관·중문 시공 요청서
- 진행 일정: 마일스톤 카드
- 인테리어 사장님 추가 요청 사항
- 상단 요약 카드 3개
  - 공사비
  - 생활 준비 비용
  - 전체 비용: 총액, 총지출, 남은 비용을 함께 표시
- 비용 한눈에 보기
  - 카테고리별 비율 도넛 차트
  - 상위 지출 TOP 8
  - 구매 항목의 `deliveryDate` 기준 다가오는 설치 일정
- 이사 정리
  - 이사집 주소
  - 이사 일정
  - 이사 관련 지출 금액
- 돈 입출금 내역
  - 가족 간 입출금 기록
  - 지출 계산에서 제외되는 참고 금액
- 공사비 지급 현황 표
- 구매 상태 요약
- 구매 필요항목 상세표

## 기준일 규칙

- 기준일은 문서에 하드코딩하지 않는다.
- 페이지가 열릴 때 브라우저의 현재 날짜를 읽어 표시한다.
- 날짜는 한국어 형식과 요일을 함께 보여준다.

## 인쇄 규칙

- 인쇄 버튼은 브라우저 인쇄 기능을 호출한다.
- 인쇄 시 `구매 필요항목` 상세표는 자동 숨김 처리한다.
- 상단 요약 카드, 진행 일정, 공사비 지급 현황, 구매 상태 요약은 인쇄에 남는다.

## 수정 방식

- 작은 수정이라도 가능하면 기존 구조를 유지한다.
- 새 항목을 추가할 때는 먼저 적절한 JSON 배열에 넣고, 렌더링 함수가 그 값을 읽는지 확인한다.
- 값 계산용 함수와 UI 렌더링 함수를 분리한 상태를 유지한다.
- 화면 문구를 바꿀 때는 HTML 마크업, JSON 문자열, 주석의 한글이 모두 정상인지 함께 확인한다.

## GitHub Pages

- 저장소 루트 `index.html`은 Pages 진입점으로 사용할 수 있다.
- 실제 예산표 작업 기준 파일은 `donga-interior/sejong_final_budget.html`이다.
