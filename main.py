import os
from pathlib import Path
from typing import Annotated

import typer
from pdf2image import convert_from_path

app = typer.Typer()


# Define project directories
PROJ_DIR = Path(__file__).parent.resolve()
BUILD_DIR = Path(os.getenv("BUILD_DIR", PROJ_DIR / "build")).resolve()
FIGURES_DIR = Path(os.getenv("FIGURES_DIR", PROJ_DIR / "figures")).resolve()


# Commands


@app.command("genfig")
def generate_cv_figure(
    output_dir: Annotated[
        Path, typer.Argument(..., help="Output directory for the generated figure")
    ] = FIGURES_DIR,
    build_dir: Annotated[
        Path, typer.Argument(..., help="Build directory containing CV data")
    ] = BUILD_DIR,
):
    """
    Generate a figure for the CV based on data in the build directory.
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = build_dir / "cv.pdf"
    png_path = output_dir / "cv.png"

    if not pdf_path.exists():
        typer.echo(f"PDF file not found: {pdf_path}")
        raise typer.Exit(code=1)

    images = convert_from_path(str(pdf_path))
    if images:
        images[0].save(png_path, "PNG")
        typer.echo(f"Generated figure saved to: {png_path}")
    else:
        typer.echo("No images were generated from the PDF.")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
