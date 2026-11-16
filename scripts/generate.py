import base64
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
ASSETS = ROOT / "assets"

FAMILY = "font-family:'Hanken Grotesk','Segoe UI',Helvetica,Arial,sans-serif"
THEMES = {
    "light": {"text": "#1F2328", "muted": "#59636E", "accent": "#3B5BDB"},
    "dark": {"text": "#F0F6FC", "muted": "#9198A1", "accent": "#7C9CFF"},
}
SIZES = {"display": 124, "title": 48, "lead": 20, "body": 16, "label": 14, "caption": 12}

NAME = "Joffre Orellana"
INTRO = "Ingeniero en Ciencias de la Computación. Hago apps web y móviles, y modelos de visión por computadora."
PROJECTS = [
    {"slug": "aura", "name": "AURA", "status": "En Google Play", "summary": "App de citas para el emprendimiento de un cliente. Likes, tokens y compras se validan en el servidor."},
    {"slug": "pic", "name": "Defectos en llantas", "status": "Tesis", "summary": "Transfer learning sobre VGG16; acierta el 94,9 % de las llantas de prueba."},
    {"slug": "el-mirador", "name": "El Mirador", "status": "Proyecto personal", "summary": "Pedidos en línea para un bar-restaurante, con cocina en vivo y un panel para cada rol."},
    {"slug": "jengat", "name": "Jengat", "status": "Proyecto personal", "summary": "Juego de fiesta 3D para Android con física real."},
]
THESIS = "Mi tesis detecta llantas defectuosas con transfer learning sobre VGG16. Acierta 242 de 255 llantas de prueba y encuentra 126 de las 130 defectuosas."
PANELS = [("gc-original.jpg", "Original"), ("gc-buena.jpg", "Clase buena"), ("gc-defectuosa.jpg", "Clase defectuosa")]
PANEL_RATIO = 241 / 427


def encode(path):
    return base64.b64encode(path.read_bytes()).decode()


FONT_FACE = (
    "@font-face{font-family:'Hanken Grotesk';font-weight:100 900;"
    f"src:url(data:font/woff2;base64,{encode(SCRIPTS / 'fonts' / 'hanken-grotesk.woff2')}) format('woff2')}}"
)


def wrapped(x, y, text, width, leading):
    rows = textwrap.wrap(text, width)
    return "".join(f'<tspan x="{x}" y="{y + i * leading}">{row}</tspan>' for i, row in enumerate(rows))


def svg(width, height, label, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'role="img" aria-label="{label}"><style>{FONT_FACE}</style>{body}</svg>'
    )


def banner(colors):
    weights = ";".join(str(weight) for weight in range(100, 801, 100))
    body = (
        f'<text x="-4" y="112" style="{FAMILY};font-size:{SIZES["display"]}px;letter-spacing:-5px" font-weight="100" fill="{colors["text"]}">{NAME}'
        f'<animate attributeName="font-weight" values="{weights}" dur="1.4s" begin=".2s" calcMode="discrete" fill="freeze"/></text>'
        f'<text style="{FAMILY};font-size:{SIZES["lead"]}px" fill="{colors["muted"]}">{wrapped(2, 168, INTRO, 64, 30)}</text>'
    )
    return svg(1000, 230, f"{NAME}. {INTRO}", body)


def project_row(colors, project):
    body = (
        f'<text x="0" y="52" style="{FAMILY};font-size:{SIZES["title"]}px;font-weight:700;letter-spacing:-1.5px" fill="{colors["text"]}">{project["name"]}</text>'
        f'<text x="560" y="26" style="{FAMILY};font-size:{SIZES["label"]}px;font-weight:600" fill="{colors["accent"]}">{project["status"]}</text>'
        f'<text style="{FAMILY};font-size:{SIZES["body"]}px" fill="{colors["muted"]}">{wrapped(560, 52, project["summary"], 48, 23)}</text>'
    )
    return svg(1000, 104, f'{project["name"]}, {project["status"].lower()}: {project["summary"]}', body)


def thesis(colors, height=230, gap=14):
    width = height * PANEL_RATIO
    body = ""
    for i, (file, label) in enumerate(PANELS):
        x = i * (width + gap)
        body += (
            f'<image href="data:image/jpeg;base64,{encode(SCRIPTS / "img" / file)}" x="{x:.1f}" y="0" '
            f'width="{width:.1f}" height="{height}" preserveAspectRatio="xMidYMid slice"/>'
            f'<text x="{x:.1f}" y="{height + 22}" style="{FAMILY};font-size:{SIZES["caption"]}px" fill="{colors["muted"]}">{label}</text>'
        )
    body += f'<text style="{FAMILY};font-size:{SIZES["body"]}px" fill="{colors["text"]}">{wrapped(470, 20, THESIS, 48, 25)}</text>'
    return svg(1000, height + 32, THESIS, body)


def write(name, content):
    (ASSETS / name).write_text(content, encoding="utf-8", newline="\n")


ASSETS.mkdir(exist_ok=True)
for theme, colors in THEMES.items():
    write(f"banner-{theme}.svg", banner(colors))
    write(f"thesis-{theme}.svg", thesis(colors))
    for project in PROJECTS:
        write(f"{project['slug']}-{theme}.svg", project_row(colors, project))
