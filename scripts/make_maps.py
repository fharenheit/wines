#!/usr/bin/env python3
"""프랑스 와인 산지 지도(SVG) 생성기.

경위도를 등장방형(equirectangular) 투영으로 픽셀에 매핑해
국경 윤곽 + 주요 하천 + 포도밭 벨트 + 산지 라벨을 그린다.
결과물은 assets/*.svg 로 저장되며 각 문서에서 참조한다.

실행: python3 scripts/make_maps.py
"""

import math
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
FONT = "'Helvetica Neue',Helvetica,Arial,sans-serif"

# ---------------------------------------------------------------- 색상 팔레트
C_BG = "#faf7f2"       # 배경
C_LAND = "#ece5d8"     # 육지
C_LAND_ED = "#c4b8a3"  # 국경선
C_WATER = "#9dc0da"    # 하천/바다
C_TEXT = "#2f2a24"     # 기본 텍스트
C_SUB = "#6b6157"      # 보조 텍스트
C_RED = "#8c2f39"      # 레드 와인 산지
C_WHITE = "#b08a2e"    # 화이트 와인 산지
C_SPARK = "#4f6d7a"    # 스파클링
C_GREEN = "#5b7f4f"    # 우안/보조 구분색
C_PURPLE = "#5c3a63"   # 북부 론

# ------------------------------------------------------------------ 국경 윤곽
FRANCE = [
    (2.38, 51.03), (1.85, 50.95), (1.58, 50.87), (1.58, 50.52), (1.55, 50.20),
    (1.08, 49.93), (0.10, 49.50), (0.23, 49.42), (-0.35, 49.34), (-1.62, 49.68),
    (-1.60, 48.83), (-1.51, 48.63), (-2.02, 48.65), (-3.05, 48.78), (-4.49, 48.39),
    (-4.73, 48.04), (-4.40, 47.80), (-3.37, 47.72), (-3.10, 47.50), (-2.20, 47.28),
    (-2.20, 46.95), (-1.78, 46.50), (-1.15, 46.16), (-1.03, 45.62), (-1.16, 44.66),
    (-1.55, 43.48), (-1.79, 43.35), (-0.75, 42.95), (0.00, 42.70), (1.70, 42.50),
    (3.03, 42.50), (3.15, 43.15), (3.70, 43.40), (4.10, 43.50), (4.60, 43.35),
    (5.37, 43.29), (5.93, 43.10), (6.64, 43.25), (7.27, 43.70), (7.50, 43.78),
    (6.90, 44.35), (7.00, 45.00), (6.80, 45.80), (6.90, 46.05), (6.15, 46.15),
    (6.10, 46.40), (5.95, 46.75), (6.40, 47.00), (7.00, 47.50), (7.59, 47.55),
    (7.60, 48.30), (8.20, 48.97), (7.90, 49.05), (6.35, 49.46), (5.80, 49.55),
    (4.85, 50.15), (4.20, 50.28), (3.66, 50.35), (3.15, 50.53), (2.55, 51.00),
]

CORSICA = [
    (9.36, 43.01), (9.45, 42.72), (9.55, 42.35), (9.55, 41.95), (9.40, 41.60),
    (9.28, 41.38), (8.80, 41.55), (8.75, 41.90), (8.55, 42.25), (8.68, 42.60),
    (9.15, 42.68), (9.20, 42.85),
]

