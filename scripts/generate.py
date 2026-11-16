import base64
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
ASSETS = ROOT / "assets"

HAND = "font-family:'Shadows Into Light','Segoe Print',cursive"
PRINT = "font-family:'Libre Franklin','Helvetica Neue',Arial,sans-serif"
SIZES = {"name": 44, "message": 26, "address": 28, "card_title": 34, "card_text": 22, "thesis": 22, "label": 20,
         "stamp_name": 13, "stamp_area": 10, "stamp_caption": 12, "postmark": 13, "postmark_year": 16}
THEMES = {
    "light": {"paper": "#FDFDFB", "edge": "#DDDDD6", "line": "#D8D8D2", "ink": "#24324A", "ink_soft": "#3A4660", "text": "#222222", "muted": "#6B6B6B",
              "postmark": "#3A3A3A", "stamp_border": "#FFFFFF", "mini_stamp": "#EEF2F6", "sheet": "#FFFFFF", "sheet_ink": "#24324A",
              "tints": {"IA": "#FCEFD9", "Web": "#E3EEFF", "Backend": "#FDE3E6", "Móvil": "#E2F5EA", "Juegos": "#EEE6FB"}},
    "dark": {"paper": "#1C2128", "edge": "#30363D", "line": "#30363D", "ink": "#D2DCEB", "ink_soft": "#AEB9C9", "text": "#E6EDF3", "muted": "#9198A1",
             "postmark": "#8B949E", "stamp_border": "#E6EDF3", "mini_stamp": "#2A313B", "sheet": "#22272E", "sheet_ink": "#E6EDF3",
             "tints": {"IA": "#3A2F1E", "Web": "#1E2A3D", "Backend": "#3A1F24", "Móvil": "#1E3328", "Juegos": "#2C2440"}},
}
LANDSCAPE = {"sky": "#DCEBF5", "hill": "#3E7A5B", "hill_dark": "#2C5D44", "sun": "#F2C14E", "caption": "#1F3A5F", "town": "#FFFFFF"}

NAME = "Joffre Orellana"
MESSAGE = ("Hola, soy Joffre. Me gradué de Ingeniería en Ciencias de la Computación en la UNL, en Loja. Hago apps web y móviles, "
           "y en mi tesis entrené un modelo que encuentra llantas defectuosas. Abajo te dejo lo que he hecho. Un saludo, Joffre.")
ADDRESS = ["Para: tu equipo", "Asunto: hola", "De: Loja, Ecuador"]
POSTMARK = "LOJA   NOV 2026   UNL"
PROJECTS = [
    {"slug": "aura", "name": "AURA", "icon": "expo", "summary": "Una app de citas que hice para el emprendimiento de un cliente. Está en Google Play."},
    {"slug": "pic", "name": "Defectos en llantas", "icon": "tensorflow", "summary": "Mi tesis: un modelo que separa llantas buenas de defectuosas. Acierta el 94,9 % en prueba."},
    {"slug": "el-mirador", "name": "El Mirador", "icon": "springboot", "summary": "Un sistema de pedidos para un bar-restaurante. La cocina ve cada pedido en vivo."},
    {"slug": "jengat", "name": "Jengat", "icon": "godotengine", "summary": "Un juego de fiesta en 3D para Android, con una torre de bloques y física real."},
]
THESIS = "Mi tesis: transfer learning sobre VGG16. Acierta 242 de 255 llantas de prueba y encuentra 126 de las 130 defectuosas."
PANELS = [("gc-original.jpg", "original"), ("gc-buena.jpg", "clase buena"), ("gc-defectuosa.jpg", "clase defectuosa")]
PANEL_RATIO = 241 / 427
STACK = {
    "IA": [("python", "Python"), ("tensorflow", "TensorFlow"), ("keras", "Keras"), ("opencv", "OpenCV")],
    "Web": [("typescript", "TypeScript"), ("javascript", "JavaScript"), ("react", "React"), ("vite", "Vite"), ("tailwindcss", "Tailwind")],
    "Backend": [("openjdk", "Java"), ("springboot", "Spring"), ("postgresql", "PostgreSQL"), ("docker", "Docker"), ("githubactions", "Actions")],
    "Móvil": [("expo", "Expo"), ("firebase", "Firebase"), ("android", "Android")],
    "Juegos": [("godotengine", "Godot")],
}


def encode(path):
    return base64.b64encode(path.read_bytes()).decode()


