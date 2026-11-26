"""Justin's seven elementary folds (L'Ouvert 42, 1986, p. 15), redrawn.
Every fold line is computed, not sketched. Also checks Justin's trisection (his section 4.3)."""
import numpy as np
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams.update({
    "font.family": "STIXGeneral", "mathtext.fontset": "stix",
    "svg.fonttype": "path", "font.size": 13,
})
ACC = "#d9480f"   # site accent: fold lines
INK = "#222222"
GREY = "#8a8a8a"

def unit(v):
    v = np.asarray(v, float); return v / np.hypot(*v)

def line_pd(p, direction):
    """Line through p with given direction -> (unit normal a, offset b): a.x = b"""
    u = unit(direction); a = np.array([-u[1], u[0]]); return a, a @ np.asarray(p, float)

def reflect(X, n, d):
    X = np.asarray(X, float); return X - 2 * (n @ X - d) * n

def bisector(P, Q):
    n = unit(np.subtract(Q, P)); return n, n @ (np.add(P, Q) / 2)

def beloch(P, D, P2, D2):
    """All folds placing P on D and P2 on D2. D, D2 given as (a, b). Returns list of (n, d)."""
    (a, b), (a2, b2) = D, D2
    def d_of(phi):
        n = np.array([np.cos(phi), np.sin(phi)])
        return n, n @ P - (a @ P - b) / (2 * (a @ n))
    def g(phi):
        n, d = d_of(phi); return a2 @ reflect(P2, n, d) - b2
    sols, phis = [], np.linspace(1e-4, np.pi - 1e-4, 20001)
    vals = np.array([g(p) for p in phis])
    for i in range(len(phis) - 1):
        if np.isfinite(vals[i]) and np.isfinite(vals[i + 1]) and vals[i] * vals[i + 1] < 0:
            r = brentq(g, phis[i], phis[i + 1], xtol=1e-14)
            if abs(g(r)) < 1e-8:          # a true root, not a pole of g
                sols.append(d_of(r))
    return sols

# ---------- check Justin's trisection, section 4.3 ----------
def check_trisection():
    for deg in (30, 50, 75, 100, 140):
        th = np.radians(deg)
        P = 1.3 * np.array([np.cos(th), np.sin(th)]); P2 = np.array([P[0], -P[1]])
        Ox = line_pd((0, 0), (1, 0)); Oz = line_pd((0, 0), (np.cos(th), np.sin(th)))
        sols = beloch(P, Ox, P2, Oz)
        angs = sorted(np.degrees(np.arctan2(n[1], n[0])) % 180 for n, d in sols)
        ok = any(abs(a - deg / 3) < 1e-6 for a in angs)
        print(f"theta={deg:4d}  folds={len(sols)}  normals at {np.round(angs, 4)}  theta/3={deg/3:.4f}  {'OK' if ok else 'FAIL'}")

# ---------- drawing helpers ----------
def seg(ax, n, d, lim, **kw):
    """Draw the part of line n.x = d inside the box [-lim, lim]^2."""
    u = np.array([-n[1], n[0]]); p0 = n * d
    ts = []
    for k in (0, 1):
        if abs(u[k]) > 1e-12:
            for s in (-lim, lim):
                t = (s - p0[k]) / u[k]; q = p0 + t * u
                if np.all(np.abs(q) <= lim + 1e-9): ts.append(t)
    if len(ts) >= 2:
        A, B = p0 + min(ts) * u, p0 + max(ts) * u
        ax.plot([A[0], B[0]], [A[1], B[1]], **kw)

def given(ax, D, lim, label, at, off=(0, 0)):
    a, b = D; seg(ax, a, b, lim, color=INK, lw=1.3, solid_capstyle="round", zorder=2)
    u = np.array([-a[1], a[0]]); q = a * b + at * u
    ax.annotate(label, q, xytext=off, textcoords="offset points", color=INK, fontsize=16, ha="center", va="center")

def pt(ax, P, label, off=(7, 6)):
    ax.plot(*P, "o", color=INK, ms=6, zorder=5)
    ax.annotate(label, P, xytext=off, textcoords="offset points", fontsize=16, color=INK, ha="center", va="center")

def fold(ax, n, d, lim, main=True):
    seg(ax, n, d, lim, color=ACC, lw=1.7 if main else 1.2, ls=(0, (5, 3)), alpha=1 if main else .55, zorder=3)

