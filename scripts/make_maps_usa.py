#!/usr/bin/env python3
"""미국 와인 산지 지도(SVG) 생성기.

make_maps.py 의 Map 클래스(경위도 → 픽셀 투영)를 재사용한다.
실행: python3 scripts/make_maps_usa.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from make_maps import (  # noqa: E402
    OUT, FONT, Map, esc,
    C_BG, C_LAND, C_LAND_ED, C_WATER, C_TEXT, C_SUB,
    C_RED, C_WHITE, C_SPARK, C_GREEN, C_PURPLE,
)

# ------------------------------------------------------------------ 국경 윤곽
USA = [
    # 태평양 연안 (북 → 남)
    (-124.70, 48.40), (-124.60, 47.30), (-124.10, 46.90), (-124.00, 46.30),
    (-124.00, 45.50), (-124.10, 44.60), (-124.40, 43.30), (-124.40, 42.40),
    (-124.20, 41.80), (-124.10, 40.40), (-123.80, 39.40), (-123.00, 38.30),
    (-122.50, 37.80), (-122.40, 37.20), (-121.90, 36.60), (-121.30, 35.70),
    (-120.60, 34.90), (-120.50, 34.45), (-119.70, 34.40), (-118.50, 34.02),
    (-118.20, 33.72), (-117.30, 33.10), (-117.13, 32.53),
    # 멕시코 국경 (서 → 동)
    (-114.72, 32.72), (-111.00, 31.33), (-108.20, 31.33), (-106.50, 31.80),
    (-104.90, 29.30), (-103.10, 28.98), (-102.30, 29.88), (-101.40, 29.77),
    (-100.00, 28.20), (-99.10, 26.40), (-97.40, 25.90),
    # 멕시코만 (서 → 동)
    (-97.40, 27.90), (-95.30, 28.93), (-93.80, 29.70), (-91.50, 29.20),
    (-90.00, 29.20), (-89.20, 30.30), (-88.00, 30.40), (-87.20, 30.40),
    (-85.60, 30.00), (-84.30, 30.00), (-83.00, 29.10), (-82.70, 27.90),
    (-81.80, 26.00), (-80.90, 25.20), (-80.10, 25.60),
    # 대서양 연안 (남 → 북)
    (-80.10, 26.90), (-80.60, 28.50), (-81.40, 30.30), (-80.90, 32.00),
    (-79.90, 32.80), (-78.00, 33.90), (-75.50, 35.20), (-76.00, 36.90),
    (-75.90, 37.20), (-75.10, 38.50), (-74.90, 38.90), (-74.00, 40.00),
    (-73.00, 41.00), (-71.90, 41.30), (-70.70, 41.70), (-70.00, 41.80),
    (-70.90, 42.40), (-70.70, 43.10), (-69.80, 43.80), (-68.00, 44.30),
    (-67.00, 44.80), (-67.80, 45.70),
    # 캐나다 국경 (동 → 서)
    (-69.20, 47.45), (-70.30, 45.90), (-71.50, 45.02), (-74.70, 45.02),
    (-76.90, 43.60), (-79.00, 43.30), (-79.10, 42.80), (-81.00, 42.30),
    (-83.10, 42.00), (-82.40, 43.00), (-82.50, 45.30), (-84.00, 46.50),
    (-84.60, 46.50), (-88.40, 48.30), (-89.50, 48.00), (-92.00, 48.40),
    (-95.20, 49.00), (-104.00, 49.00), (-116.00, 49.00), (-123.00, 49.00),
    (-123.20, 48.40),
]

CALIFORNIA = [
    (-124.21, 42.00), (-124.10, 40.40), (-123.83, 39.75), (-123.72, 39.10),
    (-123.60, 38.90), (-123.40, 38.70), (-123.32, 38.55), (-123.05, 38.32),
    (-122.98, 38.11), (-122.83, 37.99), (-122.53, 37.83), (-122.40, 37.20),
    (-121.90, 36.60), (-121.30, 35.70),
    (-120.60, 34.90), (-120.50, 34.45), (-119.70, 34.40), (-118.50, 34.02),
    (-118.20, 33.72), (-117.30, 33.10), (-117.13, 32.53), (-114.72, 32.72),
    (-114.63, 34.30), (-114.63, 35.00), (-114.57, 35.15), (-120.00, 39.00),
    (-120.00, 42.00),
]

OREGON = [
    (-124.55, 42.00), (-124.40, 43.30), (-124.10, 44.60), (-124.00, 45.50),
    (-123.90, 46.20), (-123.40, 46.20), (-122.80, 45.65), (-121.90, 45.65),
    (-121.00, 45.65), (-119.60, 45.93), (-119.00, 46.00), (-116.92, 45.99),
    (-116.90, 45.00), (-117.00, 44.30), (-117.23, 44.00), (-117.03, 43.80),
    (-117.03, 42.00),
]

WASHINGTON = [
    (-124.70, 48.40), (-124.60, 47.30), (-124.10, 46.90), (-124.00, 46.30),
    (-123.90, 46.20), (-123.40, 46.20), (-122.80, 45.65), (-121.90, 45.65),
    (-121.00, 45.65), (-119.60, 45.93), (-119.00, 46.00), (-116.92, 45.99),
    (-117.03, 49.00), (-122.80, 49.00), (-123.10, 48.20),
]

# -------------------------------------------------------------------- 하천망
RIVERS_US = {
    "Columbia": [(-117.03, 49.00), (-118.20, 47.80), (-119.30, 47.00), (-119.90, 46.60),
                 (-119.30, 46.10), (-120.50, 45.70), (-121.90, 45.65), (-122.80, 45.65),
                 (-123.90, 46.20)],
    "Snake": [(-117.03, 44.50), (-116.90, 45.80), (-117.50, 46.10), (-118.50, 46.20),
              (-119.05, 46.20)],
    "Willamette": [(-123.30, 44.00), (-123.10, 44.60), (-123.00, 45.00), (-122.80, 45.30),
                   (-122.70, 45.65)],
    "Yakima": [(-121.50, 47.00), (-120.50, 46.60), (-120.00, 46.40), (-119.45, 46.22)],
    "Sacramento": [(-122.30, 40.60), (-122.00, 39.50), (-121.80, 38.80), (-121.60, 38.20),
                   (-121.90, 38.10), (-122.35, 38.05)],
    "SanJoaquin": [(-119.70, 36.80), (-120.40, 37.10), (-121.00, 37.60), (-121.50, 37.95),
                   (-121.90, 38.05)],
    "Colorado": [(-114.63, 36.00), (-114.63, 35.00), (-114.63, 34.30), (-114.72, 32.72)],
    "Mississippi": [(-95.20, 46.50), (-92.00, 44.00), (-90.60, 41.50), (-90.20, 38.70),
                    (-89.60, 36.50), (-91.00, 34.50), (-91.20, 32.50), (-91.30, 30.50),
                    (-90.00, 29.20)],
    "Hudson": [(-73.80, 43.30), (-73.90, 42.30), (-73.95, 41.30), (-74.00, 40.70)],
}


def cities(m, pts, size=11):
    for lon, lat, name, dx, dy in pts:
        m.square(lon, lat)
        m.label(lon, lat, name, dx=dx, dy=dy, size=size, fill=C_SUB,
                anchor="middle" if dx == 0 else ("start" if dx > 0 else "end"))


def numbered(m, items, footer_h, cols, col_w, rows_per_col, name_dx=15, sub_dx=None):
    """번호 마커 + 하단 범례. items = (n, lon, lat, 한글, 원어, 보조설명, 색)"""
    m.footer_h = footer_h
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
def map_usa():
    m = Map((-125.5, 24.5, -66.0, 49.8), 900, pad=14,
            title="미국 주요 와인 산지",
            subtitle="American Viticultural Areas — 50개 주 전역에서 생산, 캘리포니아가 약 81%")
    m.base(rivers=list(RIVERS_US.keys()), shapes=[USA], river_src=RIVERS_US, river_w=1.6)

    regions = [
        (-122.60, 38.50, "나파 · 소노마 (노스 코스트)", C_RED, 11, -4),
        (-121.00, 38.40, "시에라 풋힐 · 로다이", C_RED, 11, 14),
        (-120.80, 35.60, "센트럴 코스트 Central Coast", C_RED, 11, 4),
        (-120.35, 34.70, "산타바버라 Santa Barbara", C_RED, 11, 9),
        (-123.05, 45.20, "윌라멧 밸리 Willamette", C_RED, 11, 16),
        (-119.60, 46.60, "컬럼비아 밸리 Columbia Valley", C_RED, 11, -4),
        (-118.30, 46.00, "왈라왈라 Walla Walla", C_RED, 11, 12),
        (-116.50, 43.60, "스네이크 리버 Snake River", C_WHITE, 11, 4),
        (-110.00, 32.00, "애리조나 Arizona", C_RED, 11, 4),
        (-106.00, 34.50, "뉴멕시코 New Mexico", C_SPARK, 11, 4),
        (-101.90, 33.60, "텍사스 하이플레인스", C_RED, 11, 4),
        (-98.90, 30.30, "텍사스 힐 컨트리", C_RED, 11, 4),
        (-85.60, 44.90, "미시간 Michigan", C_WHITE, -11, 4),
        (-77.00, 42.65, "핑거레이크스 Finger Lakes", C_WHITE, -11, -6),
        (-72.50, 40.95, "롱아일랜드 Long Island", C_RED, -11, 22),
        (-78.30, 38.05, "버지니아 Virginia", C_RED, 11, 4),
    ]
    for lon, lat, name, color, dx, dy in regions:
        if not name:
            continue
        m.pin(lon, lat, name, dx=dx, dy=dy, color=color, r=5.0, size=11.5)

    cities(m, [(-87.63, 41.88, "Chicago", 0, -10),
               (-74.01, 40.71, "New York", 10, 4),
               (-95.37, 29.76, "Houston", 0, 14),
               (-104.99, 39.74, "Denver", 0, -10)])

    m.legend([(C_RED, "레드 중심"), (C_WHITE, "화이트 중심"), (C_SPARK, "스파클링")],
             title="주요 스타일", x=16, y=m.h - 100, w=168)
    m.save("usa-overview.svg")


# ======================================================================== 지도 2
def map_california():
    m = Map((-124.8, 32.2, -113.8, 42.3), 620, pad=16,
            title="캘리포니아 — 주요 AVA",
            subtitle="California : 미국 와인 생산량의 약 81%, AVA 약 150개")
    m.base(rivers=["Sacramento", "SanJoaquin", "Colorado"], shapes=[CALIFORNIA],
           river_src=RIVERS_US, river_w=2.4)

    # 해안 산맥·센트럴 밸리 벨트
    m.belt([(-123.00, 39.10), (-122.60, 38.60), (-122.30, 38.30)], C_RED, width=13, opacity=0.42)
    m.belt([(-122.10, 37.20), (-121.60, 36.60), (-121.10, 35.90), (-120.50, 35.10),
            (-120.10, 34.60)], C_RED, width=11, opacity=0.34)
    m.belt([(-121.30, 38.60), (-120.80, 38.40), (-120.50, 38.20)], C_RED, width=11, opacity=0.34)

    items = [
        (1, -122.40, 38.50, "나파 밸리", "Napa Valley", "카베르네 소비뇽", C_RED),
        (2, -122.90, 38.55, "소노마 카운티", "Sonoma County", "피노 누아 · 진판델", C_RED),
        (3, -122.32, 38.13, "로스 카네로스", "Los Carneros", "서늘 · 스파클링", C_SPARK),
        (4, -123.40, 39.05, "앤더슨 밸리", "Anderson Valley", "피노 누아 · 스파클링", C_SPARK),
        (5, -122.10, 37.15, "산타크루즈 산맥", "Santa Cruz Mts.", "리지 몬테 벨로", C_RED),
        (6, -121.75, 37.68, "리버모어 밸리", "Livermore Valley", "샤르도네 클론 발상지", C_WHITE),
        (7, -121.35, 36.30, "산타루시아 하이랜즈", "Santa Lucia Highlands", "피노 누아 · 시라", C_RED),
        (8, -120.90, 35.65, "파소 로블스", "Paso Robles", "론 품종 · 카베르네", C_RED),
        (9, -120.72, 35.30, "에드나 밸리", "Edna Valley", "샤르도네", C_WHITE),
        (10, -120.44, 35.02, "산타마리아 밸리", "Santa Maria Valley", "비앙 나시도 밭", C_RED),
        (11, -120.48, 34.60, "스타 리타 힐스", "Sta. Rita Hills", "피노 누아", C_RED),
        (12, -119.98, 34.70, "산타이네스 밸리", "Santa Ynez Valley", "시라 · 보르도 품종", C_RED),
        (13, -120.60, 38.72, "시에라 풋힐", "Sierra Foothills", "고목 진판델", C_RED),
        (14, -121.25, 38.13, "로다이", "Lodi", "고목 진판델", C_RED),
        (15, -122.35, 40.20, "노스 코스트 북부", "Lake / Red Hills", "카베르네", C_RED),
    ]
    numbered(m, items, footer_h=332, cols=1, col_w=560, rows_per_col=15, sub_dx=556)

    cities(m, [(-122.42, 37.77, "San Francisco", -11, 3.5),
               (-118.24, 34.05, "Los Angeles", -11, 3.5),
               (-117.16, 32.72, "San Diego", -11, 3.5)])
    m.save("california.svg")


# ======================================================================== 지도 3
def map_napa_sonoma():
    m = Map((-123.45, 37.98, -122.05, 38.95), 900, pad=16,
            title="나파 · 소노마 — 하위 AVA 배치",
            subtitle="Napa (16개 하위 AVA) / Sonoma (19개 AVA) · 태평양 안개가 남서쪽에서 밀려든다")
    m.base(rivers=[], shapes=[CALIFORNIA], river_src=RIVERS_US)

    # 산맥 표시 — 마야카마스(나파·소노마 사이), 바카(나파 동쪽)
    m.belt([(-122.62, 38.30), (-122.50, 38.45), (-122.40, 38.62)], "#8a7f72", width=17,
           opacity=0.30)
    m.belt([(-122.24, 38.28), (-122.28, 38.48), (-122.42, 38.66)], "#8a7f72", width=15,
           opacity=0.26)
    x, y = m.xy(-122.660, 38.470)
    m.text_px(x, y, "마야카마스 산맥", size=10.5, fill="#6b6157", weight="600", anchor="middle")
    x, y = m.xy(-122.150, 38.560)
    m.text_px(x, y, "바카 산맥", size=10.5, fill="#6b6157", weight="600", anchor="middle")

    # 샌파블로 만(안개 유입구)
    m.poly([(-122.56, 38.16), (-122.34, 38.19), (-122.16, 38.14), (-122.09, 37.96),
            (-122.62, 37.96)], C_WATER, opacity=0.55)
    ax, ay = m.xy(-122.34, 38.20)
    m.add('<path d="M %.1f %.1f L %.1f %.1f" stroke="%s" stroke-width="3" fill="none" '
          'opacity="0.7"/>' % (ax, ay, ax - 26, ay - 96, "#5f92b5"))
    m.add('<path d="M %.1f %.1f l 5 11 l -11 -2 Z" fill="%s" opacity="0.8"/>'
          % (ax - 27, ay - 100, "#5f92b5"))
    x, y = m.xy(-122.35, 38.070)
    m.text_px(x, y, "샌파블로 만 — 여기서 안개가 밀려 올라간다", size=10.5, fill="#3f6a8a", weight="600",
              anchor="middle")

    napa = [
        (1, -122.350, 38.230, "로스 카네로스", "Los Carneros", "가장 서늘 · 스파클링"),
        (2, -122.245, 38.300, "쿰스빌", "Coombsville", "서늘 · 신선"),
        (3, -122.200, 38.320, "와일드 호스 밸리", "Wild Horse Valley", "극소 면적"),
        (4, -122.320, 38.360, "오크 놀 디스트릭트", "Oak Knoll District", "전이 지대"),
        (5, -122.362, 38.400, "용트빌", "Yountville", "우아 · 균형"),
        (6, -122.318, 38.425, "스택스 립 디스트릭트", "Stags Leap District", "벨벳 탄닌"),
        (7, -122.410, 38.440, "오크빌", "Oakville", "투 칼론 · 최상급"),
        (8, -122.432, 38.470, "러더퍼드", "Rutherford", "러더퍼드 더스트"),
        (9, -122.470, 38.510, "세인트 헬레나", "St. Helena", "가장 따뜻한 계곡 바닥"),
        (10, -122.580, 38.585, "칼리스토가", "Calistoga", "최북 · 최고온"),
        (11, -122.470, 38.395, "마운트 비더", "Mount Veeder", "서쪽 산지 · 척박"),
        (12, -122.550, 38.535, "스프링 마운틴", "Spring Mountain District", "서쪽 산지"),
        (13, -122.615, 38.575, "다이아몬드 마운틴", "Diamond Mountain District", "화산토"),
        (14, -122.410, 38.575, "하웰 마운틴", "Howell Mountain", "안개 위 · 강한 탄닌"),
        (15, -122.245, 38.450, "아틀라스 피크", "Atlas Peak", "동쪽 산지 · 고도"),
        (16, -122.310, 38.560, "칠레스 밸리", "Chiles Valley District", "동쪽 내륙 · 서늘"),
    ]
    sonoma = [
        (17, -122.460, 38.300, "소노마 밸리", "Sonoma Valley", "소노마의 원조"),
        (18, -122.555, 38.325, "소노마 마운틴", "Sonoma Mountain", "로렐 글렌"),
        (19, -122.420, 38.345, "문 마운틴", "Moon Mountain District", "화산토 사면"),
        (20, -122.615, 38.395, "베넷 밸리", "Bennett Valley", "서늘 · 소규모"),
        (21, -122.720, 38.220, "페탈루마 갭", "Petaluma Gap", "강풍 · 시라/피노"),
        (22, -122.860, 38.470, "러시안 리버 밸리", "Russian River Valley", "피노 누아 중심지"),
        (23, -122.920, 38.415, "그린 밸리", "Green Valley of RRV", "가장 서늘 · 골드리지 토양"),
        (24, -122.780, 38.610, "초크 힐", "Chalk Hill", "화산재 토양"),
        (25, -122.700, 38.525, "파운틴그로브", "Fountaingrove District", "산지"),
        (26, -123.000, 38.680, "드라이 크리크 밸리", "Dry Creek Valley", "진판델의 성지"),
        (27, -122.860, 38.760, "알렉산더 밸리", "Alexander Valley", "카베르네 · 따뜻함"),
        (28, -122.720, 38.690, "나이츠 밸리", "Knights Valley", "가장 따뜻 · 카베르네"),
        (29, -123.100, 38.760, "록파일", "Rockpile", "고지대 · 진판델"),
        (30, -123.050, 38.850, "파인 마운틴", "Pine Mtn-Cloverdale Peak", "최고 고도"),
        (31, -123.230, 38.560, "포트 로스-시뷰", "Fort Ross-Seaview", "해안 절벽 · 안개 위"),
        (32, -123.180, 38.400, "웨스트 소노마 코스트", "West Sonoma Coast", "2022 신설"),
    ]
    for n, lon, lat, ko, en, sub in napa:
        x, y = m.xy(lon, lat)
        m.add('<circle cx="%.1f" cy="%.1f" r="10.5" fill="%s" stroke="%s" stroke-width="1.6"/>'
              % (x, y, C_RED, C_BG))
        m.text_px(x, y + 4, str(n), size=12, fill="#fff", anchor="middle", weight="700",
                  halo=False)
    for n, lon, lat, ko, en, sub in sonoma:
        x, y = m.xy(lon, lat)
        m.add('<circle cx="%.1f" cy="%.1f" r="10.5" fill="%s" stroke="%s" stroke-width="1.6"/>'
              % (x, y, "#4a6b8a", C_BG))
        m.text_px(x, y + 4, str(n), size=12, fill="#fff", anchor="middle", weight="700",
                  halo=False)

    footer_h = 372
    m.h += footer_h
    fy = m.h - footer_h + 6
    m.add('<rect x="14" y="%.1f" width="%.1f" height="%.1f" fill="#ffffff" '
          'fill-opacity="0.92" stroke="%s" rx="4"/>' % (fy, m.w - 28, footer_h - 20, C_LAND_ED))
    m.text_px(32, fy + 22, "나파 밸리 AVA (16)", size=12.5, weight="700", fill=C_RED, halo=False)
    m.text_px(462, fy + 22, "소노마 카운티 AVA (주요 16)", size=12.5, weight="700",
              fill="#4a6b8a", halo=False)
    for group, color, bx0 in [(napa, C_RED, 32), (sonoma, "#4a6b8a", 462)]:
        for i, (n, lon, lat, ko, en, sub) in enumerate(group):
            by = fy + 46 + i * 19.5
            m.add('<circle cx="%.1f" cy="%.1f" r="8" fill="%s"/>' % (bx0, by - 4, color))
            m.text_px(bx0, by, str(n), size=10.5, fill="#fff", anchor="middle", weight="700",
                      halo=False)
            m.text_px(bx0 + 15, by, "%s %s" % (ko, en), size=11, weight="600", halo=False)
            m.text_px(bx0 + 390, by, sub, size=10.5, fill=C_SUB, anchor="end", halo=False)
    m.save("napa-sonoma.svg")


# ======================================================================== 지도 4
def map_napa_strip():
    """나파 밸리 16개 하위 AVA — 남(서늘) → 북(고온), 계곡 바닥 / 산지 구분."""
    W, TOP, ROW = 1120, 100, 31.0
    rows = [
        ("로스 카네로스 Los Carneros", "F", "1983", "샤르도네 · 피노 누아 · 스파클링",
         "만 바로 옆 · 나파에서 가장 서늘"),
        ("쿰스빌 Coombsville", "F", "2011", "카베르네 · 샤르도네", "신선한 산도 · 최근 재평가"),
        ("와일드 호스 밸리 Wild Horse Valley", "M", "1988", "피노 누아 · 샤르도네", "극소 면적"),
        ("오크 놀 디스트릭트 Oak Knoll District", "F", "2004", "카베르네 · 샤르도네 · 리슬링",
         "서늘~온난 전이 지대"),
        ("용트빌 Yountville", "F", "1999", "카베르네 소비뇽", "도미누스 · 우아한 구조"),
        ("스택스 립 디스트릭트 Stags Leap District", "F", "1989", "카베르네 소비뇽",
         "\"벨벳 장갑 속 철권\" · 1976 파리의 심판"),
        ("오크빌 Oakville", "F", "1993", "카베르네 소비뇽", "투 칼론 · 나파의 심장"),
        ("러더퍼드 Rutherford", "F", "1993", "카베르네 소비뇽", "\"러더퍼드 더스트\" · 흙 뉘앙스"),
        ("세인트 헬레나 St. Helena", "F", "1995", "카베르네 소비뇽", "계곡이 좁아져 열이 갇힘"),
        ("칼리스토가 Calistoga", "F", "2010", "카베르네 소비뇽 · 프티 시라",
         "최북 · 최고온 · 일교차 최대"),
        ("마운트 비더 Mount Veeder", "M", "1993", "카베르네 · 샤르도네",
         "마야카마스 서쪽 · 척박한 해양 퇴적토"),
        ("스프링 마운틴 Spring Mountain District", "M", "1993", "카베르네 · 소비뇽 블랑",
         "서쪽 산지 · 서늘하고 습함"),
        ("다이아몬드 마운틴 Diamond Mountain District", "M", "2001", "카베르네 소비뇽",
         "화산토 · 다이아몬드 크릭"),
        ("하웰 마운틴 Howell Mountain", "M", "1983", "카베르네 · 진판델",
         "안개 위(400 m+) · 나파에서 가장 강건한 탄닌"),
        ("아틀라스 피크 Atlas Peak", "M", "1992", "카베르네 소비뇽",
         "바카 산맥 동쪽 · 화산토 · 고도"),
        ("칠레스 밸리 Chiles Valley District", "M", "1999", "진판델 · 카베르네",
         "동쪽 내륙 계곡 · 서늘하고 늦게 익음"),
    ]
    H = TOP + len(rows) * ROW + 52
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
         'role="img"><rect width="100%%" height="100%%" fill="%s"/>' % (W, H, W, H, C_BG)]
    o.append('<text x="20" y="28" font-size="18" font-weight="700" fill="%s" font-family="%s">'
             '나파 밸리 — 16개 하위 AVA (남 → 북)</text>' % (C_TEXT, FONT))
    o.append('<text x="20" y="48" font-size="12.5" fill="%s" font-family="%s">'
             'Napa Valley AVA (1981) 안에 16개 하위 AVA가 중첩된다 · 괄호 안은 지정 연도</text>'
             % (C_SUB, FONT))
    o.append('<text x="20" y="72" font-size="11.5" fill="%s" font-family="%s">'
             '남쪽 샌파블로 만에서 안개가 들어와 북쪽으로 갈수록 더워진다 — '
             '카네로스(서늘) → 칼리스토가(고온) · 산지 AVA는 안개 위에 있어 별개 기후</text>'
             % (C_SUB, FONT))

    xl, c1, c2, c3 = 20, 300, 356, 620
    for i, (name, kind, year, grapes, note) in enumerate(rows):
        y = TOP + i * ROW
        cy = y + ROW / 2
        o.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="%s"/>'
                 % (xl, y, W - 40, ROW, "#f4efe6" if i % 2 == 0 else "#ffffff"))
        acc = C_RED if kind == "F" else "#5b7f4f"
        o.append('<rect x="%d" y="%.1f" width="5" height="%.1f" fill="%s"/>' % (xl, y, ROW, acc))
        o.append('<text x="%d" y="%.1f" font-size="12.5" font-weight="700" fill="%s" '
                 'font-family="%s">%s</text>' % (xl + 15, cy + 4, C_TEXT, FONT, esc(name)))
        o.append('<text x="%d" y="%.1f" font-size="10.5" fill="%s" font-family="%s">%s</text>'
                 % (xl + c1, cy + 4, C_SUB, FONT, year))
        o.append('<text x="%d" y="%.1f" font-size="11.5" fill="%s" font-family="%s">%s</text>'
                 % (xl + c2, cy + 4, C_TEXT, FONT, esc(grapes)))
        o.append('<text x="%d" y="%.1f" font-size="11" fill="%s" font-family="%s">%s</text>'
                 % (xl + c3, cy + 4, "#8a7f72", FONT, esc(note)))

    yl = TOP + len(rows) * ROW + 30
    o.append('<circle cx="30" cy="%.1f" r="5" fill="%s"/>' % (yl - 4, C_RED))
    o.append('<text x="42" y="%.1f" font-size="11.5" fill="%s" font-family="%s">'
             '계곡 바닥 (Valley Floor)</text>' % (yl, C_TEXT, FONT))
    o.append('<circle cx="212" cy="%.1f" r="5" fill="#5b7f4f"/>' % (yl - 4))
    o.append('<text x="224" y="%.1f" font-size="11.5" fill="%s" font-family="%s">'
             '산지 (Mountain AVA)</text>' % (yl, C_TEXT, FONT))
    o.append('<text x="420" y="%.1f" font-size="11.5" fill="%s" font-family="%s">'
             'AVA는 경계만 규정할 뿐 품종·수확량·양조법을 제한하지 않는다</text>'
             % (yl, C_SUB, FONT))
    o.append("</svg>")
    p = os.path.join(OUT, "napa-ava-strip.svg")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    print("wrote", p)


# ======================================================================== 지도 5
def map_pnw():
    m = Map((-124.9, 41.8, -116.4, 49.2), 860, pad=16,
            title="태평양 북서부 — 오리건 / 워싱턴",
            subtitle="캐스케이드 산맥 서쪽은 서늘·습윤(피노 누아), 동쪽은 건조 사막(카베르네·시라)")
    m.base(rivers=["Columbia", "Snake", "Willamette", "Yakima"],
           shapes=[OREGON, WASHINGTON], river_src=RIVERS_US, river_w=3.4)

    # 캐스케이드 산맥
    m.belt([(-121.80, 48.80), (-121.60, 47.40), (-121.60, 46.20), (-121.75, 45.30),
            (-121.90, 44.20), (-122.10, 43.00), (-122.20, 42.10)], "#8a7f72",
           width=9, opacity=0.30)
    x, y = m.xy(-121.55, 48.90)
    m.text_px(x, y, "캐스케이드 산맥", size=11, fill="#6b6157", weight="700", anchor="middle")
    x, y = m.xy(-123.30, 47.60)
    m.text_px(x, y, "서쪽 : 서늘·습윤", size=11, fill="#5b7f4f", weight="700", anchor="middle")
    x, y = m.xy(-119.00, 48.40)
    m.text_px(x, y, "동쪽 : 건조 사막 (연 강수 200 mm)", size=11, fill="#a05a3a",
              weight="700", anchor="middle")

    items = [
        (1, -123.05, 45.25, "윌라멧 밸리", "Willamette Valley", "피노 누아 · 하위 AVA 11개", C_RED),
        (2, -123.35, 45.05, "맥민빌", "McMinnville", "해양 퇴적 · 구조적", C_RED),
        (3, -123.20, 44.92, "에올라-에이미티 힐스", "Eola-Amity Hills", "반 두저 바람길", C_RED),
        (4, -123.35, 43.30, "엄프콰 밸리", "Umpqua Valley", "템프라니요 · 남부 오리건", C_RED),
        (5, -123.00, 42.35, "로그 · 애플게이트", "Rogue / Applegate", "따뜻 · 보르도 품종", C_RED),
        (6, -121.50, 45.70, "컬럼비아 고지", "Columbia Gorge", "협곡 · 기후 급변", C_WHITE),
        (7, -119.60, 46.62, "컬럼비아 밸리", "Columbia Valley", "워싱턴 생산의 99%", C_RED),
        (8, -120.20, 46.35, "야키마 밸리", "Yakima Valley", "워싱턴 최고(最古) AVA", C_RED),
        (9, -119.45, 46.28, "레드 마운틴", "Red Mountain", "최고가 카베르네", C_RED),
        (10, -118.35, 46.05, "왈라왈라 밸리", "Walla Walla Valley", "주 경계를 넘는 AVA", C_RED),
        (11, -118.58, 45.92, "더 록스 디스트릭트", "The Rocks District", "현무암 자갈 · 시라", C_PURPLE),
        (12, -119.85, 45.92, "호스 헤븐 힐스", "Horse Heaven Hills", "챔푸 밭", C_RED),
        (13, -119.85, 46.88, "왈루크 슬로프", "Wahluke Slope", "가장 따뜻 · 건조", C_RED),
        (14, -119.95, 47.25, "에인션트 레이크스", "Ancient Lakes", "리슬링 · 화이트", C_WHITE),
        (15, -120.05, 47.85, "레이크 첼란", "Lake Chelan", "호수 완충 효과", C_WHITE),
        (16, -122.60, 48.35, "퓨젓 사운드", "Puget Sound", "캐스케이드 서쪽 유일", C_WHITE),
    ]
    numbered(m, items, footer_h=192, cols=2, col_w=410, rows_per_col=8, sub_dx=388)

    cities(m, [(-122.68, 45.52, "Portland", -11, 3.5), (-122.33, 47.61, "Seattle", -11, 3.5),
               (-119.28, 46.23, "Tri-Cities", 11, 3.5), (-123.26, 44.56, "Corvallis", -11, 3.5)])
    m.save("pacific-northwest.svg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    map_usa()
    map_california()
    map_napa_sonoma()
    map_napa_strip()
    map_pnw()