# -------------------------------------------------------------------- 하천망
RIVERS = {
    "Loire": [(4.20, 44.85), (4.07, 46.04), (3.16, 46.99), (2.60, 47.55), (1.90, 47.90),
              (1.33, 47.59), (0.69, 47.39), (-0.08, 47.26), (-0.50, 47.40), (-1.55, 47.21),
              (-2.20, 47.28)],
    "Rhone": [(6.14, 46.20), (5.83, 46.11), (4.84, 45.76), (4.87, 45.52), (4.89, 44.93),
              (4.75, 44.56), (4.81, 44.14), (4.81, 43.95), (4.63, 43.68), (4.85, 43.35)],
    "Saone": [(6.15, 47.90), (5.59, 47.44), (5.10, 47.05), (4.85, 46.78), (4.83, 46.31),
              (4.84, 45.76)],
    "Garonne": [(1.44, 43.60), (0.62, 44.20), (0.16, 44.50), (-0.25, 44.55), (-0.57, 44.84),
                (-0.55, 45.03)],
    "Dordogne": [(1.20, 44.85), (0.48, 44.85), (0.03, 44.86), (-0.24, 44.91), (-0.55, 45.03)],
    "Gironde": [(-0.55, 45.03), (-0.66, 45.13), (-0.74, 45.20), (-0.85, 45.32), (-1.00, 45.45),
                (-1.06, 45.57)],
    "Marne": [(4.90, 48.70), (4.35, 48.95), (3.96, 49.04), (3.40, 49.05), (2.88, 48.96),
              (2.42, 48.82)],
    "Seine": [(4.07, 48.30), (3.50, 48.49), (2.66, 48.54), (2.35, 48.86), (1.10, 49.44),
              (0.10, 49.49)],
    "Yonne": [(3.57, 47.80), (3.40, 47.98), (3.28, 48.20), (2.95, 48.39)],
    "Serein": [(3.85, 47.50), (3.80, 47.82), (3.70, 48.05)],
    "Rhin": [(7.59, 47.56), (7.60, 48.00), (7.80, 48.58), (8.10, 48.80), (8.20, 48.97)],
    "Ill": [(7.30, 47.70), (7.36, 48.08), (7.60, 48.35), (7.75, 48.57)],
    "Allier": [(3.30, 45.30), (3.15, 46.10), (3.16, 46.99)],
    "Aube": [(4.60, 48.10), (4.15, 48.25), (3.72, 48.42), (3.50, 48.49)],
    "Vienne": [(0.34, 46.58), (0.22, 47.18), (0.05, 47.20)],
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Map:
    """경위도 → 픽셀 변환기 + SVG 조립기."""

    def __init__(self, bbox, width, pad=0, title=None, subtitle=None):
        self.lon0, self.lat0, self.lon1, self.lat1 = bbox  # (W, S, E, N)
        self.kx = math.cos(math.radians((self.lat0 + self.lat1) / 2))
        span_x = (self.lon1 - self.lon0) * self.kx
        span_y = self.lat1 - self.lat0
        self.scale = (width - 2 * pad) / span_x
        self.pad = pad
        self.w = width
        self.head_h = 52 if title else 0
        self.h = span_y * self.scale + 2 * pad + self.head_h
        self.title = title
        self.subtitle = subtitle
        self.parts = []

    # -- 좌표 ---------------------------------------------------------------
    def xy(self, lon, lat):
        return (self.pad + (lon - self.lon0) * self.kx * self.scale,
                self.pad + (self.lat1 - lat) * self.scale + self.head_h)

    def path(self, pts, close=True):
        d = "M " + " L ".join("%.1f %.1f" % self.xy(lo, la) for lo, la in pts)
        return d + (" Z" if close else "")

    def add(self, s):
        self.parts.append(s)

    # -- 기본 도형 -----------------------------------------------------------
    def dot(self, lon, lat, r=4.8, fill=C_RED, stroke=C_BG, sw=1.5):
        x, y = self.xy(lon, lat)
        self.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" '
                 'stroke-width="%.1f"/>' % (x, y, r, fill, stroke, sw))

    def square(self, lon, lat, s=6, fill=C_SUB):
        x, y = self.xy(lon, lat)
        self.add('<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="%s"/>'
                 % (x - s / 2, y - s / 2, s, s, fill))

    def text_px(self, x, y, text, size=12, fill=C_TEXT, anchor="start", weight="400",
                halo=True, italic=False, halo_w=3.4):
        t = esc(text)
        st = ' font-style="italic"' if italic else ""
        if halo:
            self.add('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" '
                     'font-weight="%s" fill="none" stroke="%s" stroke-width="%.1f" '
                     'stroke-linejoin="round" font-family="%s"%s>%s</text>'
                     % (x, y, size, anchor, weight, C_BG, halo_w, FONT, st, t))
        self.add('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" '
                 'font-weight="%s" fill="%s" font-family="%s"%s>%s</text>'
                 % (x, y, size, anchor, weight, fill, FONT, st, t))

    def label(self, lon, lat, text, dx=9, dy=4, **kw):
        x, y = self.xy(lon, lat)
        self.text_px(x + dx, y + dy, text, **kw)

    def pin(self, lon, lat, text, dx=9, dy=4, sub=None, color=C_RED, r=4.8, size=12,
            leader=False):
        """점 + (필요 시 지시선) + 라벨. dx<0 이면 라벨이 왼쪽에 붙는다."""
        x, y = self.xy(lon, lat)
        anchor = "start" if dx >= 0 else "end"
        if leader:
            gap = 6 if dx >= 0 else -6
            self.add('<path d="M %.1f %.1f L %.1f %.1f" stroke="%s" stroke-width="0.9" '
                     'fill="none" opacity="0.8"/>' % (x + gap, y, x + dx - gap * 0.5,
                                                      y + dy - 4, C_SUB))
        self.dot(lon, lat, r=r, fill=color)
        self.text_px(x + dx, y + dy, text, size=size, anchor=anchor, weight="600")
        if sub:
            self.text_px(x + dx, y + dy + 14, sub, size=10.8, anchor=anchor,
                         fill=C_SUB, weight="400")

    def belt(self, pts, color, width=9, opacity=0.55):
        """포도밭 벨트(재배 구역)를 굵은 선으로 표현."""
        self.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" '
                 'stroke-linecap="round" stroke-linejoin="round" opacity="%.2f"/>'
                 % (self.path(pts, close=False), color, width, opacity))

    def poly(self, pts, fill, opacity=0.35, stroke="none"):
        self.add('<path d="%s" fill="%s" stroke="%s" opacity="%.2f"/>'
                 % (self.path(pts), fill, stroke, opacity))

    # -- 배경 ----------------------------------------------------------------
    def base(self, rivers=(), river_w=2.2):
        self.add('<g clip-path="url(#frame)">')
        self.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.4"/>'
                 % (self.path(FRANCE), C_LAND, C_LAND_ED))
        self.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.4"/>'
                 % (self.path(CORSICA), C_LAND, C_LAND_ED))
        for name in rivers:
            self.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" '
                     'stroke-linecap="round" stroke-linejoin="round"/>'
                     % (self.path(RIVERS[name], close=False), C_WATER, river_w))
        self.add("</g>")

    def legend(self, items, title=None, x=None, y=None, w=190):
        h = 14 + len(items) * 18 + (18 if title else 0)
        x = self.w - w - 14 if x is None else x
        y = self.h - h - 14 if y is None else y
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#ffffff" '
                 'fill-opacity="0.92" stroke="%s" stroke-width="1" rx="4"/>'
                 % (x, y, w, h, C_LAND_ED))
        yy = y + 18
        if title:
            self.text_px(x + 10, yy, title, size=11.5, weight="700", fill=C_SUB, halo=False)
            yy += 18
        for color, text in items:
            self.add('<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s"/>' % (x + 16, yy - 4, color))
            self.text_px(x + 27, yy, text, size=11.5, halo=False)
            yy += 18

    # -- 출력 ----------------------------------------------------------------
    def render(self):
        head = ""
        if self.title:
            head = ('<text x="%.1f" y="26" font-size="17" font-weight="700" fill="%s" '
                    'font-family="%s">%s</text>' % (self.pad + 2, C_TEXT, FONT, esc(self.title)))
            if self.subtitle:
                head += ('\n<text x="%.1f" y="44" font-size="12" fill="%s" font-family="%s">'
                         '%s</text>' % (self.pad + 2, C_SUB, FONT, esc(self.subtitle)))
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" '
            'width="%.0f" height="%.0f" role="img">\n'
            '<defs><clipPath id="frame"><rect x="0" y="%.0f" width="%.0f" height="%.0f"/>'
            '</clipPath></defs>\n'
            '<rect width="100%%" height="100%%" fill="%s"/>\n%s\n%s\n</svg>\n'
            % (self.w, self.h, self.w, self.h, self.head_h, self.w, self.h - self.head_h,
               C_BG, head, "\n".join(self.parts)))

    def save(self, name):
        p = os.path.join(OUT, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(self.render())
        print("wrote", p)


# ======================================================================== 지도 1
def map_france():
    m = Map((-5.6, 41.2, 10.4, 51.4), 800, pad=14,
            title="프랑스 주요 와인 산지",
            subtitle="Les vignobles de France — 주요 13개 지방")
    m.base(rivers=list(RIVERS.keys()))

    # (경도, 위도, 라벨, 색, dx, dy)
    regions = [
        (4.05, 49.10, "샹파뉴 Champagne", C_SPARK, 10, 4),
        (7.42, 48.15, "알자스 Alsace", C_WHITE, 10, 4),
        (3.80, 47.82, "샤블리 Chablis", C_WHITE, -10, -2),
        (4.90, 47.10, "부르고뉴 Bourgogne", C_RED, 10, -4),
        (4.70, 46.05, "보졸레 Beaujolais", C_RED, -10, 4),
        (5.77, 46.90, "쥐라 Jura", C_WHITE, 10, 12),
        (5.92, 45.57, "사부아 Savoie", C_WHITE, 10, 4),
        (4.85, 45.07, "북부 론 N. Rhône", C_RED, -10, 4),
        (4.83, 44.06, "남부 론 S. Rhône", C_RED, 10, 2),
        (6.05, 43.42, "프로방스 Provence", C_RED, 10, 4),
        (3.20, 43.42, "랑그독 Languedoc", C_RED, -10, -4),
        (2.75, 42.68, "루시용 Roussillon", C_RED, -10, 6),
        (-0.58, 44.84, "보르도 Bordeaux", C_RED, -10, 4),
        (0.90, 44.20, "쉬드우에스트 Sud-Ouest", C_RED, -10, 6),
        (-0.33, 45.69, "코냑 Cognac", C_SUB, -10, 4),
        (0.69, 47.39, "루아르 Loire", C_WHITE, 4, -12),
        (-1.55, 47.21, "뮈스카데 Muscadet", C_WHITE, -10, 6),
        (2.84, 47.33, "상세르 Sancerre", C_WHITE, 10, 6),
        (9.10, 42.20, "코르시카 Corse", C_RED, -10, 4),
    ]
    for lon, lat, name, color, dx, dy in regions:
        m.pin(lon, lat, name, dx=dx, dy=dy, color=color, r=5.2, size=12.5)

    for lon, lat, name, dx, dy in [(2.35, 48.86, "Paris", 8, 3.5), (4.84, 45.76, "Lyon", 8, 3.5),
                                   (5.37, 43.30, "Marseille", -8, 3.5),
                                   (1.44, 43.60, "Toulouse", 0, -10)]:
        m.square(lon, lat)
        m.label(lon, lat, name, dx=dx, dy=dy, size=11, fill=C_SUB,
                anchor="middle" if dx == 0 else ("start" if dx > 0 else "end"))

    m.legend([(C_RED, "레드 중심"), (C_WHITE, "화이트 중심"), (C_SPARK, "스파클링")],
             title="주요 스타일", x=16, y=m.h - 100, w=170)
    m.save("france-overview.svg")


# ======================================================================== 지도 2
def map_bordeaux():
    m = Map((-1.30, 44.32, 0.72, 45.72), 780, pad=16,
            title="보르도 — 좌안 / 우안",
            subtitle="Rive Gauche (자갈·카베르네 소비뇽) / Rive Droite (점토·석회, 메를로)")
    m.base(rivers=[], river_w=0)

    # 지롱드 하구 + 두 강을 면(面)으로 표현
    m.add('<g clip-path="url(#frame)">')
    m.add('<path d="%s" fill="%s"/>' % (m.path([
        (-1.02, 45.60), (-0.96, 45.60), (-0.80, 45.36), (-0.62, 45.14),
        (-0.53, 45.02), (-0.58, 44.98), (-0.68, 45.12), (-0.86, 45.34),
        (-1.10, 45.58)]), C_WATER))
    for pts, wdt in [(RIVERS["Garonne"], 4.2), (RIVERS["Dordogne"], 4.2)]:
        m.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" '
              'stroke-linecap="round"/>' % (m.path(pts, close=False), C_WATER, wdt))
    m.add("</g>")

    # 좌안 / 우안 음영
    m.poly([(-1.12, 45.58), (-0.72, 45.30), (-0.50, 44.95), (-0.28, 44.62),
            (-0.12, 44.42), (-0.55, 44.38), (-0.85, 44.60), (-1.18, 45.05)],
           "#7fa3c0", opacity=0.22)
    m.poly([(-0.52, 45.16), (-0.10, 45.10), (0.45, 45.02), (0.55, 44.72),
            (-0.02, 44.78), (-0.34, 44.92)], "#b98a5e", opacity=0.22)

    x, y = m.xy(-1.00, 45.30)
    m.text_px(x, y, "좌안 RIVE GAUCHE", size=13.5, fill="#3f5f7c", weight="700",
              anchor="middle")
    x, y = m.xy(0.28, 45.12)
    m.text_px(x, y, "우안 RIVE DROITE", size=13.5, fill="#8a5a3c", weight="700",
              anchor="middle")
    x, y = m.xy(-0.90, 45.50)
    m.text_px(x, y, "지롱드 강 어귀", size=11, fill="#3f6a8a", weight="600", anchor="middle")

    left = [
        (-0.755, 45.265, "생테스테프 St-Estèphe", -10, 4),
        (-0.750, 45.200, "포이약 Pauillac", -10, 4),
        (-0.770, 45.150, "생쥘리앵 St-Julien", -10, 4),
        (-0.870, 45.083, "리스트락 Listrac", -10, 0),
        (-0.815, 45.058, "물리 Moulis", -10, 4),
        (-0.677, 45.041, "마고 Margaux", -10, 22),
        (-0.630, 44.790, "페삭레오냥 Pessac-Léognan", -10, 4),
        (-0.430, 44.660, "그라브 Graves", -10, 4),
        (-0.320, 44.535, "소테른·바르삭 Sauternes / Barsac", -10, 4),
    ]
    right = [
        (-0.665, 45.130, "블라이 Blaye", 10),
        (-0.560, 45.040, "부르 Bourg", 10),
        (-0.320, 44.930, "프롱삭 Fronsac", -10),
        (-0.200, 44.940, "포므롤 Pomerol", 10),
        (-0.155, 44.885, "생테밀리옹 St-Émilion", 10),
        (0.030, 44.845, "카스티용 Castillon", 10),
    ]
    for lon, lat, name, dx, dy in left:
        m.pin(lon, lat, name, dx=dx, dy=dy, color=C_RED, r=5.0, size=12, leader=dy > 14)
    for lon, lat, name, dx in right:
        m.pin(lon, lat, name, dx=dx, dy=4, color=C_GREEN, r=5.0, size=12)

    m.pin(-0.300, 44.720, "앙트르되메르 Entre-Deux-Mers", dx=10, dy=4, color=C_SUB,
          r=4.2, size=11.5)

    m.square(-0.575, 44.838, s=8, fill=C_TEXT)
    m.label(-0.575, 44.838, "보르도 시", dx=-10, dy=4, size=12, anchor="end")

    m.legend([(C_RED, "좌안 코뮌"), (C_GREEN, "우안 코뮌"), (C_SUB, "기타 광역 AOC")],
             x=16, y=m.h - 90, w=160)
    m.save("bordeaux.svg")


