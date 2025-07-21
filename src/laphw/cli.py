from pathlib import Path
from pprint import pprint

import typer
from rich.console import Console

from .file_tree_parser import get_brand_model_distribution, get_fixes_documents

app = typer.Typer(help="A CLI tool for accessing Linux laptop hardware fixes")
console = Console()
all_fixes = get_fixes_documents().fix_file_paths


@app.command()  # type: ignore[misc]
def main(
    distribution: str | None = typer.Option(
        None, "--dist", "-d", help="Distribution: arch, opensuse, ubuntu"
    ),
    brand: str | None = typer.Option(
        None, "--brand", "-b", help="Brand (dell, lenovo, framework, hp)"
    ),
    model: str | None = typer.Option(
        None, "--model", "-m", help="Model (xps-13-9370, framework13, thinkpad-x1)"
    ),
    hardware: str | None = typer.Option(
        None,
        "--hardware",
        "-hw",
        help="Hardware (audio, bluetooth, suspend, graphics, wifi, power, touchpad, fingerprint)",
    ),
) -> None:
    if not any([distribution, brand, model, hardware]):
        typer.echo("Please specify at least one filter: --dist, --brand, or --model")
        raise typer.Exit(1)

    fixes: set[Path] = set(all_fixes)
    if distribution:
        fixes = get_brand_model_distribution(distribution, set(all_fixes))
    if brand:
        fixes = get_brand_model_distribution(brand, set(fixes))
    if model:
        fixes = get_brand_model_distribution(model, set(fixes))
    if hardware:
        """ Implement a filter for hardware"""

    pprint(fixes)


if __name__ == "__main__":
    app()
