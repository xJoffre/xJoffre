import base64
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
ASSETS = ROOT / "assets"

FONT = "font-family:'Libre Franklin','Helvetica Neue',Arial,sans-serif"
SIZES = {"title": 62, "subtitle": 21, "wall": 18, "placard_title": 24, "placard_medium": 15, "placard_text": 16, "placard_meta": 13,
         "label_title": 18, "label_medium": 13, "label_text": 13, "material": 15}
THEMES = {
    "light": {"ink": "#222222", "soft": "#6B6B6B", "card": "#FFFFFF", "edge": "#DADADA", "title": "#151515", "medium": "#555555",
              "text": "#222222", "meta": "#777777", "frame": "#151515", "mat": "#FFFFFF"},
    "dark": {"ink": "#E6EDF3", "soft": "#9198A1", "card": "#161B22", "edge": "#30363D", "title": "#F0F6FC", "medium": "#9198A1",
             "text": "#C9D1D9", "meta": "#8B949E", "frame": "#C9D1D9", "mat": "#161B22"},
}

NAME = "Joffre Orellana"
PERIOD = "Obras, 2025–2026"
WALL_TEXT = ("Hola, soy Joffre. Me gradué de Ingeniería en Ciencias de la Computación en la UNL, en Loja. "
             "Hago apps web y móviles, y en mi tesis entrené un modelo que encuentra llantas defectuosas.")
PROJECTS = [
    {"slug": "aura", "name": "AURA", "year": "2026", "medium": "React Native, Expo, Firebase y Cloud Functions",
     "text": "Una app de citas que hice para el emprendimiento de un cliente. Está en Google Play.", "collection": "Colección Google Play"},
    {"slug": "pic", "name": "Defectos en llantas", "year": "2025–2026", "medium": "Python, TensorFlow, Keras y OpenCV",
     "text": "Mi tesis: un modelo que separa llantas buenas de defectuosas. Acierta el 94,9 % en prueba.", "collection": "Tesis de grado, Universidad Nacional de Loja"},
    {"slug": "el-mirador", "name": "El Mirador", "year": "2026", "medium": "Java 25, Spring Boot, PostgreSQL y React",
     "text": "Un sistema de pedidos para un bar-restaurante. La cocina ve cada pedido en vivo.", "collection": "Colección personal"},
    {"slug": "jengat", "name": "Jengat", "year": "2026", "medium": "Godot 4.6 y GDScript",
     "text": "Un juego de fiesta en 3D para Android, con una torre de bloques y física real.", "collection": "Colección personal"},
]
THESIS = {"title": "Qué mira el modelo", "year": "2025–2026", "medium": "Grad-CAM sobre VGG16",
          "text": "Acierta 242 de 255 llantas de prueba y encuentra 126 de las 130 defectuosas."}
PANELS = ["gc-original.jpg", "gc-buena.jpg", "gc-defectuosa.jpg"]
PANEL_RATIO = 241 / 427
MATERIALS = [("python", "Python"), ("tensorflow", "TensorFlow"), ("keras", "Keras"), ("opencv", "OpenCV"), ("typescript", "TypeScript"),
             ("javascript", "JavaScript"), ("react", "React"), ("vite", "Vite"), ("tailwindcss", "Tailwind"), ("openjdk", "Java"),
             ("springboot", "Spring"), ("postgresql", "PostgreSQL"), ("docker", "Docker"), ("githubactions", "Actions"), ("expo", "Expo"),
             ("firebase", "Firebase"), ("android", "Android"), ("godotengine", "Godot")]


def encode(path):
    return base64.b64encode(path.read_bytes()).decode()


FONT_FACES = {
    "normal": "@font-face{font-family:'Libre Franklin';font-weight:400 700;"
              f"src:url(data:font/woff2;base64,{encode(SCRIPTS / 'fonts' / 'libre-franklin.woff2')}) format('woff2')}}",
    "italic": "@font-face{font-family:'Libre Franklin';font-style:italic;font-weight:400 700;"
              f"src:url(data:font/woff2;base64,{encode(SCRIPTS / 'fonts' / 'libre-franklin-italic.woff2')}) format('woff2')}}",
}
ICON_PATHS = {path.stem: re.search(r' d="([^"]+)"', path.read_text(encoding="utf-8")).group(1) for path in (SCRIPTS / "icons").glob("*.svg")}


def icon(slug, cx, cy, size, color):
    return (f'<path d="{ICON_PATHS[slug]}" fill="{color}" '
            f'transform="translate({cx - size / 2:.1f} {cy - size / 2:.1f}) scale({size / 24:.3f})"/>')


def wrapped(x, y, text, width, leading):
    return "".join(f'<tspan x="{x}" y="{y + i * leading}">{row}</tspan>' for i, row in enumerate(textwrap.wrap(text, width)))