# ======================================================================== 지도 3
def map_cote_dor():
    """코트도르 — 마을과 그랑크뤼를 남북 축으로 배열한 스트립 맵."""
    W, TOP, ROW = 1080, 92, 31.0
    villages = [
        ("마르사네 Marsannay", "", "Clos du Roy · Les Longeroies (리외디)", "N"),
        ("픽생 Fixin", "1er", "Clos de la Perrière · Clos du Chapitre", "N"),
        ("주브레샹베르탱 Gevrey-Chambertin", "GC 9",
         "Chambertin · Clos de Bèze · Charmes · Mazis · Griotte · Latricières · Ruchottes · Chapelle", "N"),
        ("모레생드니 Morey-St-Denis", "GC 5",
         "Clos de la Roche · Clos St-Denis · Clos de Tart · Clos des Lambrays · Bonnes-Mares(일부)", "N"),
        ("샹볼뮈지니 Chambolle-Musigny", "GC 2",
         "Musigny · Bonnes-Mares   |   1er Les Amoureuses · Les Charmes", "N"),
        ("부조 Vougeot", "GC 1", "Clos de Vougeot (50.6ha · 80여 소유주)", "N"),
        ("본로마네 Vosne-Romanée", "GC 8",
         "Romanée-Conti · La Tâche · Richebourg · Romanée-St-Vivant · La Romanée · La Grande Rue · Échezeaux", "N"),
        ("뉘생조르주 Nuits-St-Georges", "1er",
         "Les St-Georges · Les Vaucrains · Les Cailles · Clos de la Maréchale (그랑크뤼 없음)", "N"),
        ("라두아세리니 Ladoix-Serrigny", "GC", "Corton (일부)", "B"),
        ("알록스코르통 Aloxe-Corton", "GC 2", "Corton (레드) · Corton-Charlemagne (화이트)", "B"),
        ("페르낭베르줄레스 Pernand-Vergelesses", "GC",
         "Corton-Charlemagne (일부)   |   1er Île des Vergelesses", "B"),
        ("사비니레본 Savigny-lès-Beaune", "1er", "Les Vergelesses · Les Lavières · Les Serpentières", "B"),
        ("본 Beaune", "1er", "Les Grèves · Clos des Mouches · Bressandes · Clos du Roi", "B"),
        ("포마르 Pommard", "1er", "Les Rugiens · Les Épenots · Clos des Épeneaux", "B"),
        ("볼네 Volnay", "1er", "Clos des Chênes · Caillerets · Taillepieds · Clos des Ducs", "B"),
        ("뫼르소 Meursault", "1er", "Les Perrières · Genevrières · Charmes · Poruzots", "B"),
        ("퓔리니몽라셰 Puligny-Montrachet", "GC 4",
         "Montrachet · Chevalier-Montrachet · Bâtard-Montrachet · Bienvenues-Bâtard", "B"),
        ("샤사뉴몽라셰 Chassagne-Montrachet", "GC 3",
         "Montrachet(일부) · Bâtard(일부) · Criots-Bâtard-Montrachet", "B"),
        ("생토뱅 St-Aubin", "1er", "En Remilly · Les Murgers des Dents de Chien", "B"),
        ("상트네 Santenay", "1er", "Les Gravières · Clos de Tavannes", "B"),
        ("마랑주 Maranges", "1er", "Clos des Loyères · La Fussière", "B"),
    ]
    H = TOP + len(villages) * ROW + 46
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
         'role="img"><rect width="100%%" height="100%%" fill="%s"/>' % (W, H, W, H, C_BG)]
    o.append('<text x="20" y="28" font-size="18" font-weight="700" fill="%s" font-family="%s">'
             '코트도르 — 마을별 그랑크뤼 배열 (북 → 남)</text>' % (C_TEXT, FONT))
    o.append('<text x="20" y="48" font-size="12.5" fill="%s" font-family="%s">'
             'La Côte d\'Or : Côte de Nuits (피노 누아) → Côte de Beaune (샤르도네 · 피노 누아)</text>'
             % (C_SUB, FONT))
    o.append('<text x="20" y="70" font-size="11.5" fill="%s" font-family="%s">'
             '↑ 북 Dijon  ·  포도밭은 동향(東向) 사면에 띠처럼 이어지며, 그랑크뤼는 대개 사면 중턱에 위치한다  ·  '
             '↓ 남 Santenay</text>' % (C_SUB, FONT))

    xl, col_w = 20, 268
    for i, (name, grade, crus, sec) in enumerate(villages):
        y = TOP + i * ROW
        cy = y + ROW / 2
        o.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="%s"/>'
                 % (xl, y, W - 40, ROW, "#f4efe6" if i % 2 == 0 else "#ffffff"))
        acc = C_RED if sec == "N" else C_WHITE
        o.append('<rect x="%d" y="%.1f" width="5" height="%.1f" fill="%s"/>' % (xl, y, ROW, acc))
        o.append('<text x="%d" y="%.1f" font-size="12.5" font-weight="700" fill="%s" '
                 'font-family="%s">%s</text>' % (xl + 15, cy + 4, C_TEXT, FONT, esc(name)))
        if grade:
            o.append('<rect x="%d" y="%.1f" width="44" height="17" rx="8.5" fill="%s"/>'
                     % (xl + col_w, cy - 12, acc))
            o.append('<text x="%d" y="%.1f" font-size="10.5" font-weight="700" fill="#fff" '
                     'text-anchor="middle" font-family="%s">%s</text>'
                     % (xl + col_w + 22, cy + 1, FONT, esc(grade)))
        o.append('<text x="%d" y="%.1f" font-size="11.5" fill="%s" font-family="%s">%s</text>'
                 % (xl + col_w + 56, cy + 4, C_SUB, FONT, esc(crus)))

    yl = TOP + len(villages) * ROW + 26
    o.append('<circle cx="30" cy="%.1f" r="5" fill="%s"/>' % (yl - 4, C_RED))
    o.append('<text x="42" y="%.1f" font-size="11.5" fill="%s" font-family="%s">Côte de Nuits</text>'
             % (yl, C_TEXT, FONT))
    o.append('<circle cx="176" cy="%.1f" r="5" fill="%s"/>' % (yl - 4, C_WHITE))
    o.append('<text x="188" y="%.1f" font-size="11.5" fill="%s" font-family="%s">Côte de Beaune</text>'
             % (yl, C_TEXT, FONT))
    o.append('<text x="340" y="%.1f" font-size="11.5" fill="%s" font-family="%s">'
             'GC n = 마을이 보유한 그랑크뤼 수 · 1er = 그랑크뤼 없이 프리미에 크뤼가 정점</text>'
             % (yl, C_SUB, FONT))
    o.append("</svg>")
    p = os.path.join(OUT, "cote-dor.svg")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(o))
    print("wrote", p)


