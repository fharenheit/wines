# 와인 정리 노트

지역 → 마을 → 등급 → 밭(클리마/리외디) → 주요 생산자 순으로 정리한 와인 자료.

---

## 🇫🇷 프랑스 France

![프랑스 와인 산지 지도](assets/france-overview.svg)

| # | 문서 | 내용 |
|---|---|---|
| 00 | **[프랑스 개요](france/00-overview.md)** | 등급 체계(AOC/IGP), 지역별 등급 단위 차이, 라벨 읽기, 빈티지 |
| 01 | **[보르도](france/01-bordeaux.md)** | **좌안/우안** 구분, 1855 그랑크뤼 클라세 1~5등급, 그라브·소테른, 생테밀리옹·포므롤 |
| 02 | **[부르고뉴 개요](france/02-bourgogne.md)** | 등급 피라미드, 하위 산지 6곳, 도멘 vs 네고시앙 |
| 02-1 | **[코트드뉘](france/02-1-cote-de-nuits.md)** | **마을별** — 주브레샹베르탱 ~ 뉘생조르주, 그랑크뤼 24개 |
| 02-2 | **[코트드본](france/02-2-cote-de-beaune.md)** | **마을별** — 코르통 ~ 마랑주, 화이트 그랑크뤼 |
| 02-3 | **[샤블리·샬로네즈·마코네](france/02-3-chablis-chalonnaise-maconnais.md)** | 샤블리 그랑크뤼 7개, 메르퀴레·지브리, 푸이퓌세 |
| 02-4 | **[보졸레](france/02-4-beaujolais.md)** | 크뤼 10개, 갱 오브 포 |
| 03 | **[샹파뉴](france/03-champagne.md)** | 그랑크뤼 17개 마을, 5개 지구, 하우스 vs 그로워 |
| 04 | **[론](france/04-rhone.md)** | 북부(에르미타주·코트로티) / 남부(샤토뇌프뒤파프) |
| 05 | **[루아르](france/05-loire.md)** | 뮈스카데 → 사브니에르 → 부브레·시농 → 상세르 |
| 06 | **[알자스](france/06-alsace.md)** | 그랑크뤼 51개 밭, 고귀품종 4종 |
| 07 | **[남부 및 기타](france/07-sud-et-autres.md)** | 랑그독루시용·프로방스·쉬드우에스트·쥐라·사부아·코르시카 |

---

## 지도

저장소에 포함된 SVG 지도. `scripts/make_maps.py`로 생성한다.

| 지도 | 파일 |
|---|---|
| 프랑스 전도 | [`assets/france-overview.svg`](assets/france-overview.svg) |
| 보르도 좌안/우안 | [`assets/bordeaux.svg`](assets/bordeaux.svg) |
| 코트도르 마을별 그랑크뤼 | [`assets/cote-dor.svg`](assets/cote-dor.svg) |
| 부르고뉴 하위 산지 | [`assets/bourgogne.svg`](assets/bourgogne.svg) |
| 론 밸리 | [`assets/rhone.svg`](assets/rhone.svg) |
| 루아르 | [`assets/loire.svg`](assets/loire.svg) |
| 샹파뉴 | [`assets/champagne.svg`](assets/champagne.svg) |
| 알자스 | [`assets/alsace.svg`](assets/alsace.svg) |

```bash
python3 scripts/make_maps.py   # assets/*.svg 재생성
```

---

## 빠른 참조

### 등급의 대상이 지역마다 다르다

| 지역 | 등급 대상 | 예 |
|---|---|---|
| 보르도 | **생산자(샤토)** | Château Latour = 1등급 |
| 부르고뉴 | **밭(클리마)** | Chambertin = 그랑크뤼 |
| 샹파뉴 | **마을** | Ambonnay = 그랑크뤼 마을 |
| 알자스 | **밭(리외디)** | Rangen = 그랑크뤼 |

### 보르도 좌안 1등급 5개

Lafite Rothschild · Latour · Mouton Rothschild (이상 포이약) · Margaux (마고) · Haut-Brion (페삭레오냥)

### 부르고뉴 라벨 규칙

라벨에 **마을명 없이 밭 이름만** 있으면 그랑크뤼.
`Chambertin` = 그랑크뤼 / `Gevrey-Chambertin` = 마을 등급

---

## 앞으로 정리할 산지

- [ ] 이탈리아 (피에몬테, 토스카나, 베네토)
- [ ] 스페인 (리오하, 리베라 델 두에로, 프리오라트)
- [ ] 독일 (모젤, 라인가우 — VDP 등급)
- [ ] 신대륙 (나파, 바로사, 말보로 등)
