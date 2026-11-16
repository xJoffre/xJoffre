from pathlib import Path

from receipt import FONT, SIZES, THEMES, Receipt, encode, svg, wrapped

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "scripts" / "img"
ASSETS = ROOT / "assets"

HEADER = ["JOFFRE ORELLANA", "Ingeniero en Ciencias de la Computación", "Loja, Ecuador"]
PROJECTS = [("AURA", "publicada"), ("Defectos en llantas", "94,9 %"), ("El Mirador", "personal"), ("Jengat", "APK 1.0")]
STACK = {
    "IA": ["Python", "TensorFlow", "Keras", "OpenCV"],
    "Web": ["TypeScript", "JavaScript", "React", "Vite", "Tailwind"],
    "Backend": ["Java", "Spring", "PostgreSQL", "Docker", "Actions"],
    "Móvil": ["Expo", "Firebase", "Android"],
    "Juegos": ["Godot"],
}
THESIS = "Mi tesis: transfer learning sobre VGG16. Acierta 242 de 255 llantas de prueba y encuentra 126 de las 130 defectuosas."
PANELS = [("gc-original.jpg", "original"), ("gc-buena.jpg", "clase buena"), ("gc-defectuosa.jpg", "clase defectuosa")]
PANEL_RATIO = 241 / 427


def profile(colors):
    ticket = Receipt(colors)
    ticket.center(HEADER[0], SIZES["title"], 700, 30)
    ticket.center(HEADER[1], SIZES["small"])
    ticket.center(HEADER[2], SIZES["small"], gap=30)
    ticket.rule()
    ticket.pair("PROYECTOS", size=SIZES["small"], weight=700)
    for name, detail in PROJECTS:
        ticket.pair(name, detail)
    ticket.rule()
    ticket.pair("STACK", "CANT.", SIZES["small"], 700)
    for area, tools in STACK.items():
        ticket.pair(area, str(len(tools)))
        ticket.note(", ".join(tools))
    ticket.rule()
    ticket.pair("TOTAL", f"{sum(len(tools) for tools in STACK.values())} tecnologías", SIZES["total"], 700)
    ticket.rule()
    ticket.center("Gracias por tu visita", SIZES["small"], gap=18)
    ticket.barcode("xJoffre")
    ticket.center("github.com/xJoffre", SIZES["caption"], gap=30)
    label = f"Recibo de {HEADER[0].title()}: " + ", ".join(f"{name} ({detail})" for name, detail in PROJECTS)
    return ticket.render(label)


def thesis(colors, height=220, gap=16):
    width = height * PANEL_RATIO
    body = ""
    for i, (file, label) in enumerate(PANELS):
        x = i * (width + gap)
        body += (f'<image href="data:image/jpeg;base64,{encode(IMAGES / file)}" x="{x:.1f}" y="10" '
                 f'width="{width:.1f}" height="{height}" preserveAspectRatio="xMidYMid slice"/>'
                 f'<text x="{x:.1f}" y="{height + 32}" style="{FONT};font-size:{SIZES["caption"]}px" fill="{colors["muted"]}">{label}</text>')
    body += f'<text style="{FONT};font-size:{SIZES["thesis"]}px" fill="{colors["text"]}">{wrapped(560, 60, THESIS, 38, 30)}</text>'
    return svg(1000, height + 42, THESIS, body)


ASSETS.mkdir(exist_ok=True)
for theme, colors in THEMES.items():
    (ASSETS / f"banner-{theme}.svg").write_text(profile(colors), encoding="utf-8", newline="\n")
    (ASSETS / f"thesis-{theme}.svg").write_text(thesis(colors), encoding="utf-8", newline="\n")