# ======================================================================== 지도 4
def map_bourgogne():
    m = Map((3.00, 45.60, 6.10, 48.20), 660, pad=16,
            title="부르고뉴 — 6개 하위 산지",
            subtitle="Chablis → Côte de Nuits → Côte de Beaune → Côte Chalonnaise → Mâconnais → Beaujolais")
    m.base(rivers=["Saone", "Yonne", "Serein", "Loire", "Rhone", "Seine"], river_w=2.6)

    # 포도밭 벨트
    m.belt([(3.72, 47.92), (3.82, 47.80), (3.92, 47.70)], C_WHITE, width=16, opacity=0.5)
    m.belt([(5.00, 47.34), (4.94, 47.22), (4.86, 47.10)], C_RED, width=11, opacity=0.6)
    m.belt([(4.86, 47.10), (4.80, 46.98), (4.72, 46.88)], C_WHITE, width=11, opacity=0.6)
    m.belt([(4.76, 46.86), (4.70, 46.70), (4.66, 46.55)], C_RED, width=10, opacity=0.5)
    m.belt([(4.72, 46.52), (4.72, 46.36), (4.72, 46.22)], C_WHITE, width=10, opacity=0.5)
    m.belt([(4.66, 46.20), (4.68, 46.05), (4.72, 45.88)], "#a34a3a", width=10, opacity=0.5)

    zones = [
        (3.80, 47.82, "샤블리 Chablis", C_WHITE, 14, 0, "샤르도네 · GC 7 클리마"),
        (4.95, 47.28, "코트드뉘 Côte de Nuits", C_RED, 14, -2, "레드 그랑크뤼의 심장"),
        (4.83, 47.03, "코트드본 Côte de Beaune", C_RED, 14, 6, "화이트 그랑크뤼 · 몽라셰"),
        (4.70, 46.70, "코트샬로네즈 Côte Chalonnaise", C_RED, 14, 4, "메르퀴레 · 지브리"),
        (4.72, 46.34, "마코네 Mâconnais", C_WHITE, 14, 4, "푸이퓌세 · 생베랑"),
        (4.68, 46.03, "보졸레 Beaujolais", "#a34a3a", 14, 4, "가메 · 10개 크뤼"),
    ]
    for lon, lat, name, color, dx, dy, sub in zones:
        m.pin(lon, lat, name, dx=dx, dy=dy, sub=sub, color=color, r=5.6, size=13)

    for lon, lat, name, dx, dy in [(3.57, 47.80, "Auxerre", -9, 3.5), (5.04, 47.32, "Dijon", 0, -10),
                                   (4.84, 47.02, "Beaune", -9, 3.5),
                                   (4.85, 46.78, "Chalon-s-Saône", -9, 3.5),
                                   (4.83, 46.31, "Mâcon", 0, 16), (4.84, 45.76, "Lyon", -9, 3.5)]:
        m.square(lon, lat)
        m.label(lon, lat, name, dx=dx, dy=dy, size=11, fill=C_SUB,
                anchor="middle" if dx == 0 else "end")

    m.legend([(C_RED, "피노 누아 중심"), (C_WHITE, "샤르도네 중심"), ("#a34a3a", "가메")],
             x=16, y=m.h - 90, w=170)
    m.save("bourgogne.svg")


