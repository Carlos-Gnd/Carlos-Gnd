"""Genera las tarjetas SVG (tema cyber) del README del perfil Carlos-Gnd."""
import os
import sys
from html import escape

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

SANS = "'Inter','Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace"
BLUE, CYAN, PURPLE, GREEN, AMBER, GRAY = "#4f9cf9", "#22d3ee", "#a78bfa", "#4ade80", "#fbbf24", "#94a3b8"

STATUS = {
    "activo": ("ACTIVO", GREEN),
    "entregado": ("ENTREGADO", CYAN),
    "pausado": ("EN PAUSA", AMBER),
    "congelado": ("CONGELADO", GRAY),
    "propuesta": ("PROPUESTA", PURPLE),
}


def frame(w, h, body, uid):
    """Marco con halo de color y panel negro, igual que los widgets de GitSkins."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<defs>
  <radialGradient id="g1{uid}" cx="12%" cy="0%" r="55%"><stop offset="0" stop-color="#3b82f6" stop-opacity=".55"/><stop offset="1" stop-color="#3b82f6" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2{uid}" cx="78%" cy="0%" r="45%"><stop offset="0" stop-color="#22c55e" stop-opacity=".35"/><stop offset="1" stop-color="#22c55e" stop-opacity="0"/></radialGradient>
  <radialGradient id="g3{uid}" cx="60%" cy="100%" r="45%"><stop offset="0" stop-color="#a855f7" stop-opacity=".45"/><stop offset="1" stop-color="#a855f7" stop-opacity="0"/></radialGradient>
  <radialGradient id="g4{uid}" cx="100%" cy="80%" r="40%"><stop offset="0" stop-color="#14b8a6" stop-opacity=".45"/><stop offset="1" stop-color="#14b8a6" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{w}" height="{h}" rx="18" fill="#0b1020"/>
<rect width="{w}" height="{h}" rx="18" fill="url(#g1{uid})"/>
<rect width="{w}" height="{h}" rx="18" fill="url(#g2{uid})"/>
<rect width="{w}" height="{h}" rx="18" fill="url(#g3{uid})"/>
<rect width="{w}" height="{h}" rx="18" fill="url(#g4{uid})"/>
<rect x="12" y="12" width="{w-24}" height="{h-24}" rx="14" fill="#000" stroke="#4f9cf9" stroke-opacity=".45"/>
{body}
</svg>
"""


