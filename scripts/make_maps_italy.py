#!/usr/bin/env python3
"""이탈리아 와인 산지 지도(SVG) 생성기.

make_maps.py 의 Map 클래스(경위도 → 픽셀 투영)를 재사용한다.
실행: python3 scripts/make_maps_italy.py
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
ITALY = [
    # 티레니아해 연안 (북서 → 남)
    (7.60, 43.79), (8.93, 44.41), (9.83, 44.10), (10.31, 43.55), (10.52, 42.93),
    (11.13, 42.40), (11.80, 42.09), (12.28, 41.73), (12.63, 41.44), (13.57, 41.21),
    (14.05, 40.96), (14.25, 40.85), (14.77, 40.68), (14.99, 40.35), (15.63, 40.07),
    (16.05, 39.36), (15.90, 38.68), (15.65, 38.11),
    # 칼라브리아 발끝 → 이오니아해 연안 북상
    (15.95, 37.93), (16.26, 38.24), (16.58, 38.45), (17.14, 39.08), (17.13, 39.37),
    (16.60, 39.83), (16.80, 40.38), (17.24, 40.47),
    # 살렌토 반도 (이오니아 쪽 남하 → 레우카 → 아드리아 쪽 북상)
    (17.60, 40.30), (17.98, 40.06), (18.35, 39.79), (18.50, 40.15), (18.05, 40.50),
    (17.95, 40.63), (17.28, 40.83), (16.87, 41.13),
    # 아드리아해 연안 (가르가노 곶 포함) 북상
    (16.30, 41.35), (15.92, 41.62), (16.18, 41.88), (15.88, 41.93), (15.35, 41.86),
    (14.99, 42.00), (14.22, 42.46), (13.52, 43.62), (12.57, 44.06), (12.34, 45.44),
    (13.10, 45.55), (13.77, 45.65),
    # 알프스 국경 (동 → 서)
    (13.70, 46.52), (12.38, 46.68), (12.15, 47.09), (11.10, 46.99), (10.45, 46.87),
    (10.10, 46.62), (9.25, 46.50), (8.62, 46.12), (8.10, 46.10), (7.85, 45.92),
    (6.98, 45.86), (6.63, 45.11), (7.02, 44.85), (7.35, 44.12),
]

SICILY = [
    (15.55, 38.20), (15.24, 38.28), (14.50, 38.10), (13.36, 38.12), (12.85, 38.10),
    (12.51, 38.02), (12.44, 37.80), (12.59, 37.65), (13.08, 37.51), (13.58, 37.28),
    (14.25, 37.06), (14.85, 36.73), (15.10, 36.69), (15.29, 37.07), (15.28, 37.35),
    (15.09, 37.50), (15.24, 37.80),
]

SARDINIA = [
    (9.19, 41.24), (9.50, 40.92), (9.70, 40.38), (9.70, 39.94), (9.63, 39.50),
    (9.52, 39.10), (9.11, 39.21), (8.85, 38.87), (8.45, 39.10), (8.38, 39.55),
    (8.50, 39.90), (8.31, 40.56), (8.16, 40.57), (8.23, 40.94), (8.71, 40.92),
]

PANTELLERIA = [(11.93, 36.82), (12.03, 36.83), (12.06, 36.76), (11.96, 36.74)]

ELBA = [(10.10, 42.79), (10.20, 42.82), (10.32, 42.80), (10.42, 42.81),
        (10.40, 42.74), (10.25, 42.73), (10.13, 42.75)]

# -------------------------------------------------------------------- 하천망
RIVERS_IT = {
    "Po": [(7.55, 44.70), (7.68, 45.07), (8.45, 45.10), (9.15, 45.05), (10.30, 44.98),
           (11.00, 44.95), (11.80, 44.98), (12.35, 44.95)],
    "Tanaro": [(7.90, 44.15), (8.03, 44.70), (8.21, 44.90), (8.61, 44.91), (8.85, 45.02)],
    "Adige": [(11.35, 46.50), (11.12, 46.07), (11.00, 45.44), (11.62, 45.20), (12.33, 45.20)],
    "Arno": [(11.88, 43.77), (11.25, 43.77), (10.90, 43.72), (10.40, 43.72), (10.28, 43.68)],
    "Tevere": [(12.10, 43.40), (12.24, 42.83), (12.47, 42.42), (12.48, 41.90), (12.23, 41.75)],
    "Ticino": [(8.62, 46.12), (8.72, 45.55), (9.00, 45.15), (9.15, 45.05)],
    "Adda": [(10.10, 46.30), (9.65, 46.15), (9.40, 45.85), (9.55, 45.30), (9.85, 45.15),
             (9.95, 45.05)],
    "Piave": [(12.35, 46.55), (12.20, 46.10), (12.25, 45.85), (12.50, 45.60), (12.65, 45.55)],
    "Ombrone": [(11.55, 43.10), (11.30, 42.85), (11.05, 42.66)],
}


def cities(m, pts, size=11):
    for lon, lat, name, dx, dy in pts:
        m.square(lon, lat)
        m.label(lon, lat, name, dx=dx, dy=dy, size=size, fill=C_SUB,
                anchor="middle" if dx == 0 else ("start" if dx > 0 else "end"))


# ======================================================================== 지도 1
def map_italy():
    m = Map((6.20, 36.40, 19.00, 47.30), 720, pad=14,
            title="이탈리아 주요 와인 산지",
            subtitle="I vigneti d'Italia — 20개 주 전역에서 와인을 생산하는 유일한 나라")
    m.base(rivers=list(RIVERS_IT.keys()), shapes=[ITALY, SICILY, SARDINIA, ELBA],
           river_src=RIVERS_IT, river_w=2.0)

    # (경도, 위도, 라벨, 색, dx, dy)
    regions = [
        (7.95, 44.62, "피에몬테 Piemonte", C_RED, 10, 0),
        (7.40, 45.70, "발레다오스타 V. d'Aosta", C_WHITE, 10, -10),
        (9.85, 46.17, "발텔리나 Valtellina", C_RED, 10, -4),
        (10.05, 45.62, "프란차코르타 Franciacorta", C_SPARK, -10, 12),
        (11.35, 46.45, "알토아디제 Alto Adige", C_WHITE, 10, -4),
        (11.12, 46.07, "트렌티노 Trentino", C_SPARK, 10, 10),
        (12.05, 45.90, "프로세코 Prosecco", C_SPARK, 10, 18),
        (13.40, 46.05, "프리울리 Friuli", C_WHITE, 10, 4),
        (11.60, 45.25, "베네토 Veneto", C_RED, -10, 4),
        (11.35, 44.55, "에밀리아로마냐 Emilia-Romagna", C_RED, 10, 6),
        (9.30, 44.20, "리구리아 Liguria", C_WHITE, -10, 6),
        (11.30, 43.45, "키안티 클라시코", C_RED, 10, -6),
        (11.49, 43.06, "몬탈치노 Montalcino", C_RED, 10, 6),
        (10.60, 43.23, "볼게리 Bolgheri", C_RED, -10, 4),
        (12.65, 42.90, "움브리아 Umbria", C_RED, 10, 18),
        (13.30, 43.45, "마르케 Marche", C_WHITE, 10, 6),
        (13.90, 42.35, "아브루초 Abruzzo", C_RED, 10, 2),
        (12.60, 41.80, "라치오 Lazio", C_WHITE, -10, 6),
        (14.90, 40.95, "캄파니아 Campania", C_RED, -10, 0),
        (15.55, 40.95, "바실리카타 Basilicata", C_RED, 10, -6),
        (17.30, 40.60, "풀리아 Puglia", C_RED, -10, 4),
        (16.60, 39.20, "칼라브리아 Calabria", C_RED, 10, 4),
        (15.00, 37.75, "에트나 Etna", C_RED, 10, -4),
        (14.53, 36.99, "체라수올로 디 비토리아", C_RED, 10, 8),
        (12.45, 37.80, "마르살라 Marsala", C_WHITE, -10, 4),
        (9.15, 41.05, "사르데냐 Sardegna", C_RED, -10, 4),
    ]
    for lon, lat, name, color, dx, dy in regions:
        m.pin(lon, lat, name, dx=dx, dy=dy, color=color, r=5.0, size=12)

    cities(m, [(12.48, 41.90, "Roma", 9, 3.5), (9.19, 45.46, "Milano", -9, 3.5),
               (7.68, 45.07, "Torino", -9, 3.5), (12.34, 45.44, "Venezia", 9, 12),
               (11.25, 43.77, "Firenze", -9, 3.5), (14.25, 40.85, "Napoli", -9, 3.5),
               (13.36, 38.12, "Palermo", 0, -10)])

    m.legend([(C_RED, "레드 중심"), (C_WHITE, "화이트 중심"), (C_SPARK, "스파클링")],
             title="주요 스타일", x=16, y=m.h - 100, w=168)
    m.save("italy-overview.svg")


# ======================================================================== 지도 2
def map_langhe():
    tanaro_local = {"Tanaro": [(7.78, 44.62), (7.84, 44.635), (7.90, 44.662),
                               (7.98, 44.690), (8.03, 44.706), (8.09, 44.750),
                               (8.14, 44.800), (8.21, 44.900)]}
    m = Map((7.78, 44.53, 8.24, 44.80), 760, pad=18,
            title="랑게 — 바롤로 / 바르바레스코 코무네",
            subtitle="Le Langhe : 타나로 강을 사이에 두고 바롤로(남서) · 바르바레스코(북동)")
    m.base(rivers=["Tanaro"], shapes=[ITALY], river_src=tanaro_local, river_w=7.0)

    # 두 DOCG 구역 음영
    m.poly([(7.845, 44.700), (7.995, 44.700), (8.035, 44.640), (8.030, 44.565),
            (7.925, 44.560), (7.855, 44.610)], "#9b3946", opacity=0.16)
    m.poly([(8.048, 44.748), (8.078, 44.758), (8.138, 44.746), (8.148, 44.700),
            (8.118, 44.660), (8.052, 44.662), (8.036, 44.702)], "#4a6b8a", opacity=0.16)

    x, y = m.xy(7.870, 44.575)
    m.text_px(x, y, "BAROLO DOCG", size=13, fill="#8c2f39", weight="700", anchor="middle")
    x, y = m.xy(8.115, 44.768)
    m.text_px(x, y, "BARBARESCO DOCG", size=13, fill="#3f5f7c", weight="700", anchor="middle")

    barolo = [
        (7.9430, 44.6120, "바롤로 Barolo", -10, 4),
        (7.9230, 44.6370, "라 모라 La Morra", -10, 4),
        (7.9770, 44.6220, "카스틸리오네 팔레토 Castiglione Falletto", 10, -4),
        (8.0070, 44.6170, "세랄룽가 달바 Serralunga d'Alba", 10, 8),
        (7.9680, 44.5830, "몬포르테 달바 Monforte d'Alba", 10, 4),
        (7.9180, 44.5830, "노벨로 Novello", -10, 4),
        (7.9250, 44.6730, "베르두노 Verduno", -10, 4),
        (7.9920, 44.6530, "그린차네 카부르 Grinzane Cavour", -10, -2),
        (8.0170, 44.6580, "디아노 달바 Diano d'Alba", 10, 4),
        (7.8580, 44.6470, "케라스코 Cherasco", -10, 4),
        (7.9550, 44.6850, "로디 Roddi", -10, 4),
    ]
    barbaresco = [
        (8.0830, 44.7230, "바르바레스코 Barbaresco", 10, 4),
        (8.1170, 44.7280, "네이베 Neive", 10, -6),
        (8.0670, 44.6770, "트레이소 Treiso", 10, 4),
    ]
    for lon, lat, name, dx, dy in barolo:
        m.pin(lon, lat, name, dx=dx, dy=dy, color=C_RED, r=5.0, size=11.5)
    for lon, lat, name, dx, dy in barbaresco:
        m.pin(lon, lat, name, dx=dx, dy=dy, color="#4a6b8a", r=5.0, size=11.5)

    m.pin(7.9930, 44.8000, "카날레 Canale (로에로)", dx=10, dy=4, color=C_WHITE, r=4.5, size=11)

    m.square(8.0350, 44.7000, s=8, fill=C_TEXT)
    m.label(8.0350, 44.7000, "알바 Alba", dx=-10, dy=4, size=12.5, weight="700")

    x, y = m.xy(7.9600, 44.7550)
    m.text_px(x, y, "타나로 강 Tanaro", size=11, fill="#3f6a8a", weight="600", anchor="middle")

    m.legend([(C_RED, "바롤로 코무네 (11)"), ("#4a6b8a", "바르바레스코 코무네 (4)"),
              (C_WHITE, "로에로")], x=16, y=m.h - 90, w=210)
    m.save("langhe.svg")


# ======================================================================== 지도 3
def map_barolo_mga():
    """바롤로·바르바레스코 코무네별 대표 MGA(크뤼) 배열표."""
    W, TOP, ROW = 1100, 96, 31.0
    rows = [
        ("라 모라 La Morra", "B", "Brunate · Cerequio · Rocche dell'Annunziata · La Serra · Arborina · Gattera",
         "가장 향기롭고 우아 — 여성적"),
        ("바롤로 Barolo", "B", "Cannubi · Brunate · Cerequio · Sarmassa · Bricco delle Viole · Ravera",
         "균형형, 칸누비가 상징"),
        ("베르두노 Verduno", "B", "Monvigliero · Massara · Breri", "섬세·꽃향, 재평가 급상승"),
        ("케라스코 Cherasco", "B", "Mantoetto", "최소 면적"),
        ("로디 Roddi", "B", "Bricco Ambrogio", "북서쪽 가장자리"),
        ("그린차네 카부르 Grinzane Cavour", "B", "Gustava · Borzone · Canova", "중간 성격"),
        ("노벨로 Novello", "B", "Ravera (바롤로와 공유) · Bergera-Pezzole", "고도 높고 서늘"),
        ("카스틸리오네 팔레토 Castiglione F.", "B",
         "Villero · Rocche di Castiglione · Monprivato · Bricco Boschis · Fiasco · Codana",
         "두 스타일의 접점, 완성도 최고"),
        ("몬포르테 달바 Monforte d'Alba", "B",
         "Bussia · Ginestra · Mosconi · Gramolere · Bricco San Pietro · Perno",
         "구조적·묵직, 장기 숙성"),
        ("세랄룽가 달바 Serralunga d'Alba", "B",
         "Vigna Rionda · Francia · Lazzarito · Falletto · Ornato · Cerretta · Prapò",
         "가장 강건·탄닌 강함 — 남성적"),
        ("디아노 달바 Diano d'Alba", "B", "Sorano (세랄룽가와 공유) · La Vigna", "소규모"),
        ("바르바레스코 Barbaresco", "N",
         "Asili · Rabajà · Martinenga · Montestefano · Ovello · Pora · Montefico · Rio Sordo",
         "가장 우아, 아실리·라바야가 정점"),
        ("네이베 Neive", "N", "Santo Stefano · Albesani · Gallina · Serraboella · Basarin · Currà",
         "향신료·구조감"),
        ("트레이소 Treiso", "N", "Pajorè · Bernadot · Nervo · Rombone · Marcarini",
         "고도 최고, 신선·긴장감"),
        ("산 로코 세노 델비오", "N", "Rocche Massalupo · San Stunet", "알바 시 소속 프라치오네"),
    ]
    H = TOP + len(rows) * ROW + 46
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
         'role="img"><rect width="100%%" height="100%%" fill="%s"/>' % (W, H, W, H, C_BG)]
    o.append('<text x="20" y="28" font-size="18" font-weight="700" fill="%s" font-family="%s">'
             '바롤로 · 바르바레스코 — 코무네별 대표 크뤼(MGA)</text>' % (C_TEXT, FONT))
    o.append('<text x="20" y="48" font-size="12.5" fill="%s" font-family="%s">'
             'MGA = Menzione Geografica Aggiuntiva (추가 지리 표기) · '
             '바롤로 181개 · 바르바레스코 66개 중 대표만 발췌</text>' % (C_SUB, FONT))
    o.append('<text x="20" y="72" font-size="11.5" fill="%s" font-family="%s">'
             '서쪽(라 모라·바롤로)은 청회색 이회토 → 향기·조기 접근 / '
             '동쪽(세랄룽가·몬포르테)은 사질 압축토 → 탄닌·장기 숙성</text>' % (C_SUB, FONT))

    xl, col_w = 20, 250
    for i, (name, sec, crus, note) in enumerate(rows):
        y = TOP + i * ROW
        cy = y + ROW / 2
        o.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="%s"/>'
                 % (xl, y, W - 40, ROW, "#f4efe6" if i % 2 == 0 else "#ffffff"))
        acc = C_RED if sec == "B" else "#4a6b8a"
        o.append('<rect x="%d" y="%.1f" width="5" height="%.1f" fill="%s"/>' % (xl, y, ROW, acc))
        o.append('<text x="%d" y="%.1f" font-size="12.5" font-weight="700" fill="%s" '
                 'font-family="%s">%s</text>' % (xl + 15, cy + 4, C_TEXT, FONT, esc(name)))
        o.append('<text x="%d" y="%.1f" font-size="11.5" fill="%s" font-family="%s">%s</text>'
                 % (xl + col_w, cy + 4, C_SUB, FONT, esc(crus)))
        o.append('<text x="%d" y="%.1f" font-size="11" fill="%s" text-anchor="end" '
                 'font-family="%s">%s</text>' % (W - 32, cy + 4, "#8a7f72", FONT, esc(note)))

    yl = TOP + len(rows) * ROW + 26
    o.append('<circle cx="30" cy="%.1f" r="5" fill="%s"/>' % (yl - 4, C_RED))
    o.append('<text x="42" y="%.1f" font-size="11.5" fill="%s" font-family="%s">'
             'Barolo DOCG (11개 코무네)</text>' % (yl, C_TEXT, FONT))
    o.append('<circle cx="240" cy="%.1f" r="5" fill="#4a6b8a"/>' % (yl - 4))
    o.append('<text x="252" y="%.1f" font-size="11.5" fill="%s" font-family="%s">'
             'Barbaresco DOCG (4개 코무네)</text>' % (yl, C_TEXT, FONT))
    o.append("</svg>")
    p = os.path.join(OUT, "barolo-mga.svg")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    print("wrote", p)


# ======================================================================== 지도 4
def map_toscana():
    m = Map((9.90, 42.35, 12.30, 44.15), 760, pad=16,
            title="토스카나 — 주요 DOCG / DOC",
            subtitle="Chianti Classico · Brunello di Montalcino · Vino Nobile · Bolgheri")
    m.base(rivers=["Arno", "Ombrone", "Tevere"], shapes=[ITALY, ELBA],
           river_src=RIVERS_IT, river_w=3.0)

    # 키안티 클라시코 벨트
    m.belt([(11.32, 43.68), (11.31, 43.55), (11.36, 43.44), (11.42, 43.35)],
           C_RED, width=22, opacity=0.30)

    pts = [
        (11.315, 43.585, "키안티 클라시코 Chianti Classico", C_RED, 14, -6,
         "산조베제 · 11개 UGA"),
        (11.490, 43.055, "브루넬로 디 몬탈치노", C_RED, 14, 16, "산조베제 그로소 100%"),
        (11.780, 43.100, "비노 노빌레 디 몬테풀차노", C_RED, 14, -8, "프루뇰로 젠틸레"),
        (10.600, 43.230, "볼게리 Bolgheri", C_RED, -14, 2, "사시카이아 · 오르넬라이아"),
        (11.040, 43.470, "베르나차 디 산지미냐노", C_WHITE, -14, 2, "토스카나 유일 화이트 DOCG"),
        (11.000, 43.810, "카르미냐노 Carmignano", C_RED, -14, 2, "산조베제 + 카베르네"),
        (11.340, 42.690, "모렐리노 디 스칸사노", C_RED, 14, 2, "마렘마"),
        (11.560, 42.900, "몬테쿠코 Montecucco", C_RED, 14, 2, None),
        (10.860, 43.030, "수베레토 Suvereto", C_RED, -14, 2, "발 디 코르니아"),
        (11.900, 43.470, "키안티 루피나 Chianti Rùfina", C_RED, -14, 2, "서늘·장기 숙성"),
    ]
    for lon, lat, name, color, dx, dy, sub in pts:
        m.pin(lon, lat, name, dx=dx, dy=dy, sub=sub, color=color, r=5.2, size=12)

    cities(m, [(11.25, 43.77, "Firenze", -10, 3.5), (11.33, 43.32, "Siena", -10, 3.5),
               (10.40, 43.72, "Pisa", -10, 3.5), (11.11, 42.77, "Grosseto", -10, 3.5)])

    m.legend([(C_RED, "레드 (산조베제·보르도 품종)"), (C_WHITE, "화이트")],
             x=16, y=m.h - 72, w=230)
    m.save("toscana.svg")


# ======================================================================== 지도 5
def map_nordest():
    m = Map((9.60, 44.90, 14.10, 47.10), 820, pad=16,
            title="북동부 — 베네토 · 트렌티노알토아디제 · 프리울리",
            subtitle="Amarone · Soave · Prosecco · Alto Adige · Collio")
    m.base(rivers=["Adige", "Piave", "Po", "Adda"], shapes=[ITALY],
           river_src=RIVERS_IT, river_w=3.0)

    # 산지가 촘촘해 라벨이 겹치므로 번호 마커 + 하단 3열 범례로 표기
    items = [
        (1, 10.95, 45.53, "발폴리첼라", "Valpolicella", "아마로네 · 리파소", C_RED),
        (2, 11.25, 45.42, "소아베", "Soave", "가르가네가", C_WHITE),
        (3, 10.68, 45.50, "바르돌리노", "Bardolino", "코르비나", C_RED),
        (4, 10.50, 45.47, "루가나", "Lugana", "투르비아나", C_WHITE),
        (5, 12.10, 45.92, "코넬리아노 발도비아데네", "Prosecco Superiore", "글레라 · DOCG", C_SPARK),
        (6, 11.90, 45.78, "아솔로", "Asolo Prosecco", "글레라 · DOCG", C_SPARK),
        (7, 11.12, 46.07, "트렌토", "Trento DOC", "메토도 클라시코", C_SPARK),
        (8, 11.15, 46.22, "테롤데고 로탈리아노", "Teroldego Rotaliano", "테롤데고", C_RED),
        (9, 11.32, 46.52, "알토아디제", "Alto Adige", "테를라노 · 발레 이자르코", C_WHITE),
        (10, 11.24, 46.34, "테르메노", "Termeno / Tramin", "게뷔르츠트라미너 원산지", C_WHITE),
        (11, 13.52, 45.96, "콜리오", "Collio", "리볼라 지알라 · 프리울라노", C_WHITE),
        (12, 13.32, 46.14, "콜리 오리엔탈리", "Colli Orientali", "피콜리트 · 스키오페티노", C_WHITE),
        (13, 13.78, 45.74, "카르소", "Carso", "비토프스카 · 테라노", C_WHITE),
        (14, 10.02, 45.62, "프란차코르타", "Franciacorta", "메토도 클라시코 DOCG", C_SPARK),
        (15, 9.85, 46.17, "발텔리나", "Valtellina", "네비올로(키아벤나스카)", C_RED),
    ]
    m.footer_h = 188
    m.h += m.footer_h
    for n, lon, lat, ko, it, sub, color in items:
        x, y = m.xy(lon, lat)
        m.add('<circle cx="%.1f" cy="%.1f" r="10.5" fill="%s" stroke="%s" stroke-width="1.6"/>'
              % (x, y, color, C_BG))
        m.text_px(x, y + 4, str(n), size=12, fill="#ffffff", anchor="middle", weight="700",
                  halo=False)

    cities(m, [(11.00, 45.44, "Verona", 0, 18), (12.34, 45.44, "Venezia", 0, 18),
               (11.35, 46.50, "Bolzano", -14, 4), (13.24, 46.07, "Udine", -14, 4),
               (9.19, 45.46, "Milano", 0, 18), (11.88, 45.41, "Padova", 0, 18)])

    fy = m.h - m.footer_h + 6
    m.add('<rect x="14" y="%.1f" width="%.1f" height="%.1f" fill="#ffffff" '
          'fill-opacity="0.92" stroke="%s" rx="4"/>' % (fy, m.w - 28, m.footer_h - 20, C_LAND_ED))
    for i, (n, lon, lat, ko, it, sub, color) in enumerate(items):
        col, row = divmod(i, 8)
        bx = 32 + col * 390
        by = fy + 24 + row * 19.5
        m.add('<circle cx="%.1f" cy="%.1f" r="8" fill="%s"/>' % (bx, by - 4, color))
        m.text_px(bx, by, str(n), size=10.5, fill="#fff", anchor="middle", weight="700", halo=False)
        m.text_px(bx + 15, by, "%s %s" % (ko, it), size=11.5, weight="600", halo=False)
        m.text_px(bx + 370, by, sub, size=10.5, fill=C_SUB, anchor="end", halo=False)
    m.save("nordest.svg")


# ======================================================================== 지도 6
def map_sud_isole():
    m = Map((7.90, 36.40, 19.00, 41.90), 860, pad=16,
            title="남부 및 도서 — 캄파니아 · 풀리아 · 시칠리아 · 사르데냐",
            subtitle="Taurasi · Aglianico del Vulture · Primitivo · Etna · Cannonau")
    m.base(rivers=[], shapes=[ITALY, SICILY, SARDINIA, PANTELLERIA], river_src=RIVERS_IT)

    # 남부는 산지가 겹쳐 있어 번호 마커 + 하단 2열 범례로 표기
    items = [
        (1, 15.15, 41.12, "타우라시", "Taurasi", "알리아니코 · 캄파니아 최고", C_RED),
        (2, 14.70, 40.86, "피아노 디 아벨리노", "Fiano di Avellino", "피아노", C_WHITE),
        (3, 14.92, 40.99, "그레코 디 투포", "Greco di Tufo", "그레코", C_WHITE),
        (4, 14.55, 41.22, "산니오", "Sannio Falanghina", "팔랑기나", C_WHITE),
        (5, 14.60, 40.62, "코스타 다말피", "Costa d'Amalfi", "절벽 계단밭", C_WHITE),
        (6, 15.62, 40.95, "알리아니코 델 불투레", "Aglianico del Vulture", "바실리카타 · 화산토", C_RED),
        (7, 16.27, 41.05, "카스텔 델 몬테", "Castel del Monte", "네로 디 트로이아", C_RED),
        (8, 16.92, 40.80, "조이아 델 콜레", "Gioia del Colle", "프리미티보", C_RED),
        (9, 17.63, 40.40, "프리미티보 디 만두리아", "Primitivo di Manduria", "프리미티보", C_RED),
        (10, 17.98, 40.33, "살리체 살렌티노", "Salice Salentino", "네그로아마로", C_RED),
        (11, 17.12, 39.38, "치로", "Cirò", "칼라브리아 · 갈리오포", C_RED),
        (12, 15.00, 37.75, "에트나", "Etna", "네렐로 마스칼레제 · 콘트라다", C_RED),
        (13, 14.53, 36.99, "체라수올로 디 비토리아", "Cerasuolo di Vittoria", "시칠리아 유일 DOCG", C_RED),
        (14, 12.44, 37.80, "마르살라", "Marsala", "주정강화", C_WHITE),
        (15, 11.99, 36.79, "판텔레리아", "Pantelleria", "지비보 파시토", C_WHITE),
        (16, 9.35, 41.02, "베르멘티노 디 갈루라", "Vermentino di Gallura", "사르데냐 유일 DOCG", C_WHITE),
        (17, 9.20, 40.30, "칸노나우 디 사르데냐", "Cannonau di Sardegna", "= 그르나슈", C_RED),
        (18, 8.55, 39.15, "카리냐노 델 술치스", "Carignano del Sulcis", "= 카리냥", C_RED),
    ]
    m.footer_h = 212
    m.h += m.footer_h
    for n, lon, lat, ko, it, sub, color in items:
        x, y = m.xy(lon, lat)
        m.add('<circle cx="%.1f" cy="%.1f" r="10.5" fill="%s" stroke="%s" stroke-width="1.6"/>'
              % (x, y, color, C_BG))
        m.text_px(x, y + 4, str(n), size=12, fill="#ffffff", anchor="middle", weight="700",
                  halo=False)

    cities(m, [(14.25, 40.85, "Napoli", -13, 4), (16.87, 41.13, "Bari", 0, -13),
               (15.09, 37.50, "Catania", -13, 4), (13.36, 38.12, "Palermo", 0, -13),
               (9.11, 39.21, "Cagliari", 0, 17)])

    fy = m.h - m.footer_h + 6
    m.add('<rect x="14" y="%.1f" width="%.1f" height="%.1f" fill="#ffffff" '
          'fill-opacity="0.92" stroke="%s" rx="4"/>' % (fy, m.w - 28, m.footer_h - 20, C_LAND_ED))
    for i, (n, lon, lat, ko, it, sub, color) in enumerate(items):
        col, row = divmod(i, 9)
        bx = 32 + col * 410
        by = fy + 24 + row * 19.5
        m.add('<circle cx="%.1f" cy="%.1f" r="8" fill="%s"/>' % (bx, by - 4, color))
        m.text_px(bx, by, str(n), size=10.5, fill="#fff", anchor="middle", weight="700", halo=False)
        m.text_px(bx + 15, by, "%s %s" % (ko, it), size=11.5, weight="600", halo=False)
        m.text_px(bx + 388, by, sub, size=10.5, fill=C_SUB, anchor="end", halo=False)
    m.save("sud-isole.svg")


# ======================================================================== 지도 7
def map_etna():
    """에트나 — 사면별 콘트라다 배치도(모식도)."""
    W, H = 880, 660
    cx, cy, r = 440, 320, 140
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
         'role="img"><rect width="100%%" height="100%%" fill="%s"/>' % (W, H, W, H, C_BG)]
    o.append('<text x="20" y="28" font-size="18" font-weight="700" fill="%s" font-family="%s">'
             '에트나 — 사면별 콘트라다(Contrade)</text>' % (C_TEXT, FONT))
    o.append('<text x="20" y="48" font-size="12.5" fill="%s" font-family="%s">'
             'Etna DOC : 화산 사면을 둘러싼 133개 콘트라다 · 부르고뉴식 단일 구획 표기 체계</text>'
             % (C_SUB, FONT))

    # 화산 사면 동심원
    for rr, op in [(r + 46, 0.16), (r + 8, 0.26), (r - 48, 0.40)]:
        o.append('<circle cx="%d" cy="%d" r="%d" fill="#8a7f72" opacity="%.2f"/>' % (cx, cy, rr, op))
    o.append('<circle cx="%d" cy="%d" r="26" fill="#5a4f45"/>' % (cx, cy))
    o.append('<text x="%d" y="%d" font-size="12" font-weight="700" fill="#fff" '
             'text-anchor="middle" font-family="%s">분화구</text>' % (cx, cy + 4, FONT))
    o.append('<text x="%d" y="%d" font-size="9.5" fill="#d9cfc4" text-anchor="middle" '
             'font-family="%s">3,357 m</text>' % (cx, cy + 16, FONT))

    # 사면별 블록
    slopes = [
        ("북 사면 Nord", 440, 92, "middle", "#8c2f39",
         "Guardiola · Rampante · Santo Spirito · Calderara Sottana · Feudo di Mezzo",
         ["가장 유명 · 고도 600~1,000 m", "서늘하고 섬세 · 최고가 콘트라다 밀집"]),
        ("동 사면 Est", 862, 300, "end", "#a05a3a",
         "Milo · Praino · Caselle · Villagrande",
         ["이오니아해 영향 · 강수량 최다", "카리칸테 화이트 (Bianco Superiore는 밀로만)"]),
        ("남서 사면 Sud-Ovest", 440, 532, "middle", "#7a5a8a",
         "Biancavilla · Santa Maria di Licodia · Contrada Cavaliere",
         ["따뜻하고 풍만 · 재평가 진행 중"]),
        ("서 사면 Ovest", 18, 300, "start", "#5b7f4f",
         "Bronte · Contrada Nave",
         ["가장 고지대 · 최근 개발"]),
    ]
    for name, tx, ty, anchor, color, contrade, notes in slopes:
        o.append('<text x="%d" y="%d" font-size="13.5" font-weight="700" fill="%s" '
                 'text-anchor="%s" font-family="%s">%s</text>' % (tx, ty, color, anchor, FONT, name))
        o.append('<text x="%d" y="%d" font-size="11" fill="%s" text-anchor="%s" '
                 'font-family="%s">%s</text>' % (tx, ty + 17, C_TEXT, anchor, FONT, esc(contrade)))
        for k, note in enumerate(notes):
            o.append('<text x="%d" y="%d" font-size="10.5" fill="%s" text-anchor="%s" '
                     'font-family="%s">%s</text>'
                     % (tx, ty + 33 + k * 14, C_SUB, anchor, FONT, esc(note)))

    # 품종 안내
    box_y = H - 66
    o.append('<rect x="20" y="%d" width="%d" height="52" fill="#ffffff" fill-opacity="0.92" '
             'stroke="%s" rx="4"/>' % (box_y, W - 40, C_LAND_ED))
    o.append('<text x="34" y="%d" font-size="11.5" fill="%s" font-family="%s">'
             '<tspan font-weight="700">레드</tspan> 네렐로 마스칼레제(주) + 네렐로 카푸초   ·   '
             '<tspan font-weight="700">화이트</tspan> 카리칸테 + 카타라토</text>'
             % (box_y + 21, C_TEXT, FONT))
    o.append('<text x="34" y="%d" font-size="11" fill="%s" font-family="%s">'
             '용암류·화산재가 층층이 쌓여 콘트라다마다 토양 연대가 달라진다 — '
             '같은 품종이라도 구획별 성격 차이가 크다</text>' % (box_y + 39, C_SUB, FONT))
    o.append("</svg>")
    p = os.path.join(OUT, "etna.svg")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    print("wrote", p)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    map_italy()
    map_langhe()
    map_barolo_mga()
    map_toscana()
    map_nordest()
    map_sud_isole()
    map_etna()
