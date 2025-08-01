import air
from air_markdown import Markdown
from fastapi import HTTPException
from fastapi import FastAPI
from pathlib import Path

app = air.Air()
api = FastAPI()

app.mount("/static", air.StaticFiles(directory="static"), name="static")


def nav():
    return air.Nav(
        air.A("Home", href="/"),
        air.A("Usage Policy", href="/usage-policy"),
    )


@app.page
def index():
    return air.layouts.mvpcss(
        nav(),
        air.Title("Feldroy SVGs"),
        air.H1("The Feldroy logo as SVG"),
        air.P("This page contains the Feldroy logo in SVG format."),
        
        air.Img(src="/static/feldroy-logo-square.svg", alt="Feldroy Logo", width=200, height=200),

        air.Div(
            air.A(
                "Download SVG",
                href="/static/feldroy-logo-square.svg",
                download=True,
            ),
        )
    )


def layout(request: air.Request, *content):
    if not isinstance(request, air.Request):
        raise Exception('First arg of layout needs to be an air.Request')
    return air.layouts.mvpcss(
        nav(),
        *content
    )


@app.get('/{slug:path}')
def mdpage(request: air.Request, slug: str):
    path = Path(f"pages/{slug}.md")
    if path.exists():
        text = path.read_text()
        # TODO add fetching of page title from first H1 tag
        return layout(
            request, Markdown(text)
        )
    path = Path(f"pages/{slug}.py")
    if path.exists():
        module_name = f'pages.{slug.replace('/', '.')}'     
        mod = importlib.import_module(module_name)
        return layout(
            request, mod.render(request)
        )
    raise HTTPException(status_code=404)


if __name__ == "__main__":
    print("Run this with fastapi dev")