FONT_FACES = {
    HAND: "@font-face{font-family:'Shadows Into Light';"
          f"src:url(data:font/woff2;base64,{encode(SCRIPTS / 'fonts' / 'shadows-into-light.woff2')}) format('woff2')}}",
    PRINT: "@font-face{font-family:'Libre Franklin';font-weight:400 700;"
           f"src:url(data:font/woff2;base64,{encode(SCRIPTS / 'fonts' / 'libre-franklin.woff2')}) format('woff2')}}",
}
ICON_PATHS = {path.stem: re.search(r' d="([^"]+)"', path.read_text(encoding="utf-8")).group(1) for path in (SCRIPTS / "icons").glob("*.svg")}


LIFT = '<defs><filter id="lift" x="-5%" y="-5%" width="110%" height="110%"><feDropShadow dx="0" dy="1" stdDeviation="1.2" flood-opacity=".22"/></filter></defs>'


def icon(slug, cx, cy, size, color):
    return (f'<path d="{ICON_PATHS[slug]}" fill="{color}" '
            f'transform="translate({cx - size / 2:.1f} {cy - size / 2:.1f}) scale({size / 24:.3f})"/>')


def wrapped(x, y, text, width, leading):
    return "".join(f'<tspan x="{x}" y="{y + i * leading}">{row}</tspan>' for i, row in enumerate(textwrap.wrap(text, width)))


def svg(width, height, label, body):
    faces = "".join(face for family, face in FONT_FACES.items() if family in body)
    if "url(#lift)" in body:
        body = LIFT + body
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
            f'role="img" aria-label="{label}"><style>{faces}</style>{body}</svg>')


