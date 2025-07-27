from pprint import pprint

import typer
from rich.console import Console

from . import file_tree_parser

ALL_DOCUMENTS = file_tree_parser.get_all_documents()
FILE_TREE_DATA = file_tree_parser.get_file_tree_data(all_documents=ALL_DOCUMENTS)

available_distributions = ", ".join(
    file_tree_parser.get_all_distributions(all_documents=ALL_DOCUMENTS)
)
available_brands = ", ".join(file_tree_parser.get_all_brands(ALL_DOCUMENTS))
available_models = ", ".join(file_tree_parser.get_all_models(ALL_DOCUMENTS))
available_fixes = ", ".join(file_tree_parser.get_all_fixes(ALL_DOCUMENTS))

app = typer.Typer(help="A CLI tool for accessing Linux laptop hardware fixes")
console = Console()


@app.command()  # type: ignore[misc]
def main(
    distribution: str | None = typer.Option(
        None, "--dist", "-d", help=f"Available distributions: {available_distributions}"
    ),
    brand: str | None = typer.Option(
        None, "--brand", "-b", help=f"Available brands: {available_brands}"
    ),
    model: str | None = typer.Option(
        None, "--model", "-m", help=f"Available models: {available_models}"
    ),
    hardware: str | None = typer.Option(
        None,
        "--hardware",
        "-hw",
        help=f"Available hardware fixes: {available_fixes}",
    ),
) -> None:
    if not any([distribution, brand, model, hardware]):
        typer.echo("Please specify at least one filter: --dist, --brand, or --model")
        raise typer.Exit(1)

    if distribution:
        fixes = file_tree_parser.get_fixes_by_distribution(distribution, FILE_TREE_DATA)
        pprint(fixes)
    # if brand:
    #     fixes = get_brand_model_distribution(brand, set(fixes))
    # if model:
    #     fixes = get_brand_model_distribution(model, set(fixes))
    # if hardware:
    #     """ Implement a filter for hardware"""
    #


if __name__ == "__main__":
    app()
