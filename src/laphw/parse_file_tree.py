from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set

Filename = str


def get_fixes_folder() -> Path:
    fixes_folder_path = Path.home() / ".cache" / "laphw" / "fixes"
    Path(fixes_folder_path).mkdir(parents=True, exist_ok=True)

    return fixes_folder_path


FIXES_ROOT_FOLDER = get_fixes_folder()


@dataclass(frozen=True)
class MetaData:
    distributions: Set[str]
    brands: Set[str]
    models: Set[str]
    tags: List[str]
    difficulty: str
    tested_by: Set[str]


@dataclass(frozen=True)
class FixedDistributions:
    distributions: Set[str]
    distribution_paths: List[Path]


@dataclass(frozen=True)
class FixedBrands:
    brand_names: Set[str]
    brand_paths: List[Path]


@dataclass(frozen=True)
class FixedModels:
    model_names: Set[str]
    model_paths: List[Path]


@dataclass(frozen=True)
class Fixes:
    fix_file_names: Set[str]
    fix_file_paths: List[Path]


@dataclass(frozen=True)
class FixedModelsByDistribution:
    distribution: str
    devices: Dict[str, Path]


@dataclass(frozen=True)
class FixesForModels:
    device: str
    device_path: Path
    fixes: List[Filename]


def check_dir(path: Path) -> None:
    if not path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")


def check_file(path: Path) -> None:
    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")


def get_sub_dir_names(parent: Path) -> List[str]:
    check_dir(parent)
    return [dir.name for dir in parent.iterdir() if dir.is_dir()]


def get_sub_dir_paths(parent: Path) -> List[Path]:
    check_dir(parent)
    return [dir for dir in parent.iterdir() if dir.is_dir()]


def get_file_names(path: Path) -> List[str]:
    check_file(path)
    return [file.name for file in path.iterdir() if file.is_file()]


def get_file_paths(path: Path) -> List[Path]:
    check_file(path)
    return [file for file in path.iterdir() if file.is_file()]


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


def get_brand_from_path() -> List[Path]:
    lenovo_fixes = []
    models = get_models()
    for model in models.model_paths:
        if "lenovo" in str(model):
            lenovo_fixes.append(model)
    return lenovo_fixes


if __name__ == "__main__":
    # print(get_distributions())
    # print(get_brands())
    # print(get_models())
    # print(get_fixes())
    fixes = get_fixes()
    print(len(fixes.fix_file_paths))
    # print(get_brand_from_path())