def svg(width, height, label, body):
    faces = FONT_FACES["normal"] + (FONT_FACES["italic"] if "font-style:italic" in body else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
            f'role="img" aria-label="{label}"><style>{faces}</style>{body}</svg>')


def wall(colors):
    body = (f'<text x="0" y="78" style="{FONT};font-size:{SIZES["title"]}px;font-weight:600;letter-spacing:-1px" fill="{colors["ink"]}">{NAME}</text>'
            f'<text x="2" y="116" style="{FONT};font-size:{SIZES["subtitle"]}px" fill="{colors["soft"]}">{PERIOD}</text>'
            f'<line x1="2" y1="146" x2="60" y2="146" stroke="{colors["ink"]}" stroke-width="2"/>'
            f'<text style="{FONT};font-size:{SIZES["wall"]}px" fill="{colors["ink"]}">{wrapped(2, 186, WALL_TEXT, 82, 28)}</text>')
    return svg(1000, 260, f"{NAME}. {PERIOD}. {WALL_TEXT}", body)


def placard(colors, project):
    body = (f'<rect x="1" y="1" width="498" height="218" fill="{colors["card"]}" stroke="{colors["edge"]}"/>'
            f'<text x="28" y="50" style="{FONT};font-size:{SIZES["placard_title"]}px" fill="{colors["title"]}"><tspan font-weight="700">{project["name"]}</tspan>, {project["year"]}</text>'
            f'<text x="28" y="78" style="{FONT};font-size:{SIZES["placard_medium"]}px;font-style:italic" fill="{colors["medium"]}">{project["medium"]}</text>'
            f'<text style="{FONT};font-size:{SIZES["placard_text"]}px" fill="{colors["text"]}">{wrapped(28, 112, project["text"], 50, 23)}</text>'
            f'<text x="28" y="196" style="{FONT};font-size:{SIZES["placard_meta"]}px" fill="{colors["meta"]}">{project["collection"]}</text>')
    return svg(500, 220, f'{project["name"]}, {project["year"]}. {project["medium"]}. {project["text"]} {project["collection"]}.', body)


def framed_thesis(colors, height=200, gap=12):
    width = height * PANEL_RATIO
    frame_width = 3 * width + 2 * gap + 80
    body = f'<rect x="2" y="2" width="{frame_width:.0f}" height="{height + 76}" fill="{colors["mat"]}" stroke="{colors["frame"]}" stroke-width="5"/>'
    body += "".join(f'<image href="data:image/jpeg;base64,{encode(SCRIPTS / "img" / file)}" x="{40 + i * (width + gap):.1f}" y="40" '
                    f'width="{width:.1f}" height="{height}" preserveAspectRatio="xMidYMid slice"/>' for i, file in enumerate(PANELS))
    x = frame_width + 40
    body += (f'<rect x="{x:.0f}" y="110" width="340" height="150" fill="{colors["card"]}" stroke="{colors["edge"]}"/>'
             f'<text x="{x + 22:.0f}" y="146" style="{FONT};font-size:{SIZES["label_title"]}px" fill="{colors["title"]}"><tspan font-weight="700">{THESIS["title"]}</tspan>, {THESIS["year"]}</text>'
             f'<text x="{x + 22:.0f}" y="168" style="{FONT};font-size:{SIZES["label_medium"]}px;font-style:italic" fill="{colors["medium"]}">{THESIS["medium"]}</text>'
             f'<text style="{FONT};font-size:{SIZES["label_text"]}px" fill="{colors["text"]}">{wrapped(x + 22, 194, THESIS["text"], 38, 18)}</text>')
    return svg(1000, height + 82, f'{THESIS["title"]}, {THESIS["year"]}. {THESIS["medium"]}. {THESIS["text"]}', body)


def materials(colors, per_row=9):
    body = ""
    for i, (slug, name) in enumerate(MATERIALS):
        row, col = divmod(i, per_row)
        x, y = 40 + col * 110, 36 + row * 100
        body += (icon(slug, x, y, 30, colors["ink"])
                 + f'<text x="{x}" y="{y + 44}" text-anchor="middle" style="{FONT};font-size:{SIZES["material"]}px" fill="{colors["soft"]}">{name}</text>')
    rows = -(-len(MATERIALS) // per_row)
    return svg(1000, rows * 100 - 4, "Materiales: " + ", ".join(name for _slug, name in MATERIALS), body)


def write(name, content):
    (ASSETS / name).write_text(content, encoding="utf-8", newline="\n")


ASSETS.mkdir(exist_ok=True)
for theme, colors in THEMES.items():
    write(f"banner-{theme}.svg", wall(colors))
    write(f"thesis-{theme}.svg", framed_thesis(colors))
    write(f"stack-{theme}.svg", materials(colors))
    for project in PROJECTS:
        write(f"{project['slug']}-{theme}.svg", placard(colors, project))