def text(x, y, s, size, fill="#e5e7eb", weight=400, font=SANS, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def chip_row(x, y, items, max_x):
    out, cx = [], x
    for t in items:
        w = int(len(t) * 6.6 + 18)
        if cx + w > max_x:
            break
        out.append(f'<rect x="{cx}" y="{y}" width="{w}" height="22" rx="11" fill="#0f172a" stroke="#4f9cf9" stroke-opacity=".5"/>')
        out.append(text(cx + w / 2, y + 15, t, 11, "#cbd5e1", 600, MONO, "middle"))
        cx += w + 7
    return "\n".join(out)


def project(slug, title, status, lines, meta, chips, private=False):
    w, h = 460, 250
    label, color = STATUS[status]
    pw = len(label) * 7.5 + 22
    body = [
        text(34, 46, f"~/proyectos/{slug}", 12, BLUE, 500, MONO),
        text(34 + len(f"~/proyectos/{slug}") * 7.3 + 10, 46, "· privado" if private else "", 12, GRAY, 500, MONO),
        f'<rect x="{w-34-pw}" y="31" width="{pw}" height="22" rx="11" fill="{color}" fill-opacity=".12" stroke="{color}" stroke-opacity=".7"/>',
        f'<circle cx="{w-34-pw+11}" cy="42" r="3.5" fill="{color}"/>',
        text(w - 34 - pw / 2 + 5, 46, label, 10.5, color, 700, MONO, "middle", 'letter-spacing="1"'),
        text(34, 86, title, 27, "#f8fafc", 800),
    ]
    for i, ln in enumerate(lines):
        body.append(text(34, 114 + i * 20, ln, 13.5, "#a8b3c7"))
    my = 114 + len(lines) * 20 + 8
    body.append(text(34, my, "▸ " + meta, 12, CYAN, 500, MONO))
    body.append(chip_row(34, h - 52, chips, w - 30))
    return frame(w, h, "\n".join(body), slug)


cards = {
    "ferred": project("ferred", "FERRED", "entregado",
        ["ERP/POS offline-first para ferretería multi-sucursal:",
         "inventario, ventas, facturación electrónica DTE y",
         "tienda online sobre el mismo backend (hexagonal)."],
        "Líder de desarrollo · 419 commits",
        ["Electron", "Express", "Prisma", "SQLite↔Supabase", "Stripe"]),
    "sia-u": project("sia-u", "SIA-U", "activo",
        ["Asistencia para las 6 facultades de la UNIVO: clases,",
         "prácticas y eventos con QR + GPS por edificio, sobre",
         "un solo motor (facultades = filas, no módulos)."],
        "Módulo académico · proyecto institucional",
        ["React", "TypeScript", "Supabase", "Edge Functions", "Playwright"], private=True),
    "check-health": project("check-health", "UNIVO Check-Health", "congelado",
        ["Asistencia en prácticas clínicas: geofencing GPS en",
         "el servidor, QR firmado con JWT, detección de GPS",
         "falso y audit trail inmutable. Evolucionó a SIA-U."],
        "325 commits · presentado en CONINFO 2026",
        ["React", "Supabase", "RLS", "Firebase FCM", "Vitest"], private=True),
    "pokecards": project("pokecards", "PokéCards Market", "entregado",
        ["E-commerce de cartas Pokémon TCG: marketplace con",
         "filtros, sobres, pagos con PayPal y colección.",
         "951 cartas en Supabase con caché de 5 min."],
        "Backend en VPS de Azure con Docker",
        ["React", "NestJS", "Prisma", "PayPal", "Azure"]),
    "smart-inventory": project("smart-inventory", "Smart Inventory ERP", "pausado",
        ["ERP retail/restaurante para pymes: inventario, POS,",
         "caja, compras y RRHH. Reescritura web de mi app",
         "de escritorio en C# WinForms + SQL Server."],
        "Monorepo pnpm + Turborepo · 27 modelos Prisma",
        ["NestJS", "Prisma", "PostgreSQL", "shadcn/ui", "Docker"], private=True),
    "anamnesis-xr": project("anamnesis-xr", "ANAMNESIS XR", "propuesta",
        ["Simulador de entrevista clínica en realidad virtual:",
         "el estudiante habla con un paciente 3D movido por",
         "IA 100% local, y otro agente lo evalúa con rúbrica."],
        "Objetivo: respuesta por voz en < 3 s, sin internet",
        ["WebXR", "faster-whisper", "LLM local", "Piper TTS", "FastAPI"]),
}

# Trayectoria: lo que aprendí en cada ciclo (fuente: vault de Obsidian)
steps = [
    ("CICLO I–II", "2024", ["HTML · CSS · JS", "Bash · Linux"], BLUE),
    ("CICLO III", "2025-I", ["POO en JS", "Express · MongoDB"], CYAN),
    ("CICLO IV", "2025-II", ["C# · SQL Server", "Python · Docker"], GREEN),
    ("CICLO V", "2026-I", ["React · NestJS", "Prisma · Electron"], PURPLE),
    ("CICLO VI", "ahora", ["Supabase · Astro", "Seguridad · Perf"], AMBER),
]
W, H = 920, 262
body = [text(36, 52, "Trayectoria", 26, "#f8fafc", 800),
        text(36, 76, "Cómo fue creciendo el stack, ciclo a ciclo · Ing. en Desarrollo de Software, UNIVO", 13, GRAY),
        text(W - 36, 52, "> git log --stack", 13, BLUE, 600, MONO, "end")]
x0, x1, ly = 90, W - 90, 120
body.append(f'<line x1="{x0}" y1="{ly}" x2="{x1}" y2="{ly}" stroke="#334155" stroke-width="2" stroke-dasharray="4 6"/>')
step = (x1 - x0) / (len(steps) - 1)
for i, (cyc, yr, items, c) in enumerate(steps):
    cx = x0 + i * step
    body.append(f'<circle cx="{cx}" cy="{ly}" r="9" fill="#000" stroke="{c}" stroke-width="3"/>')
    body.append(f'<circle cx="{cx}" cy="{ly}" r="3.5" fill="{c}"/>')
    body.append(text(cx, ly + 34, cyc, 12, c, 700, MONO, "middle", 'letter-spacing="1"'))
    body.append(text(cx, ly + 52, yr, 11, GRAY, 500, MONO, "middle"))
    for j, it in enumerate(items):
        body.append(text(cx, ly + 76 + j * 18, it, 12.5, "#cbd5e1", 500, SANS, "middle"))
cards["trayectoria"] = frame(W, H, "\n".join(body), "tl")

# Ahora mismo: plan de mejora (24 semanas) + lo que estoy construyendo
W, H = 920, 260
body = [text(36, 52, "Ahora mismo", 26, "#f8fafc", 800),
        text(36, 76, "Oct 2026 – Mar 2027 · entender a fondo lo que construyo", 13, GRAY),
        text(W - 36, 52, "> cat now.md", 13, BLUE, 600, MONO, "end")]
cols = [
    ("// construyendo", CYAN, ["SIA-U: módulo académico", "ANAMNESIS XR: prueba de concepto", "  (ciclo de voz con IA local)"]),
    ("// estudiando", PURPLE, ["Event loop, closures y promesas", "HTTP y auth sin framework", "SQL a mano: índices y EXPLAIN"]),
    ("// siguiente", GREEN, ["Testing + CI en FERRED", "Sync offline e idempotencia", "Auditoría OWASP"]),
]
for i, (h, c, items) in enumerate(cols):
    cx = 36 + i * 290
    body.append(f'<rect x="{cx}" y="98" width="270" height="124" rx="12" fill="#05080f" stroke="{c}" stroke-opacity=".45"/>')
    body.append(text(cx + 18, 126, h, 13, c, 700, MONO))
    for j, it in enumerate(items):
        bullet = "" if it.startswith("  ") else "› "
        body.append(text(cx + 18, 154 + j * 22, bullet + it.strip(), 13, "#cbd5e1"))
cards["ahora"] = frame(W, H, "\n".join(body), "now")

for name, svg in cards.items():
    with open(os.path.join(OUT, f"{name}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
print("ok", list(cards))
