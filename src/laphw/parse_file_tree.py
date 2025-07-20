from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from typing import Any

import frontmatter

Filename = str


def get_fixes_folder() -> Path:
    fixes_folder_path = Path.home() / ".cache" / "laphw" / "fixes"
    Path(fixes_folder_path).mkdir(parents=True, exist_ok=True)

    return fixes_folder_path


FIXES_ROOT_FOLDER = get_fixes_folder()


@dataclass(frozen=True, kw_only=True)
class MetaData:
    distributions: set[str]
    brands: set[str]
    models: set[str]
    tags: list[str]
    difficulty: str
    tested_by: set[str]


@dataclass(frozen=True, kw_only=True)
class FixedDistributions:
    distributions: set[str]
    distribution_paths: list[Path]


@dataclass(frozen=True, kw_only=True)
class FixedBrands:
    brand_names: set[str]
    brand_paths: list[Path]


@dataclass(frozen=True, kw_only=True)
class FixedModels:
    model_names: set[str]
    model_paths: list[Path]


@dataclass(frozen=True, kw_only=True)
class Fixes:
    fix_file_names: set[str]
    fix_file_paths: list[Path]


def check_dir(path: Path) -> None:
    if not path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")


def get_sub_dir_names(parent: Path) -> list[str]:
    check_dir(parent)
    return [dir.name for dir in parent.iterdir() if dir.is_dir()]


def get_sub_dir_paths(parent: Path) -> list[Path]:
    check_dir(parent)
    return [dir for dir in parent.iterdir() if dir.is_dir()]


def get_distributions() -> FixedDistributions:
    distribution_names = []
    distribution_paths = [dist for dist in FIXES_ROOT_FOLDER.iterdir() if dist.is_dir()]
    for distribution in distribution_paths:
        distribution_names.append(distribution.name)

    return FixedDistributions(
        distributions=set(distribution_names), distribution_paths=distribution_paths
    )


def get_brands() -> FixedBrands:
    brand_names = []
    brand_paths = []
    fixed_distributions = get_distributions()
    for distribution_path in fixed_distributions.distribution_paths:
        brand_names.extend(get_sub_dir_names(distribution_path))
        brand_paths.extend(get_sub_dir_paths(distribution_path))

    return FixedBrands(brand_names=set(brand_names), brand_paths=brand_paths)


def get_models() -> FixedModels:
    model_names = []
    model_paths = []
    fixed_brands = get_brands()
    for brand_path in fixed_brands.brand_paths:
        model_names.extend(get_sub_dir_names(brand_path))
        model_paths.extend(get_sub_dir_paths(brand_path))

    return FixedModels(model_names=set(model_names), model_paths=model_paths)


def get_fixes() -> Fixes:
    fix_file_paths = list(Path(FIXES_ROOT_FOLDER).rglob("*.md"))
    fix_file_names = [file_path.name for file_path in fix_file_paths]

    return Fixes(
        fix_file_names=set(fix_file_names), fix_file_paths=list(fix_file_paths)
    )


def parse_frontmatter(path: Path) -> dict[Any, Any]:
    with open(path, encoding="utf-8") as f:
        post = frontmatter.load(f)
        return post.metadata  # type: ignore[no-any-return]


def is_brand_model_distribution_in_dict(
    data: dict[str, Any], search_string: str
) -> bool:
    search_string = search_string.lower()

    # Check distributions (list)
    distributions = data.get("distributions", [])
    if any(search_string in dist.lower() for dist in distributions):
        return True

    # Check models (list or string)
    models = data.get("model", [])
    if isinstance(models, str):
        models = [models]
    if any(search_string in model.lower() for model in models):
        return True
    if any("all" in model.lower() for model in models):
        return True

    # Check brand (string)
    brand = data.get("brand", "")
    if search_string in brand.lower():
        return True
    if "generic" in brand.lower():
        return True

    return False


def get_brand_model_distribution(search_string: str) -> set[Path]:
    """Get all fixes for a brand, model or distributions"""
    found_fixes = []
    all_fixes = get_fixes()
    for path in all_fixes.fix_file_paths:
        if search_string in path.parts:
            found_fixes.append(path)
        if "common" in path.parts:
            if is_brand_model_distribution_in_dict(
                parse_frontmatter(path), search_string
            ):
                found_fixes.append(path)

    return set(found_fixes)


if __name__ == "__main__":
    # print(get_distributions())
    # print(get_brands())
    # print(get_models())
    # pprint(get_fixes())
    # fixes = get_fixes()
    # print(len(fixes.fix_file_paths))
    pprint(get_brand_model_distribution("lenovo"))
    # pprint(get_brand_model_distribution("thinkpad-x1-carbon-gen6"))
    # pprint(get_brand_model_distribution("ubuntu"))