# ======================================================================== 지도 5
def map_rhone():
    m = Map((3.55, 43.55, 6.35, 45.95), 660, pad=16,
            title="론 밸리 — 북부 / 남부",
            subtitle="Vallée du Rhône : Nord (시라 단일 품종) / Sud (그르나슈 중심 블렌드)")
    m.base(rivers=["Rhone", "Saone", "Loire"], river_w=4.6)

    m.belt([(4.85, 45.52), (4.83, 45.30), (4.86, 45.05), (4.82, 44.85)], C_PURPLE,
           width=13, opacity=0.35)
    m.belt([(4.60, 44.35), (4.85, 44.20), (5.15, 44.25), (5.05, 44.05), (4.70, 44.00)],
           C_RED, width=16, opacity=0.28)

    north = [
        (4.87, 45.50, "코트로티 Côte-Rôtie", 10, -2),
        (4.78, 45.46, "콩드리외 Condrieu", -10, 6),
        (4.77, 45.41, "샤토그리예 Château-Grillet", -10, 8),
        (4.79, 45.25, "생조제프 St-Joseph", -10, 4),
        (4.86, 45.07, "에르미타주 Hermitage", 10, -3),
        (4.96, 45.01, "크로즈에르미타주 Crozes-Hermitage", 10, 9),
        (4.78, 44.87, "코르나스 Cornas", -10, 0),
        (4.80, 44.82, "생페레 St-Péray", -10, 11),
    ]
    south = [
        (4.81, 44.09, "샤토뇌프뒤파프 Châteauneuf-du-Pape", -10, 4),
        (5.00, 44.19, "지공다스 Gigondas", 10, -2),
        (5.03, 44.12, "바케라스 Vacqueyras", 10, 8),
        (5.04, 44.29, "라스토 Rasteau", 10, -2),
        (4.93, 44.245, "케란 Cairanne", -10, 2),
        (4.65, 44.02, "리락 Lirac", -10, -4),
        (4.69, 43.96, "타벨 Tavel", -10, 8),
        (5.16, 44.36, "뱅소브르 Vinsobres", 10, 4),
    ]
    for lon, lat, name, dx, dy in north:
        m.pin(lon, lat, name, dx=dx, dy=dy, color=C_PURPLE, r=4.8, size=11.5)
    for lon, lat, name, dx, dy in south:
        m.pin(lon, lat, name, dx=dx, dy=dy, color=C_RED, r=4.8, size=11.5)

    for lon, lat, name, dx in [(4.84, 45.76, "Lyon", 9), (4.89, 44.93, "Valence", 9),
                               (4.81, 43.95, "Avignon", 9), (4.36, 43.83, "Nîmes", -9)]:
        m.square(lon, lat)
        m.label(lon, lat, name, dx=dx, dy=3.5, size=11, fill=C_SUB,
                anchor="start" if dx > 0 else "end")

    x, y = m.xy(4.20, 45.20)
    m.text_px(x, y, "북부 론", size=14, fill=C_PURPLE, weight="700", anchor="middle")
    x, y = m.xy(4.05, 44.25)
    m.text_px(x, y, "남부 론", size=14, fill=C_RED, weight="700", anchor="middle")

    m.legend([(C_PURPLE, "북부 론 (시라)"), (C_RED, "남부 론 (GSM)")], x=16, y=m.h - 72, w=170)
    m.save("rhone.svg")


