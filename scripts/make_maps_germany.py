#!/usr/bin/env python3
"""독일 와인 산지 지도(SVG) 생성기.

make_maps.py 의 Map 클래스(경위도 → 픽셀 투영)를 재사용한다.
실행: python3 scripts/make_maps_germany.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from make_maps import (  # noqa: E402
    OUT, Map,
    C_BG, C_LAND_ED, C_SUB,
    C_RED, C_WHITE, C_SPARK, C_GREEN, C_PURPLE,
)

# ------------------------------------------------------------------ 국경 윤곽
GERMANY = [
    # 북해·덴마크 (서 → 동)
    (8.65, 54.90), (9.00, 54.85), (9.60, 54.83), (10.00, 54.40), (10.80, 54.35),
    (11.30, 54.10), (12.10, 54.20), (13.00, 54.40), (13.80, 54.15), (14.27, 53.75),
    # 폴란드 (북 → 남)
    (14.40, 53.30), (14.60, 52.60), (14.70, 52.10), (14.60, 51.80), (14.75, 51.50),
    (15.03, 51.28), (14.82, 50.87),
    # 체코 (동 → 서)
    (14.40, 50.90), (13.50, 50.70), (12.90, 50.40), (12.10, 50.30), (12.20, 50.00),
    (12.50, 49.90), (13.40, 48.90), (13.80, 48.77),
    # 오스트리아 (동 → 서)
    (13.00, 47.85), (12.80, 47.70), (12.20, 47.70), (11.40, 47.45), (10.90, 47.40),
    (10.45, 47.55), (10.10, 47.35), (9.60, 47.53),
    # 스위스 (동 → 서)
    (9.50, 47.55), (8.90, 47.65), (8.60, 47.60), (8.20, 47.60), (7.70, 47.55),
    (7.60, 47.58),
    # 프랑스 (남 → 북)
    (7.58, 48.00), (7.60, 48.30), (8.20, 48.97), (7.90, 49.05), (6.90, 49.20),
    (6.35, 49.46),
    # 룩셈부르크·벨기에
    (6.10, 49.50), (6.15, 50.00), (6.35, 50.30), (6.00, 50.75),
    # 네덜란드 (남 → 북)
    (5.90, 51.05), (6.20, 51.50), (6.80, 51.90), (6.70, 52.00), (7.05, 52.20),
    (7.20, 53.20), (7.00, 53.30), (8.00, 53.70), (8.50, 53.90), (8.90, 54.40),
]

# -------------------------------------------------------------------- 하천망
RIVERS_DE = {
    "Rhein": [(7.60, 47.58), (7.80, 48.10), (8.10, 48.70), (8.30, 49.00), (8.40, 49.50),
              (8.44, 49.80), (8.27, 50.00), (7.90, 50.05), (7.70, 50.15), (7.60, 50.36),
              (7.20, 50.55), (6.95, 50.94), (6.70, 51.40), (6.20, 51.85)],
    "Mosel": [(6.36, 49.46), (6.55, 49.60), (6.64, 49.75), (6.85, 49.85), (6.95, 49.90),
              (7.07, 49.92), (7.02, 49.96), (7.11, 49.95), (7.15, 50.05), (7.30, 50.15),
              (7.45, 50.25), (7.60, 50.36)],
    "Main": [(11.20, 50.10), (10.60, 50.05), (9.93, 49.79), (9.50, 49.80), (9.10, 49.85),
             (8.70, 50.00), (8.27, 50.00)],
    "Neckar": [(8.70, 48.20), (8.90, 48.60), (9.18, 48.78), (9.20, 49.05), (9.00, 49.20),
               (8.70, 49.40), (8.44, 49.53)],
    "Nahe": [(7.10, 49.65), (7.35, 49.78), (7.65, 49.85), (7.87, 49.95)],
    "Ahr": [(6.60, 50.48), (6.85, 50.52), (7.05, 50.54), (7.12, 50.55)],
    "Elbe": [(14.00, 50.80), (13.74, 51.05), (13.20, 51.50), (12.90, 51.90), (11.90, 52.10),
             (11.00, 52.90), (10.00, 53.50), (9.20, 53.60), (8.90, 53.90)],
    "Saale": [(11.55, 50.30), (11.75, 50.80), (11.85, 51.15), (11.95, 51.55)],
    "Unstrut": [(10.80, 51.20), (11.30, 51.20), (11.85, 51.18)],
}


def cities(m, pts, size=11):
    for lon, lat, name, dx, dy in pts:
        m.square(lon, lat)
        m.label(lon, lat, name, dx=dx, dy=dy, size=size, fill=C_SUB,
                anchor="middle" if dx == 0 else ("start" if dx > 0 else "end"))


def numbered(m, items, footer_h, col_w, rows_per_col, name_dx=15, sub_dx=None):
    m.h += footer_h
    for n, lon, lat, ko, en, sub, color in items:
        x, y = m.xy(lon, lat)
        m.add('<circle cx="%.1f" cy="%.1f" r="10.5" fill="%s" stroke="%s" stroke-width="1.6"/>'
              % (x, y, color, C_BG))
        m.text_px(x, y + 4, str(n), size=12, fill="#ffffff", anchor="middle", weight="700",
                  halo=False)
    fy = m.h - footer_h + 6
    m.add('<rect x="14" y="%.1f" width="%.1f" height="%.1f" fill="#ffffff" '
          'fill-opacity="0.92" stroke="%s" rx="4"/>' % (fy, m.w - 28, footer_h - 20, C_LAND_ED))
    sub_dx = col_w - 22 if sub_dx is None else sub_dx
    for i, (n, lon, lat, ko, en, sub, color) in enumerate(items):
        col, row = divmod(i, rows_per_col)
        bx = 32 + col * col_w
        by = fy + 24 + row * 19.5
        m.add('<circle cx="%.1f" cy="%.1f" r="8" fill="%s"/>' % (bx, by - 4, color))
        m.text_px(bx, by, str(n), size=10.5, fill="#fff", anchor="middle", weight="700",
                  halo=False)
        m.text_px(bx + name_dx, by, "%s %s" % (ko, en) if en else ko, size=11.5,
                  weight="600", halo=False)
        if sub:
            m.text_px(bx + sub_dx, by, sub, size=10.5, fill=C_SUB, anchor="end", halo=False)


# ======================================================================== 지도 1
def map_germany():
    m = Map((5.4, 47.1, 15.4, 55.2), 720, pad=14,
            title="독일 13개 와인 산지 (Anbaugebiete)",
            subtitle="Deutschland : 리슬링 세계 최대 재배국. 북위 47~52°의 서늘한 한계 지대")
    m.base(rivers=list(RIVERS_DE.keys()), shapes=[GERMANY], river_src=RIVERS_DE, river_w=1.8)

    items = [
        (1, 7.05, 50.53, "아르", "Ahr", "슈페트부르군더(피노 누아)", C_RED),
        (2, 7.72, 50.22, "미텔라인", "Mittelrhein", "급경사 편암", C_WHITE),
        (3, 6.95, 49.88, "모젤", "Mosel", "리슬링 · 청회색 편암", C_WHITE),
        (4, 7.68, 49.83, "나에", "Nahe", "지질 다양성 최대", C_WHITE),
        (5, 8.00, 50.03, "라인가우", "Rheingau", "리슬링 · 남향 사면", C_WHITE),
        (6, 8.20, 49.82, "라인헤센", "Rheinhessen", "최대 면적", C_WHITE),
        (7, 8.15, 49.35, "팔츠", "Pfalz", "온난 · 리슬링 · 레드", C_WHITE),
        (8, 8.62, 49.65, "헤시셰 베르크슈트라세", "Hess. Bergstraße", "최소 산지 중 하나", C_WHITE),
        (9, 10.05, 49.78, "프랑켄", "Franken", "질바너 · 복스보이텔 병", C_WHITE),
        (10, 9.30, 49.00, "뷔르템베르크", "Württemberg", "레드 중심 · 트롤링거", C_RED),
        (11, 7.90, 48.45, "바덴", "Baden", "가장 따뜻 · 부르군더", C_RED),
        (12, 11.65, 51.20, "잘레운스트루트", "Saale-Unstrut", "최북단급", C_WHITE),
        (13, 13.60, 51.10, "작센", "Sachsen", "최동단 · 최소", C_WHITE),
    ]
    numbered(m, items, footer_h=125, col_w=340, rows_per_col=5, sub_dx=318)

    cities(m, [(13.40, 52.52, "Berlin", 10, 3.5), (8.68, 50.11, "Frankfurt", 10, -6),
               (11.58, 48.14, "München", 10, 3.5), (6.96, 50.94, "Köln", -10, 3.5),
               (9.99, 53.55, "Hamburg", 10, 3.5), (8.40, 49.01, "Karlsruhe", -10, 3.5)])
    m.legend([(C_WHITE, "화이트 중심"), (C_RED, "레드 비중 높음")],
             title="주력", x=16, y=m.h - 200, w=160)
    m.save("germany-overview.svg")


# ======================================================================== 지도 2
def map_mosel():
    m = Map((6.45, 49.52, 7.30, 50.10), 760, pad=16,
            title="모젤 — 사르 · 루버 · 미텔모젤",
            subtitle="Mosel : 강이 굽이칠 때마다 남향 급경사가 생긴다. 경사 최대 65도")
    m.base(rivers=["Mosel"], shapes=[GERMANY], river_src=RIVERS_DE, river_w=5.0)

    # 사르·루버 지류
    for path in ([(6.58, 49.55), (6.60, 49.62), (6.58, 49.68), (6.64, 49.75)],
                 [(6.82, 49.80), (6.75, 49.78), (6.70, 49.77)]):
        m.add('<path d="%s" fill="none" stroke="#9dc0da" stroke-width="3.4" '
              'stroke-linecap="round"/>' % m.path(path, close=False))

    # 미텔모젤 최상급 벨트
    m.belt([(6.93, 49.88), (6.99, 49.90), (7.02, 49.93), (7.06, 49.94), (7.02, 49.96),
            (6.98, 49.99)], C_WHITE, width=13, opacity=0.34)

    villages = [
        (6.93, 49.875, "Piesport 피스포르트", C_WHITE, -10, 4),
        (6.99, 49.898, "Brauneberg 브라우네베르크", C_WHITE, 10, -4),
        (7.07, 49.918, "Bernkastel 베른카스텔", C_WHITE, 10, 12),
        (7.02, 49.932, "Wehlen 벨렌", C_WHITE, -10, 2),
        (7.06, 49.943, "Graach 그라흐", C_WHITE, 10, 2),
        (7.02, 49.962, "Zeltingen 첼팅겐", C_WHITE, -10, -4),
        (6.98, 49.990, "Ürzig 위르치히", C_WHITE, -10, 4),
        (6.96, 50.000, "Erden 에르덴", C_WHITE, -10, 14),
        (7.11, 49.952, "Traben-Trarbach 트라벤트라르바흐", C_WHITE, 10, 4),
        (7.02, 49.870, "Trittenheim 트리텐하임", C_WHITE, -10, 10),
    ]
    saar_ruwer = [
        (6.585, 49.665, "Wiltingen 빌팅겐", C_SPARK, -10, 2),
        (6.625, 49.622, "Ockfen 오크펜", C_SPARK, 10, 2),
        (6.575, 49.585, "Serrig 제리히", C_SPARK, -10, 4),
        (6.578, 49.685, "Kanzem 칸쳄", C_SPARK, -10, -6),
        (6.752, 49.777, "Kasel 카젤 (Ruwer 루버)", C_GREEN, 10, 2),
    ]
    for lon, lat, name, color, dx, dy in villages + saar_ruwer:
        m.pin(lon, lat, name, dx=dx, dy=dy, color=color, r=4.4, size=11)

    cities(m, [(6.64, 49.756, "Trier", -11, -8), (7.00, 49.90, "", 0, 0)])
    m.legend([(C_WHITE, "미텔모젤 — 청회색 편암, 최상급 밭"),
              (C_SPARK, "사르 Saar — 가장 서늘, 고산도"),
              (C_GREEN, "루버 Ruwer — 최소 지류")],
             title="세 구역", x=16, y=m.h - 92, w=280)
    m.save("mosel.svg")


# ======================================================================== 지도 3
def map_rhein():
    m = Map((7.55, 49.10, 8.85, 50.20), 700, pad=16,
            title="라인 — 라인가우 · 라인헤센 · 나에 · 팔츠",
            subtitle="라인 강이 서쪽으로 꺾이는 구간(Rheingau)에서 남향 사면이 만들어진다")
    m.base(rivers=["Rhein", "Nahe", "Main"], shapes=[GERMANY], river_src=RIVERS_DE, river_w=4.4)

    m.belt([(7.93, 50.00), (8.05, 50.00), (8.15, 50.00), (8.25, 50.01)],
           C_WHITE, width=13, opacity=0.34)   # 라인가우
    m.belt([(8.10, 49.75), (8.25, 49.85), (8.35, 49.90)], C_GREEN, width=12, opacity=0.28)
    m.belt([(8.10, 49.20), (8.15, 49.35), (8.20, 49.50)], C_RED, width=12, opacity=0.26)

    pts = [
        (7.92, 49.980, "Rüdesheim 뤼데스하임", C_WHITE, -10, 2),
        (7.98, 49.995, "Johannisberg 요하니스베르크", C_WHITE, -10, -8),
        (8.01, 50.000, "Winkel 빙켈", C_WHITE, 10, -12),
        (8.05, 50.005, "Oestrich 외스트리히", C_WHITE, 10, -2),
        (8.09, 50.008, "Hattenheim 하텐하임", C_WHITE, 10, 10),
        (8.13, 50.010, "Erbach 에르바흐", C_WHITE, 10, 22),
        (8.20, 50.020, "Kiedrich 키드리히", C_WHITE, 10, -14),
        (8.25, 50.030, "Rauenthal 라우엔탈", C_WHITE, 10, -2),
        (8.30, 50.010, "Hochheim 호흐하임", C_WHITE, 10, 10),
        (8.36, 49.870, "Nierstein 니어슈타인", C_GREEN, 10, 2),
        (8.34, 49.830, "Oppenheim 오펜하임", C_GREEN, 10, 12),
        (8.10, 49.700, "Westhofen 베스트호펜", C_GREEN, -10, 2),
        (8.05, 49.755, "Nierstein 권역", C_GREEN, 0, 0),
        (7.62, 49.845, "Schlossböckelheim 슐로스뵈켈하임", C_SPARK, -10, 2),
        (7.87, 49.950, "Bingen 빙겐", C_SPARK, -10, -4),
        (8.17, 49.470, "Kallstadt 칼슈타트", C_RED, -10, 2),
        (8.16, 49.420, "Forst 포르스트", C_RED, -10, 12),
        (8.15, 49.390, "Deidesheim 다이데스하임", C_RED, -10, 22),
        (8.13, 49.330, "Ruppertsberg 루페르츠베르크", C_RED, -10, 32),
    ]
    for lon, lat, name, color, dx, dy in pts:
        if not name or name.endswith("권역"):
            continue
        m.pin(lon, lat, name, dx=dx, dy=dy, color=color, r=4.2, size=10.8)

    cities(m, [(8.27, 50.00, "Mainz", 10, 16), (8.40, 49.01, "Karlsruhe", 0, 14),
               (8.44, 49.49, "Speyer", 10, 3.5)])
    m.legend([(C_WHITE, "라인가우 Rheingau — 남향 사면"),
              (C_GREEN, "라인헤센 Rheinhessen — 최대 면적"),
              (C_SPARK, "나에 Nahe — 지질 다양"),
              (C_RED, "팔츠 Pfalz — 온난, 미텔하르트")],
             title="네 산지", x=16, y=m.h - 110, w=290)
    m.save("rhein.svg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    map_germany()
    map_mosel()
    map_rhein()
