import air
from fastapi import FastAPI

app = air.Air()
api = FastAPI()

@app.page
def index():
    return air.layouts.mvpcss(
        air.Title("Feldroy SVGs"),
        air.H1("The Feldroy logo and other SVGs"),
        air.P("This page contains the Feldroy logo in SVG format, along with other related SVGs."),
    )


if __name__ == "__main__":
    print("Run this with fastapi dev")