# ======================================================================== 지도 6
def map_loire():
    """루아르는 산지가 강을 따라 촘촘해 라벨이 겹친다 → 번호 마커 + 하단 범례."""
    m = Map((-2.45, 46.70, 3.45, 48.15), 940, pad=16,
            title="루아르 — 하류에서 상류로",
            subtitle="Pays Nantais → Anjou-Saumur → Touraine → Centre-Loire")
    m.footer_h = 132
    m.h += m.footer_h
    m.base(rivers=["Loire", "Vienne", "Allier"], river_w=4.6)

    m.belt([(-1.75, 47.13), (-1.30, 47.14), (-1.02, 47.20)], C_WHITE, width=12, opacity=0.45)
    m.belt([(-0.72, 47.38), (-0.45, 47.22), (-0.20, 47.20)], C_WHITE, width=12, opacity=0.45)
    m.belt([(-0.10, 47.24), (0.30, 47.28), (0.95, 47.38)], C_WHITE, width=12, opacity=0.45)
    m.belt([(2.78, 47.40), (2.95, 47.28), (3.08, 47.18)], C_WHITE, width=12, opacity=0.45)

    # (번호, 경도, 위도, 한글, 원어, 품종/비고, 색)
    items = [
        (1, -1.55, 47.16, "뮈스카데", "Muscadet Sèvre-et-Maine", "믈롱 드 부르고뉴", C_WHITE),
        (2, -0.62, 47.38, "사브니에르", "Savennières", "슈냉 블랑 (드라이)", C_WHITE),
        (3, -0.52, 47.20, "코토뒤레용·카르드숌", "Coteaux du Layon / Quarts de Chaume",
         "슈냉 블랑 (스위트)", C_WHITE),
        (4, -0.08, 47.26, "소뮈르샹피니", "Saumur-Champigny", "카베르네 프랑", C_RED),
        (5, 0.18, 47.29, "부르괴이", "Bourgueil / St-Nicolas", "카베르네 프랑", C_RED),
        (6, 0.24, 47.17, "시농", "Chinon", "카베르네 프랑", C_RED),
        (7, 0.79, 47.42, "부브레", "Vouvray", "슈냉 블랑 (전 스타일)", C_WHITE),
        (8, 0.83, 47.34, "몽루이", "Montlouis-sur-Loire", "슈냉 블랑", C_WHITE),
        (9, 2.84, 47.33, "상세르", "Sancerre", "소비뇽 블랑", C_WHITE),
        (10, 3.01, 47.28, "푸이퓌메", "Pouilly-Fumé", "소비뇽 블랑", C_WHITE),
    ]
    for n, lon, lat, ko, fr, grape, color in items:
        x, y = m.xy(lon, lat)
        m.add('<circle cx="%.1f" cy="%.1f" r="10" fill="%s" stroke="%s" stroke-width="1.6"/>'
              % (x, y, color, C_BG))
        m.text_px(x, y + 4, str(n), size=12, fill="#ffffff", anchor="middle", weight="700",
                  halo=False)

    for lon, lat, name, dx, dy in [(-1.55, 47.21, "Nantes", 0, -16),
                                   (-0.55, 47.47, "Angers", 0, -10),
                                   (0.69, 47.39, "Tours", -16, 4),
                                   (1.90, 47.90, "Orléans", 0, -10)]:
        m.square(lon, lat)
        m.label(lon, lat, name, dx=dx, dy=dy, size=11, fill=C_SUB,
                anchor="middle" if dx == 0 else "end")

    # 하단 3열 범례
    fy = m.h - m.footer_h + 6
    m.add('<rect x="14" y="%.1f" width="%.1f" height="%.1f" fill="#ffffff" '
          'fill-opacity="0.92" stroke="%s" rx="4"/>' % (fy, m.w - 28, m.footer_h - 20, C_LAND_ED))
    for i, (n, lon, lat, ko, fr, grape, color) in enumerate(items):
        col, row = divmod(i, 5)
        bx = 30 + col * 460
        by = fy + 24 + row * 19
        m.add('<circle cx="%.1f" cy="%.1f" r="8" fill="%s"/>' % (bx, by - 4, color))
        m.text_px(bx, by, str(n), size=10.5, fill="#fff", anchor="middle", weight="700", halo=False)
        m.text_px(bx + 15, by, "%s %s" % (ko, fr), size=11.5, weight="600", halo=False)
        m.text_px(bx + 440, by, grape, size=11, fill=C_SUB, anchor="end", halo=False)
    m.save("loire.svg")