def perforated(x, y, width, height, mask_id, fill, inner):
    holes = "".join(f'<circle cx="{x + i * 12}" cy="{y}" r="4"/><circle cx="{x + i * 12}" cy="{y + height}" r="4"/>' for i in range(int(width // 12) + 1))
    holes += "".join(f'<circle cx="{x}" cy="{y + i * 12}" r="4"/><circle cx="{x + width}" cy="{y + i * 12}" r="4"/>' for i in range(int(height // 12) + 1))
    return (f'<mask id="{mask_id}"><rect x="{x - 6}" y="{y - 6}" width="{width + 12}" height="{height + 12}" fill="#FFFFFF"/><g fill="#000000">{holes}</g></mask>'
            f'<g filter="url(#lift)"><g mask="url(#{mask_id})"><rect x="{x - 4}" y="{y - 4}" width="{width + 8}" height="{height + 8}" fill="{fill}"/>{inner}</g></g>')


def postcard(colors):
    land = LANDSCAPE
    art = (f'<rect x="792" y="48" width="132" height="152" fill="{land["sky"]}"/>'
           f'<polygon points="792,170 830,110 862,150 890,100 924,160 924,200 792,200" fill="{land["hill"]}"/>'
           f'<polygon points="792,185 845,140 900,180 924,170 924,200 792,200" fill="{land["hill_dark"]}"/><circle cx="900" cy="80" r="14" fill="{land["sun"]}"/>'
           f'<text x="800" y="70" style="{PRINT};font-size:{SIZES["stamp_caption"]}px;font-weight:700" fill="{land["caption"]}">ECUADOR</text>'
           f'<text x="916" y="194" text-anchor="end" style="{PRINT};font-size:{SIZES["stamp_caption"]}px;font-weight:700" fill="{land["town"]}">Loja</text>')
    mark = colors["postmark"]
    waves = "".join(f'<path d="M 770 {100 + i * 16} q 20 -8 40 0 t 40 0 t 40 0 t 40 0" fill="none" stroke="{mark}" stroke-width="2.2"/>' for i in range(4))
    postmark = (f'<g opacity="0"><animate attributeName="opacity" from="0" to=".85" begin=".6s" dur=".15s" fill="freeze"/>'
                f'<circle cx="702" cy="128" r="62" fill="none" stroke="{mark}" stroke-width="3"/><circle cx="702" cy="128" r="44" fill="none" stroke="{mark}" stroke-width="2"/>'
                f'<text style="{PRINT};font-size:{SIZES["postmark"]}px;font-weight:700;letter-spacing:3px" fill="{mark}" xml:space="preserve"><textPath href="#ring" startOffset="2%">{POSTMARK}</textPath></text>'
                f'<text x="702" y="134" text-anchor="middle" style="{PRINT};font-size:{SIZES["postmark_year"]}px;font-weight:700" fill="{mark}">2026</text>{waves}</g>')
    lines = "".join(f'<line x1="560" y1="{y}" x2="950" y2="{y}" stroke="{colors["line"]}" stroke-width="1.5"/>' for y in (330, 380, 430))
    address = "".join(f'<text x="566" y="{322 + i * 50}" style="{HAND};font-size:{SIZES["address"]}px" fill="{colors["ink"]}">{row}</text>' for i, row in enumerate(ADDRESS))
    body = (f'<defs><path id="ring" d="M 640 128 a 62 62 0 1 1 124 0 a 62 62 0 1 1 -124 0"/></defs>'
            f'<rect x="1" y="1" width="998" height="498" rx="6" fill="{colors["paper"]}" stroke="{colors["edge"]}"/>'
            f'<line x1="520" y1="40" x2="520" y2="460" stroke="{colors["line"]}" stroke-width="2"/>'
            f'<text x="40" y="74" style="{HAND};font-size:{SIZES["name"]}px" fill="{colors["ink"]}">{NAME}</text>'
            f'<text style="{HAND};font-size:{SIZES["message"]}px" fill="{colors["ink"]}">{wrapped(42, 132, MESSAGE, 38, 38)}</text>'
            f'{perforated(786, 42, 144, 164, "stamp", colors["stamp_border"], art)}{postmark}{lines}{address}')
    return svg(1000, 500, MESSAGE, body)


def project_card(colors, project):
    stamp = perforated(406, 22, 66, 76, "stamp", colors["sheet"],
                       f'<rect x="410" y="26" width="58" height="68" fill="{colors["mini_stamp"]}"/>{icon(project["icon"], 439, 60, 30, colors["ink"])}')
    body = (f'<rect x="1" y="1" width="498" height="198" rx="6" fill="{colors["paper"]}" stroke="{colors["edge"]}"/>{stamp}'
            f'<text x="28" y="58" style="{HAND};font-size:{SIZES["card_title"]}px" fill="{colors["ink"]}">{project["name"]}</text>'
            f'<text style="{HAND};font-size:{SIZES["card_text"]}px" fill="{colors["ink_soft"]}">{wrapped(30, 100, project["summary"], 38, 28)}</text>')
    return svg(500, 200, f'{project["name"]}: {project["summary"]}', body)


def thesis(colors, height=220, gap=16):
    width = height * PANEL_RATIO
    body = ""
    for i, (file, label) in enumerate(PANELS):
        x = i * (width + gap)
        body += (f'<image href="data:image/jpeg;base64,{encode(SCRIPTS / "img" / file)}" x="{x:.1f}" y="10" '
                 f'width="{width:.1f}" height="{height}" preserveAspectRatio="xMidYMid slice"/>'
                 f'<text x="{x:.1f}" y="{height + 32}" style="{HAND};font-size:{SIZES["label"]}px" fill="{colors["muted"]}">{label}</text>')
    body += f'<text style="{HAND};font-size:{SIZES["thesis"]}px" fill="{colors["text"]}">{wrapped(560, 60, THESIS, 36, 34)}</text>'
    return svg(1000, height + 42, THESIS, body)


def stamp_sheet(colors, per_row=6):
    body, index = "", 0
    for area, items in STACK.items():
        for slug, name in items:
            row, col = divmod(index, per_row)
            x, y = 20 + col * 162, 20 + row * 176
            inner = (f'<rect x="{x + 10}" y="{y + 10}" width="120" height="136" fill="{colors["tints"][area]}"/>{icon(slug, x + 70, y + 66, 46, colors["sheet_ink"])}'
                     f'<text x="{x + 70}" y="{y + 128}" text-anchor="middle" style="{PRINT};font-size:{SIZES["stamp_name"]}px;font-weight:600" fill="{colors["sheet_ink"]}">{name}</text>'
                     f'<text x="{x + 18}" y="{y + 26}" style="{PRINT};font-size:{SIZES["stamp_area"]}px;font-weight:700" fill="{colors["sheet_ink"]}" opacity=".6">{area}</text>')
            body += perforated(x + 4, y + 4, 132, 148, f"stamp{index}", colors["sheet"], inner)
            index += 1
    rows = -(-index // per_row)
    label = "Stack: " + "; ".join(f"{area}: " + ", ".join(name for _slug, name in items) for area, items in STACK.items())
    return svg(1000, 20 + rows * 176, label, body)


def write(name, content):
    (ASSETS / name).write_text(content, encoding="utf-8", newline="\n")


ASSETS.mkdir(exist_ok=True)
for theme, colors in THEMES.items():
    write(f"banner-{theme}.svg", postcard(colors))
    write(f"thesis-{theme}.svg", thesis(colors))
    write(f"stack-{theme}.svg", stamp_sheet(colors))
    for project in PROJECTS:
        write(f"{project['slug']}-{theme}.svg", project_card(colors, project))
