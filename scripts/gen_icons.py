import os, zlib, struct

OUT = r"C:\Project\MonitorCompare\icons"
os.makedirs(OUT, exist_ok=True)

# 색상 (RGB) — 앱 팔레트와 동일
BG     = (15, 17, 21)      # #0f1115 다크 배경
BEZEL  = (58, 64, 78)      # 베젤/테두리 (양쪽 모니터 공통)
BLUE   = (79, 140, 255)    # #4f8cff 큰 모니터 화면
ORANGE = (255, 122, 89)    # #ff7a59 작은 모니터 화면
STAND  = (120, 130, 150)   # 스탠드(중립 회색)

# 정규화 좌표로 정의한 도형 (x0,y0,x1,y1,r,color) — 순서대로 위에 덮어 그림
# 크기가 다른 두 모니터를 같은 바닥선(y≈0.665)에 겹쳐 배치해 "비교"를 표현
def shapes():
    return [
        # 큰 모니터 (파랑) — 스탠드 먼저, 그 위에 화면
        (0.32, 0.66, 0.38, 0.755, 0.010, STAND),   # 목
        (0.25, 0.755, 0.45, 0.805, 0.022, STAND),  # 받침
        (0.12, 0.18, 0.58, 0.685, 0.048, BEZEL),   # 베젤
        (0.14, 0.20, 0.56, 0.665, 0.030, BLUE),    # 화면
        # 작은 모니터 (주황) — 앞쪽(위에) 겹쳐 그림, 바닥선 동일
        (0.65, 0.665, 0.71, 0.745, 0.010, STAND),  # 목
        (0.585, 0.745, 0.775, 0.79, 0.020, STAND), # 받침
        (0.49, 0.35, 0.87, 0.685, 0.042, BEZEL),   # 베젤
        (0.51, 0.37, 0.85, 0.665, 0.027, ORANGE),  # 화면
    ]

def inside_rr(px, py, x0, y0, x1, y1, r):
    if px < x0 or px > x1 or py < y0 or py > y1:
        return False
    cx = min(max(px, x0 + r), x1 - r)
    cy = min(max(py, y0 + r), y1 - r)
    dx = px - cx; dy = py - cy
    return dx * dx + dy * dy <= r * r

def render(size, ss=4):
    hi = size * ss
    # 고해상도 버퍼 (배경으로 채움)
    buf = bytearray(BG * (hi * hi))
    for (nx0, ny0, nx1, ny1, nr, col) in shapes():
        x0 = nx0 * hi; y0 = ny0 * hi; x1 = nx1 * hi; y1 = ny1 * hi; r = nr * hi
        bx0 = max(0, int(x0)); by0 = max(0, int(y0))
        bx1 = min(hi, int(x1) + 1); by1 = min(hi, int(y1) + 1)
        c0, c1, c2 = col
        for yy in range(by0, by1):
            py = yy + 0.5
            row = yy * hi
            for xx in range(bx0, bx1):
                if inside_rr(xx + 0.5, py, x0, y0, x1, y1, r):
                    i = (row + xx) * 3
                    buf[i] = c0; buf[i + 1] = c1; buf[i + 2] = c2
    # 다운샘플 (ss x ss 박스 평균) -> 안티에일리어싱
    out = bytearray(size * size * 3)
    inv = 1.0 / (ss * ss)
    for oy in range(size):
        for ox in range(size):
            r = g = b = 0
            base_y = oy * ss
            base_x = ox * ss
            for sy in range(ss):
                ri = ((base_y + sy) * hi + base_x) * 3
                for sx in range(ss):
                    r += buf[ri]; g += buf[ri + 1]; b += buf[ri + 2]
                    ri += 3
            oi = (oy * size + ox) * 3
            out[oi] = int(r * inv); out[oi + 1] = int(g * inv); out[oi + 2] = int(b * inv)
    return bytes(out)

def write_png(path, size, rgb):
    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)  # RGB, 8bit
    raw = bytearray()
    for y in range(size):
        raw.append(0)  # filter: none
        raw += rgb[y * size * 3:(y + 1) * size * 3]
    idat = zlib.compress(bytes(raw), 9)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)

targets = [
    ("icon-192.png", 192),
    ("icon-512.png", 512),
    ("apple-touch-icon.png", 180),
    ("favicon-32.png", 32),
]
for name, size in targets:
    rgb = render(size, ss=4 if size <= 256 else 3)
    write_png(os.path.join(OUT, name), size, rgb)
    print("wrote", name, size)
print("done")