# ======================================================================== 지도 7
def map_champagne():
    m = Map((2.55, 47.85, 5.15, 49.55), 660, pad=16,
            title="샹파뉴 — 5개 하위 지구",
            subtitle="Montagne de Reims · Vallée de la Marne · Côte des Blancs · Côte de Sézanne · Côte des Bar")
    m.base(rivers=["Marne", "Seine", "Aube"], river_w=3.4)

    m.belt([(3.95, 49.24), (4.20, 49.18), (4.22, 49.06), (4.02, 49.02)], "#7a3b4a",
           width=14, opacity=0.35)
    m.belt([(3.45, 49.05), (3.70, 49.05), (3.95, 49.04)], "#6b7a3b", width=13, opacity=0.35)
    m.belt([(4.00, 49.00), (4.02, 48.92), (4.00, 48.84)], C_WHITE, width=13, opacity=0.4)
    m.belt([(3.70, 48.88), (3.76, 48.80)], C_WHITE, width=12, opacity=0.35)
    m.belt([(4.30, 48.18), (4.20, 48.08), (4.35, 48.00)], "#7a3b4a", width=14, opacity=0.35)

    zones = [
        (4.12, 49.15, "몽타뉴드랭스 Montagne de Reims", "#7a3b4a", 12, 2, "피노 누아 · Verzenay/Ambonnay"),
        (3.62, 49.05, "발레드라마른 Vallée de la Marne", "#6b7a3b", -12, -6, "피노 뫼니에 · Aÿ"),
        (4.02, 48.90, "코트데블랑 Côte des Blancs", C_WHITE, 12, 4, "샤르도네 · Le Mesnil/Cramant"),
        (3.73, 48.84, "코트드세잔 Côte de Sézanne", C_WHITE, -12, 6, "샤르도네"),
        (4.28, 48.10, "코트데바르 Côte des Bar", "#7a3b4a", 12, 4, "피노 누아 · Les Riceys"),
    ]
    for lon, lat, name, color, dx, dy, sub in zones:
        m.pin(lon, lat, name, dx=dx, dy=dy, sub=sub, color=color, r=6.0, size=12.5)

    for lon, lat, name in [(4.03, 49.26, "Reims"), (3.96, 49.04, "Épernay"),
                           (4.07, 48.30, "Troyes")]:
        m.square(lon, lat, s=7, fill=C_TEXT)
        m.label(lon, lat, name, dx=0, dy=-10, size=11.5, anchor="middle")
    m.save("champagne.svg")


