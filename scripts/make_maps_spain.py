#!/usr/bin/env python3
"""스페인 와인 산지 지도(SVG) 생성기.

make_maps.py 의 Map 클래스(경위도 → 픽셀 투영)를 재사용한다.
실행: python3 scripts/make_maps_spain.py
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
# 이베리아 반도(스페인 + 포르투갈)를 하나의 육지로 그린다.
IBERIA = [
    # 칸타브리아 해안 (서 → 동)
    (-7.70, 43.79), (-7.05, 43.72), (-6.50, 43.57), (-5.70, 43.55), (-4.90, 43.48),
    (-4.10, 43.42), (-3.80, 43.45), (-3.00, 43.42), (-2.20, 43.32), (-1.79, 43.35),
    # 피레네 (서 → 동)
    (-0.75, 42.95), (0.00, 42.70), (0.70, 42.72), (1.70, 42.50), (2.20, 42.42),
    (3.03, 42.50),
    # 지중해 연안 (북 → 남)
    (3.20, 41.90), (2.20, 41.40), (1.20, 41.10), (0.90, 40.72), (0.65, 40.55),
    (0.20, 40.10), (0.00, 39.85), (-0.20, 39.50), (-0.33, 39.30), (0.19, 38.73),
    (-0.48, 38.35), (-0.65, 38.15), (-0.98, 37.60), (-1.60, 37.40), (-2.46, 36.83),
    (-3.40, 36.70), (-4.42, 36.72), (-5.30, 36.15), (-5.61, 36.00),
    # 대서양 남부 (동 → 서)
    (-6.29, 36.53), (-6.35, 36.80), (-6.95, 37.26), (-7.40, 37.18),
    # 포르투갈 서해안 (남 → 북)
    (-7.90, 37.02), (-8.80, 37.05), (-8.99, 37.40), (-8.80, 38.00), (-9.20, 38.42),
    (-9.48, 38.78), (-9.35, 39.35), (-9.05, 39.75), (-8.87, 40.15), (-8.75, 40.65),
    (-8.70, 41.15), (-8.87, 41.87),
    # 갈리시아 (남 → 북)
    (-8.80, 42.30), (-9.02, 42.50), (-9.27, 42.90), (-9.30, 43.20), (-8.50, 43.40),
    (-8.40, 43.38), (-8.00, 43.70),
]

# 포르투갈 국경선(참고용 실선)
PT_BORDER = [
    (-7.40, 37.18), (-7.42, 37.60), (-7.30, 38.20), (-7.00, 38.50), (-7.10, 39.10),
    (-7.50, 39.60), (-6.90, 40.20), (-6.80, 41.00), (-6.20, 41.60), (-6.60, 41.90),
    (-7.20, 41.90), (-8.20, 42.10), (-8.87, 41.87),
]

MALLORCA = [(2.35, 39.55), (2.65, 39.35), (3.15, 39.30), (3.45, 39.35), (3.30, 39.75),
            (3.15, 39.92), (2.75, 39.85), (2.40, 39.72)]
MENORCA = [(3.83, 39.92), (4.25, 39.83), (4.32, 40.00), (4.05, 40.06), (3.82, 40.00)]
IBIZA = [(1.22, 38.92), (1.45, 38.65), (1.60, 38.70), (1.55, 39.05), (1.32, 39.08)]

# -------------------------------------------------------------------- 하천망
RIVERS_ES = {
    "Ebro": [(-4.10, 43.00), (-3.80, 42.85), (-3.00, 42.65), (-2.55, 42.55),
             (-1.95, 42.50), (-1.50, 42.40), (-1.00, 42.15), (-0.88, 41.65),
             (-0.20, 41.45), (0.35, 41.25), (0.87, 41.02), (0.65, 40.72)],
    "Duero": [(-2.90, 41.80), (-3.60, 41.62), (-4.30, 41.55), (-5.00, 41.50),
              (-5.40, 41.52), (-6.00, 41.48), (-6.45, 41.38), (-6.90, 41.20),
              (-7.50, 41.10), (-8.00, 41.10), (-8.67, 41.14)],
    "Tajo": [(-1.70, 40.50), (-2.60, 40.40), (-3.30, 40.10), (-3.90, 39.90),
             (-4.80, 39.88), (-5.80, 39.72), (-6.50, 39.62), (-7.50, 39.52),
             (-8.20, 39.20), (-9.05, 38.85)],
    "Guadiana": [(-2.90, 38.95), (-3.80, 38.95), (-5.00, 38.92), (-6.30, 38.88),
                 (-7.00, 38.50), (-7.30, 38.20), (-7.42, 37.60), (-7.40, 37.18)],
    "Guadalquivir": [(-2.90, 37.95), (-3.80, 37.85), (-4.80, 37.62), (-5.50, 37.52),
                     (-5.98, 37.39), (-6.20, 37.05), (-6.35, 36.80)],
    "Mino": [(-7.50, 43.05), (-7.70, 42.70), (-7.85, 42.45), (-8.15, 42.30),
             (-8.50, 42.08), (-8.87, 41.87)],
    "Sil": [(-6.30, 42.55), (-6.80, 42.45), (-7.20, 42.42), (-7.60, 42.42),
            (-7.85, 42.45)],
    "Jucar": [(-1.50, 40.15), (-1.90, 39.55), (-1.20, 39.20), (-0.60, 39.20),
              (-0.25, 39.17)],
    "Segura": [(-2.30, 38.10), (-1.50, 38.10), (-1.10, 38.00), (-0.80, 38.10),
               (-0.65, 38.13)],
}


def cities(m, pts, size=11):
    for lon, lat, name, dx, dy in pts:
        m.square(lon, lat)
        m.label(lon, lat, name, dx=dx, dy=dy, size=size, fill=C_SUB,
                anchor="middle" if dx == 0 else ("start" if dx > 0 else "end"))


def numbered(m, items, footer_h, cols, col_w, rows_per_col, name_dx=15, sub_dx=None):
    """번호 마커 + 하단 범례. items = (n, lon, lat, 한글, 원어, 보조설명, 색)"""
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


def base_es(m, rivers, shapes=None, river_w=2.2, pt_border=True):
    shapes = [IBERIA] if shapes is None else shapes
    m.base(rivers=rivers, shapes=shapes, river_src=RIVERS_ES, river_w=river_w)
    if pt_border:
        m.add('<path d="%s" fill="none" stroke="%s" stroke-width="1.2" '
              'stroke-dasharray="5 4" opacity="0.8"/>' % (m.path(PT_BORDER, close=False),
                                                          C_LAND_ED))


# ======================================================================== 지도 1
def map_spain():
    m = Map((-9.9, 35.7, 4.6, 44.1), 940, pad=14,
            title="스페인 주요 와인 산지",
            subtitle="España : 포도밭 면적 세계 1위(약 92만 ha) · DO 약 70개 + DOCa 2개")
    base_es(m, ["Ebro", "Duero", "Tajo", "Guadiana", "Guadalquivir", "Mino", "Sil"],
            shapes=[IBERIA, MALLORCA, MENORCA, IBIZA], river_w=1.8)

    items = [
        (1, -2.55, 42.52, "리오하", "Rioja", "DOCa · 템프라니요", C_RED),
        (2, -3.85, 41.66, "리베라 델 두에로", "Ribera del Duero", "틴토 피노 · 고지대", C_RED),
        (3, -5.39, 41.52, "토로", "Toro", "틴타 데 토로 · 강건", C_RED),
        (4, -4.95, 41.36, "루에다", "Rueda", "베르데호 화이트", C_WHITE),
        (5, -6.62, 42.56, "비에르소", "Bierzo", "멘시아 · 편암", C_RED),
        (6, -8.72, 42.55, "리아스 바이사스", "Rías Baixas", "알바리뇨", C_WHITE),
        (7, -7.55, 42.40, "리베이라 사크라", "Ribeira Sacra", "협곡 계단밭", C_RED),
        (8, -7.02, 42.44, "발데오라스", "Valdeorras", "고데요", C_WHITE),
        (9, -2.20, 43.28, "차콜리", "Txakoli", "바스크 · 온다라비", C_WHITE),
        (10, -1.75, 42.55, "나바라", "Navarra", "가르나차 로사도", C_RED),
        (11, -1.35, 41.45, "아라곤 4개 DO", "Aragón", "가르나차 노목", C_RED),
        (12, 0.13, 42.08, "소몬타노", "Somontano", "피레네 기슭", C_RED),
        (13, 0.83, 41.18, "프리오라트", "Priorat", "DOQ · 이코렐라 편암", C_RED),
        (14, 1.72, 41.42, "페네데스 · 카바", "Penedès · Cava", "스파클링", C_SPARK),
        (15, 3.02, 42.25, "엠포르다", "Empordà", "트라몬타나 북풍", C_RED),
        (16, -4.25, 40.32, "그레도스 · 마드리드", "Gredos · Madrid", "고지대 가르나차", C_RED),
        (17, -3.20, 39.35, "라 만차", "La Mancha", "세계 최대 단일 산지", C_WHITE),
        (18, -1.10, 39.52, "우티엘레케나", "Utiel-Requena", "보발", C_RED),
        (19, -1.33, 38.48, "후미야", "Jumilla", "모나스트렐", C_RED),
        (20, -6.14, 36.68, "헤레스", "Jerez", "셰리 · 알바리사", C_PURPLE),
        (21, -4.63, 37.58, "몬티야모릴레스", "Montilla-Moriles", "페드로 히메네스", C_PURPLE),
        (22, -4.42, 36.88, "말라가", "Málaga", "모스카텔", C_PURPLE),
        (23, 2.90, 39.65, "마요르카", "Mallorca", "만토 네그로 · 카예트", C_RED),
    ]
    numbered(m, items, footer_h=150, cols=3, col_w=300, rows_per_col=8, sub_dx=278)

    cities(m, [(-3.70, 40.42, "Madrid", 0, -14), (-5.98, 37.39, "Sevilla", -10, 3.5),
               (2.17, 41.39, "Barcelona", 10, 3.5), (-0.88, 41.65, "Zaragoza", 10, -6),
               (-8.55, 42.88, "Santiago", -10, 3.5)])
    m.legend([(C_RED, "레드 중심"), (C_WHITE, "화이트 중심"),
              (C_SPARK, "스파클링"), (C_PURPLE, "주정강화")],
             title="주요 스타일", x=m.w - 182, y=m.h - 250, w=168)
    m.save("spain-overview.svg")


# ======================================================================== 지도 2
def map_rioja():
    m = Map((-3.30, 42.05, -1.55, 42.85), 700, pad=16,
            title="리오하 — 3개 하위 지구",
            subtitle="Rioja DOCa : 알타 / 알라베사 / 오리엔탈. 에브로 강과 시에라 데 칸타브리아 사이")
    base_es(m, ["Ebro"], river_w=4.2, pt_border=False)

    # 재배 벨트
    m.belt([(-2.95, 42.58), (-2.75, 42.55), (-2.55, 42.52), (-2.35, 42.48)],
           C_GREEN, width=15, opacity=0.30)      # 알라베사 (에브로 북안)
    m.belt([(-2.95, 42.42), (-2.70, 42.42), (-2.45, 42.42), (-2.20, 42.40)],
           C_RED, width=16, opacity=0.28)        # 알타 (남안)
    m.belt([(-2.10, 42.32), (-1.90, 42.25), (-1.75, 42.15)],
           C_WHITE, width=15, opacity=0.30)      # 오리엔탈

    zones = [
        (-2.90, 42.60, "리오하 알라베사 Rioja Alavesa", C_GREEN, 10, -8),
        (-2.95, 42.36, "리오하 알타 Rioja Alta", C_RED, 10, 14),
        (-1.92, 42.20, "리오하 오리엔탈 Rioja Oriental", C_WHITE, -10, 14),
    ]
    for lon, lat, name, color, dx, dy in zones:
        m.pin(lon, lat, name, dx=dx, dy=dy, color=color, r=5.4, size=12.5)

    towns = [
        (-2.85, 42.58, "Haro 아로", C_RED, 10, -4),
        (-2.79, 42.60, "Briñas 브리냐스", C_RED, 10, 10),
        (-2.80, 42.49, "Labastida 라바스티다", C_GREEN, -10, 2),
        (-2.58, 42.55, "Laguardia 라과르디아", C_GREEN, 10, 2),
        (-2.62, 42.51, "Elciego 엘시에고", C_GREEN, -10, 12),
        (-2.75, 42.53, "San Vicente 산비센테", C_GREEN, -10, -6),
        (-2.72, 42.42, "Briones 브리오네스", C_RED, -10, 10),
        (-2.50, 42.48, "Cenicero 세니세로", C_RED, 10, 12),
        (-2.42, 42.47, "Fuenmayor 푸엔마요르", C_RED, 10, -4),
        (-2.45, 42.46, "", C_RED, 0, 0),
        (-1.63, 42.18, "Alfaro 알파로", C_WHITE, -10, 2),
    ]
    for lon, lat, name, color, dx, dy in towns:
        if not name:
            continue
        m.pin(lon, lat, name, dx=dx, dy=dy, color=color, r=4.2, size=11)

    cities(m, [(-2.45, 42.47, "Logroño", 0, 16), (-1.61, 42.47, "Calahorra", 10, 3.5)])
    m.legend([(C_GREEN, "알라베사 — 석회질 점토, 우아"),
              (C_RED, "알타 — 서늘·고지대, 장기 숙성"),
              (C_WHITE, "오리엔탈 — 온난·건조, 가르나차")],
             title="하위 지구", x=16, y=m.h - 92, w=280)
    m.save("rioja.svg")


# ======================================================================== 지도 3
def map_duero():
    m = Map((-7.30, 40.85, -2.60, 43.05), 760, pad=16,
            title="카스티야 이 레온 — 두에로 강 산지",
            subtitle="Castilla y León : 해발 700~1,000 m 고원. 리베라 델 두에로 · 토로 · 루에다 · 비에르소")
    base_es(m, ["Duero", "Sil"], river_w=3.6, pt_border=False)

    m.belt([(-4.20, 41.62), (-3.90, 41.66), (-3.60, 41.68), (-3.30, 41.72)],
           C_RED, width=15, opacity=0.30)        # 리베라
    m.belt([(-5.55, 41.50), (-5.30, 41.52)], C_RED, width=14, opacity=0.30)   # 토로
    m.belt([(-5.10, 41.42), (-4.85, 41.35), (-4.65, 41.30)], C_WHITE, width=14, opacity=0.30)
    m.belt([(-6.80, 42.58), (-6.60, 42.55), (-6.45, 42.50)], C_PURPLE, width=14, opacity=0.30)

    items = [
        (1, -3.85, 41.66, "리베라 델 두에로", "Ribera del Duero", "틴토 피노", C_RED),
        (2, -5.39, 41.52, "토로", "Toro", "틴타 데 토로", C_RED),
        (3, -4.90, 41.36, "루에다", "Rueda", "베르데호", C_WHITE),
        (4, -4.68, 41.75, "시갈레스", "Cigales", "로사도 전통", C_RED),
        (5, -6.62, 42.56, "비에르소", "Bierzo", "멘시아", C_PURPLE),
        (6, -3.95, 42.10, "아를란사", "Arlanza", "고지대 서늘", C_RED),
        (7, -6.50, 41.25, "아리베스", "Arribes", "후안 가르시아", C_RED),
        (8, -5.55, 42.55, "티에라 데 레온", "Tierra de León", "프리에토 피쿠도", C_RED),
        (9, -5.20, 41.95, "티에라 델 비노", "Tierra del Vino", "소규모", C_RED),
    ]
    numbered(m, items, footer_h=110, cols=3, col_w=245, rows_per_col=3, sub_dx=228)

    cities(m, [(-4.72, 41.65, "Valladolid", -11, 3.5), (-3.70, 42.34, "Burgos", 10, 3.5),
               (-5.66, 40.97, "Salamanca", 0, 14), (-5.57, 42.60, "León", -11, 3.5),
               (-2.47, 41.76, "Soria", 10, 3.5)])
    m.save("duero.svg")


# ======================================================================== 지도 4
def map_catalunya():
    m = Map((0.05, 40.55, 3.40, 42.60), 700, pad=16,
            title="카탈루냐 — 프리오라트 · 페네데스 · 카바",
            subtitle="Catalunya : 지중해 연안 12개 DO + DOQ 프리오라트, 카바의 본거지")
    base_es(m, ["Ebro"], river_w=3.2, pt_border=False)

    m.belt([(0.72, 41.25), (0.83, 41.18), (0.92, 41.14)], C_RED, width=16, opacity=0.34)
    m.belt([(1.45, 41.48), (1.70, 41.42), (1.95, 41.35)], C_SPARK, width=15, opacity=0.30)

    items = [
        (1, 0.83, 41.18, "프리오라트", "Priorat", "DOQ · 이코렐라", C_RED),
        (2, 0.68, 41.28, "몬산트", "Montsant", "프리오라트를 감쌈", C_RED),
        (3, 0.42, 41.00, "테라 알타", "Terra Alta", "가르나차 블랑카", C_WHITE),
        (4, 1.72, 41.42, "페네데스", "Penedès", "사렐로 · 카바", C_SPARK),
        (5, 1.15, 41.42, "콩카 데 바르베라", "Conca de Barberà", "트레파트", C_RED),
        (6, 0.88, 41.62, "코스테르스 델 세그레", "Costers del Segre", "내륙 고지", C_RED),
        (7, 1.02, 41.15, "타라고나", "Tarragona", "광역", C_WHITE),
        (8, 2.30, 41.52, "알레야", "Alella", "바르셀로나 근교", C_WHITE),
        (9, 1.83, 41.78, "플라 데 바제스", "Pla de Bages", "소규모", C_RED),
        (10, 3.02, 42.25, "엠포르다", "Empordà", "트라몬타나", C_RED),
        (11, 1.55, 41.30, "카바 (중심지)", "Cava", "산 사두르니", C_SPARK),
    ]
    numbered(m, items, footer_h=110, cols=3, col_w=225, rows_per_col=4, sub_dx=210)

    cities(m, [(2.17, 41.39, "Barcelona", 10, 3.5), (1.25, 41.12, "Tarragona", -11, 3.5),
               (0.63, 41.62, "Lleida", -11, 3.5), (2.82, 41.98, "Girona", 10, 3.5)])
    m.save("catalunya.svg")


# ======================================================================== 지도 5
def map_galicia():
    m = Map((-9.40, 41.75, -6.10, 43.60), 700, pad=16,
            title="갈리시아 — 대서양 스페인",
            subtitle="Galicia : 강우량이 많은 녹색 스페인. 알바리뇨 · 고데요 · 멘시아")
    base_es(m, ["Mino", "Sil"], river_w=4.0, pt_border=False)

    m.belt([(-8.85, 42.60), (-8.75, 42.45), (-8.70, 42.30)], C_WHITE, width=15, opacity=0.32)
    m.belt([(-7.75, 42.42), (-7.50, 42.40), (-7.30, 42.42)], C_RED, width=15, opacity=0.30)

    items = [
        (1, -8.78, 42.58, "리아스 바이사스", "Rías Baixas", "알바리뇨 · 5개 하위지구", C_WHITE),
        (2, -8.15, 42.29, "리베이로", "Ribeiro", "트레이사두라", C_WHITE),
        (3, -7.55, 42.40, "리베이라 사크라", "Ribeira Sacra", "협곡 계단밭 · 멘시아", C_RED),
        (4, -7.02, 42.44, "발데오라스", "Valdeorras", "고데요 부활", C_WHITE),
        (5, -7.45, 41.98, "몬테레이", "Monterrei", "가장 따뜻·건조", C_RED),
        (6, -6.62, 42.56, "비에르소", "Bierzo", "행정상 카스티야", C_RED),
    ]
    numbered(m, items, footer_h=90, cols=2, col_w=330, rows_per_col=3, sub_dx=312)

    cities(m, [(-8.55, 42.88, "Santiago", 10, 3.5), (-8.72, 42.24, "Pontevedra", -11, 3.5),
               (-7.55, 43.01, "Lugo", 10, 3.5), (-8.41, 43.37, "A Coruña", 10, 3.5),
               (-7.86, 42.34, "Ourense", -11, 12)])
    m.save("galicia.svg")


# ======================================================================== 지도 6
def map_jerez():
    m = Map((-6.60, 36.35, -5.55, 36.95), 660, pad=16,
            title="헤레스 — 셰리 삼각지대와 알바리사 파고",
            subtitle="Marco de Jerez : 헤레스 · 산루카르 · 엘 푸에르토 3개 도시가 이루는 삼각형")
    m.base(rivers=[], shapes=[IBERIA], river_src=RIVERS_ES)

    # 알바리사 구역
    m.belt([(-6.30, 36.72), (-6.15, 36.72), (-6.02, 36.70)], C_WHITE, width=22, opacity=0.30)
    m.belt([(-6.32, 36.80), (-6.20, 36.78)], C_WHITE, width=18, opacity=0.30)

    pagos = [
        (-6.18, 36.76, "Macharnudo 마차르누도", C_PURPLE, 10, -4),
        (-6.08, 36.72, "Carrascal 카라스칼", C_PURPLE, 10, 6),
        (-6.25, 36.68, "Balbaína 발바이나", C_PURPLE, -10, 6),
        (-6.22, 36.80, "Añina 아니냐", C_PURPLE, -10, -4),
        (-6.32, 36.77, "Miraflores 미라플로레스", C_PURPLE, -10, 10),
    ]
    for lon, lat, name, color, dx, dy in pagos:
        m.pin(lon, lat, name, dx=dx, dy=dy, color=color, r=4.6, size=11)

    towns = [
        (-6.14, 36.68, "Jerez de la Frontera 헤레스", C_RED, 10, 14),
        (-6.35, 36.78, "Sanlúcar de Barrameda 산루카르", C_SPARK, 10, 16),
        (-6.23, 36.59, "El Puerto de Santa María 엘 푸에르토", C_GREEN, 10, 6),
    ]
    for lon, lat, name, color, dx, dy in towns:
        m.pin(lon, lat, name, dx=dx, dy=dy, color=color, r=6.0, size=12.5)

    # 삼각형
    tri = [m.xy(-6.14, 36.68), m.xy(-6.35, 36.78), m.xy(-6.23, 36.59)]
    m.add('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" fill="none" stroke="%s" '
          'stroke-width="1.6" stroke-dasharray="6 4" opacity="0.75"/>'
          % (tri[0][0], tri[0][1], tri[1][0], tri[1][1], tri[2][0], tri[2][1], C_SUB))

    m.legend([(C_SPARK, "산루카르 — 만사니야(가장 서늘·습윤)"),
              (C_RED, "헤레스 — 피노·아몬티야도의 중심"),
              (C_GREEN, "엘 푸에르토 — 해풍, 부드러운 피노"),
              (C_PURPLE, "주요 파고(pago) — 알바리사 백악토")],
             title="셰리 삼각지대", x=16, y=m.h - 110, w=300)
    m.save("jerez.svg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    map_spain()
    map_rioja()
    map_duero()
    map_catalunya()
    map_galicia()
    map_jerez()
