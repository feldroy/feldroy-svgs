import air
from fastapi import FastAPI

app = air.Air()
api = FastAPI()

app.mount("/static", air.StaticFiles(directory="static"), name="static")

@app.page
def index():
    return air.layouts.mvpcss(
        air.Title("Feldroy SVGs"),
        air.H1("The Feldroy logo as SVG"),
        air.P("This page contains the Feldroy logo in SVG format."),
        air.Img(src="/static/feldroy-logo-square.svg", alt="Feldroy Logo", width=200, height=200),
    )


if __name__ == "__main__":
    print("Run this with fastapi dev")
