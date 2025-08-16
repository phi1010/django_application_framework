import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import polars as pl
    import django
    from pathlib import Path
    import sys
    import os

    PROJECT_PATH = str(Path("./src/").resolve())
    print(f"{PROJECT_PATH=}")
    if PROJECT_PATH not in sys.path: sys.path.insert(0, PROJECT_PATH)
    print(f"{sys.path=}")

    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "True"

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    from django.conf import settings
    django.setup()


@app.cell
def _():
    settings.__dict__
    return


@app.cell
def _():
    from myapp.models import MyModel
    list(MyModel.objects.all())
    return (MyModel,)


@app.cell
def _(MyModel):
    df = pl.DataFrame(list(MyModel.objects.values()))
    df
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