# ======================================================================== 지도 8
def map_alsace():
    m = Map((6.60, 47.70, 8.35, 49.15), 560, pad=16,
            title="알자스 — 북(바랭) / 남(오랭)",
            subtitle="보주 산맥 동쪽 기슭을 따라 남북 약 120 km · 그랑크뤼 51개")
    m.base(rivers=["Rhin", "Ill"], river_w=4.0)

    m.belt([(7.36, 48.95), (7.40, 48.75), (7.42, 48.55), (7.38, 48.35),
            (7.32, 48.18), (7.28, 48.02), (7.20, 47.88)], C_WHITE, width=13, opacity=0.45)

    pts = [
        (7.35, 48.94, "클레부르 Cleebourg", 12),
        (7.42, 48.75, "몰샤임 Molsheim", 12),
        (7.44, 48.55, "바르 Barr · Kirchberg de Barr", 12),
        (7.40, 48.38, "당바크라빌 Dambach-la-Ville · Frankstein", 12),
        (7.34, 48.25, "리보빌레 Ribeauvillé · Geisberg/Osterberg", 12),
        (7.30, 48.17, "리크비르 Riquewihr · Schoenenbourg", 12),
        (7.28, 48.10, "카이제르스베르 Kaysersberg · Schlossberg", 12),
        (7.36, 48.04, "콜마르 Colmar · Brand / Hengst", 12),
        (7.27, 47.95, "게브빌레르 Guebwiller · Kitterlé/Kessler", 12),
        (7.20, 47.86, "탄 Thann · Rangen", 12),
    ]
    for lon, lat, name, dx in pts:
        m.pin(lon, lat, name, dx=dx, dy=4, color=C_WHITE, r=4.8, size=11.5)

    m.square(7.75, 48.58, s=7, fill=C_TEXT)
    m.label(7.75, 48.58, "Strasbourg", dx=9, dy=4, size=11.5)
    x, y = m.xy(6.90, 48.45)
    m.text_px(x, y, "보주 산맥", size=12.5, fill=C_SUB, anchor="middle", weight="700")
    m.text_px(x, y + 15, "Vosges", size=10.5, fill=C_SUB, anchor="middle", italic=True)
    x, y = m.xy(8.05, 48.30)
    m.text_px(x, y, "라인 강", size=11.5, fill="#4b7d9e", anchor="middle", weight="600")
    m.save("alsace.svg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    map_france()
    map_bordeaux()
    map_cote_dor()
    map_bourgogne()
    map_rhone()
    map_loire()
    map_champagne()
    map_alsace()
