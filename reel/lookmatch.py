#!/usr/bin/env python3
# ============================================================
#  Robot de Edición Anthony (REA) · v1.0.0
#  Autor:    Anthony
#  Contacto: WhatsApp +1 (849) 517-8351 · https://wa.me/18495178351
#  Repo:     https://github.com/nickjunior2506-ship-it/robot-edicion-anthony
#  Licencia: MIT (ver LICENSE). Si lo usas o modificas, conserva este crédito.
# ============================================================
"""Extrae el LOOK de un video de referencia y lo hornea como LUT .cube (33^3).
Método: transferencia de color estadística (Reinhard) en Lab. Se conserva la exposición media del material
propio (no copiamos que la referencia sea de noche), se transfiere: contraste (std de L), casta (media de a,b)
y saturación (std de a,b). Ratios acotados para que el LUT sea un "look", no una distorsión.

uso: lookmatch.py ref.rgb src.rgb W H out.cube [nombre]
   ref.rgb / src.rgb = volcados rawvideo rgb24 de N fotogramas de WxH (ffmpeg -f rawvideo -pix_fmt rgb24)
"""
__author__ = "Anthony"
__contact__ = "WhatsApp +1 (849) 517-8351 · https://wa.me/18495178351"
__version__ = "1.0.0"
__project__ = "REA — Robot de Edición Anthony"
import sys, numpy as np

ref_p, src_p, W, H, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
name = sys.argv[6] if len(sys.argv) > 6 else "look"

def load(p):
    a = np.fromfile(p, dtype=np.uint8)
    n = a.size // (W * H * 3)
    return a[: n * W * H * 3].reshape(-1, 3).astype(np.float64) / 255.0

def srgb_to_lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)

def lin_to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055)

M = np.array([[0.4124564, 0.3575761, 0.1804375],
              [0.2126729, 0.7151522, 0.0721750],
              [0.0193339, 0.1191920, 0.9503041]])
Mi = np.linalg.inv(M)
WP = np.array([0.95047, 1.0, 1.08883])

def f_lab(t):
    d = 6 / 29
    return np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4 / 29)

def f_inv(t):
    d = 6 / 29
    return np.where(t > d, t ** 3, 3 * d * d * (t - 4 / 29))

def rgb_to_lab(rgb):
    xyz = srgb_to_lin(rgb) @ M.T / WP
    fx, fy, fz = f_lab(xyz[:, 0]), f_lab(xyz[:, 1]), f_lab(xyz[:, 2])
    return np.stack([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)], 1)

def lab_to_rgb(lab):
    L, a, b = lab[:, 0], lab[:, 1], lab[:, 2]
    fy = (L + 16) / 116; fx = fy + a / 500; fz = fy - b / 200
    xyz = np.stack([f_inv(fx), f_inv(fy), f_inv(fz)], 1) * WP
    return lin_to_srgb(xyz @ Mi.T)

ref, src = rgb_to_lab(load(ref_p)), rgb_to_lab(load(src_p))
# muestreo sobre píxeles "medios" para que negros/blancos quemados no dominen las estadísticas
def stats(x):
    m = (x[:, 0] > 5) & (x[:, 0] < 95)
    return x[m].mean(0), x[m].std(0)
mr, sr = stats(ref); ms, ss = stats(src)

# ratios acotados
kL = float(np.clip(sr[0] / ss[0], 0.85, 1.25))          # contraste
ka = float(np.clip(sr[1] / ss[1], 0.7, 1.5))            # saturación eje a
kb = float(np.clip(sr[2] / ss[2], 0.7, 1.5))            # saturación eje b
da = float(np.clip(mr[1] - ms[1], -10, 10))             # casta verde-magenta
db = float(np.clip(mr[2] - ms[2], -12, 12))             # casta azul-amarillo
print(f"[{name}] ref L/a/b mean={mr.round(1)} std={sr.round(1)} | src mean={ms.round(1)} std={ss.round(1)}")
print(f"[{name}] contraste x{kL:.2f}  sat a x{ka:.2f} b x{kb:.2f}  casta a{da:+.1f} b{db:+.1f}")

N = 33
g = np.linspace(0, 1, N)
# orden .cube: R varía más rápido, luego G, luego B
B, G, R = np.meshgrid(g, g, g, indexing="ij")
lat = np.stack([R.ravel(), G.ravel(), B.ravel()], 1)
lab = rgb_to_lab(lat)
lab[:, 0] = (lab[:, 0] - ms[0]) * kL + ms[0]
lab[:, 1] = (lab[:, 1] - ms[1]) * ka + ms[1] + da
lab[:, 2] = (lab[:, 2] - ms[2]) * kb + ms[2] + db
outrgb = np.clip(lab_to_rgb(lab), 0, 1)
with open(out, "w") as f:
    f.write(f"TITLE \"{name}\"\nLUT_3D_SIZE {N}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n")
    for r, g_, b in outrgb:
        f.write(f"{r:.6f} {g_:.6f} {b:.6f}\n")
print("wrote", out)