def move(ax, P, n, d, mark=True):
    Q = reflect(P, n, d)
    ax.annotate("", Q, P, arrowprops=dict(arrowstyle="->", color=GREY, lw=.9, shrinkA=4, shrinkB=4,
                                          connectionstyle="arc3,rad=0.28"), zorder=1)
    if mark: ax.plot(*Q, "o", mfc="white", mec=INK, ms=6, mew=1.1, zorder=5)

def panel(ax, k, notation, result, number):
    L = 1.55
    ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(plt.Rectangle((-L, -L), 2 * L, 2 * L, fc="#fbfaf7", ec="#d8d4cc", lw=.8, zorder=0))
    ax.text(-L + .1, L + .58, str(k), fontsize=14, ha="center", va="center", color="white", fontweight="bold",
            bbox=dict(boxstyle="circle,pad=0.28", fc=INK, ec=INK), transform=ax.transData, clip_on=False)
    ax.text(-L + .45, L + .58, notation, fontsize=16, ha="left", va="center", clip_on=False)
    ax.text(-L, L + .18, result, fontsize=13, ha="left", va="center", color="#555", clip_on=False)
    ax.text(L, L + .18, number, fontsize=13, ha="right", va="center", color="#555", clip_on=False)
    return L - .05

def figure(path_base):
    fig, axs = plt.subplots(3, 3, figsize=(9.6, 11.6))
    axs = axs.ravel()
    fig.subplots_adjust(left=.02, right=.98, top=.93, bottom=.01, wspace=.1, hspace=.3)

    # 1  (P->P, P'->P')
    ax = axs[0]; lim = panel(ax, 1, r"$(P\to P,\ P'\to P')$", "line through two points", "1 fold")
    P, Q = np.array([-.8, -.45]), np.array([.75, .5])
    a, b = line_pd(P, Q - P); fold(ax, a, b, lim); pt(ax, P, r"$P$", (-2, 11)); pt(ax, Q, r"$P'$", (-2, 11))

    # 2  (P->P')
    ax = axs[1]; lim = panel(ax, 2, r"$(P\to P')$", "perpendicular bisector", "1 fold")
    P, Q = np.array([-.85, -.3]), np.array([.8, .45])
    n, d = bisector(P, Q); fold(ax, n, d, lim); move(ax, P, n, d, mark=False)
    pt(ax, P, r"$P$", (-8, -8)); pt(ax, Q, r"$P'$", (9, 7))

    # 3  (P->P, D->D)
    ax = axs[2]; lim = panel(ax, 3, r"$(P\to P,\ D\to D)$", "perpendicular to a line", "1 or 2 folds")
    D = line_pd((0, -.55), (1, .25)); P = np.array([.25, .75])
    n, d = line_pd(P, D[0]); given(ax, D, lim, r"$D$", -1.15, (0, 9)); fold(ax, n, d, lim); pt(ax, P, r"$P$", (15, 4))
    # right-angle mark
    u = unit((1, .25)); foot = P - (D[0] @ P - D[1]) * D[0]; s = .13
    ax.plot(*np.array([foot + s * u, foot + s * u + s * D[0], foot + s * D[0]]).T, color=INK, lw=.8)

    # 4  (P->D, D'->D')
    ax = axs[3]; lim = panel(ax, 4, r"$(P\to D,\ D'\to D')$", r"$P$ onto $D$, crease $\perp D'$", "0 or 1 fold")
    D = line_pd((.55, 0), (.35, 1)); D2 = line_pd((0, -.8), (1, .12)); P = np.array([-.95, .35])
    u2 = unit((1, .12)); s = (D[1] - D[0] @ P) / (D[0] @ u2); Pstar = P + s * u2
    n, d = bisector(P, Pstar)
    given(ax, D, lim, r"$D$", -1.0, (11, 0)); given(ax, D2, lim, r"$D'$", -1.1, (0, 9))
    fold(ax, n, d, lim); move(ax, P, n, d); pt(ax, P, r"$P$", (-3, 10))
    f = n * d + ((D2[1] - D2[0] @ (n * d)) / (D2[0] @ np.array([-n[1], n[0]]))) * np.array([-n[1], n[0]])
    w = np.array([-n[1], n[0]]); w = w if w[1] > 0 else -w; s = .13
    ax.plot(*np.array([f + s * u2, f + s * u2 + s * w, f + s * w]).T, color=INK, lw=.8)

    # 5  (D->D')
    ax = axs[4]; lim = panel(ax, 5, r"$(D\to D')$", "angle bisectors", "1 or 2 folds")
    u, v = unit((1, .2)), unit((.45, 1)); O = np.array([-.2, -.25])
    D, D2 = line_pd(O, u), line_pd(O, v)
    given(ax, D, lim, r"$D$", 1.1, (0, -9)); given(ax, D2, lim, r"$D'$", 1.2, (-10, 0))
    for k, w in enumerate((u + v, u - v)):
        n, d = line_pd(O, w); fold(ax, n, d, lim, main=(k == 0))

    # 6  (P->D, P'->P')
    ax = axs[5]; lim = panel(ax, 6, r"$(P\to D,\ P'\to P')$", "quadratic equation", "0, 1 or 2 folds")
    D = line_pd((0, -.75), (1, 0)); P = np.array([-.6, .75]); Q = np.array([.3, .1])
    r = np.hypot(*(P - Q)); h = abs(D[0] @ Q - D[1]); footQ = Q - (D[0] @ Q - D[1]) * D[0]
    given(ax, D, lim, r"$D$", -1.2, (0, 9))
    for k, sg in enumerate((-1, 1)):
        Pst = footQ + sg * np.sqrt(r * r - h * h) * np.array([1, 0])
        n, d = bisector(P, Pst); fold(ax, n, d, lim, main=(k == 0))
        if k == 0: move(ax, P, n, d)
        else: ax.plot(*Pst, "o", mfc="white", mec=GREY, ms=4, mew=.8, zorder=5)
    pt(ax, P, r"$P$", (-8, 7)); pt(ax, Q, r"$P'$", (12, -9))

    # 7  (P->D, P'->D')
    ax = axs[6]; lim = panel(ax, 7, r"$(P\to D,\ P'\to D')$", "cubic equation", "0, 1, 2 or 3 folds")
    D = line_pd((0, -.75), (1, 0)); D2 = line_pd((-.75, 0), (0, 1))
    P = np.array([.5, -.43]); Q = np.array([-.39, .5])
    sols = beloch(P, D, Q, D2); print("panel 7: folds found =", len(sols))
    given(ax, D, lim, r"$D$", 1.2, (0, 9)); given(ax, D2, lim, r"$D'$", -1.25, (-11, 0))
    sols.sort(key=lambda s: abs(s[0][0]))
    for k, (n, d) in enumerate(sols):
        fold(ax, n, d, lim, main=(k == 0))
        if k == 0: move(ax, P, n, d); move(ax, Q, n, d)
    pt(ax, P, r"$P$", (9, 5)); pt(ax, Q, r"$P'$", (10, 6))

    axs[8].axis("off")
    # legend panel
    ax = axs[7]; ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    y = .86
    ax.plot([.04, .22], [y, y], color=ACC, lw=1.7, ls=(0, (5, 3))); ax.text(.28, y, "the fold", va="center", fontsize=15)
    y -= .13
    ax.plot([.04, .22], [y, y], color=ACC, lw=1.2, ls=(0, (5, 3)), alpha=.55); ax.text(.28, y, "other solutions", va="center", fontsize=15)
    y -= .13
    ax.plot([.04, .22], [y, y], color=INK, lw=1.3); ax.text(.28, y, r"given line ($D$, for $droite$)", va="center", fontsize=15)
    y -= .13
    ax.plot([.13], [y], "o", color=INK, ms=6); ax.text(.28, y, r"given point $P$", va="center", fontsize=15)
    y -= .13
    ax.plot([.13], [y], "o", mfc="white", mec=INK, ms=6, mew=1.1); ax.text(.28, y, r"where $P$ lands", va="center", fontsize=15)
    ax.text(.04, .17, r"$X\to Y$:  the fold carries $X$ onto $Y$." "\n" r"$X\to X$:  the fold leaves $X$ on itself.",
            fontsize=14, va="center", color="#444", linespacing=1.6)

    for ext in ("svg", "png"):
        fig.savefig(f"{path_base}.{ext}", dpi=200, facecolor="white")
    plt.close(fig)

if __name__ == "__main__":
    import sys
    check_trisection()
    figure(sys.argv[1] if len(sys.argv) > 1 else "justin-seven-folds")
