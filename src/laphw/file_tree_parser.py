from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from pprint import pprint
from typing import Any

import frontmatter


def get_fixes_folder() -> Path:
    fixes_folder_path = Path.home() / ".cache" / "laphw" / "fixes"
    Path(fixes_folder_path).mkdir(parents=True, exist_ok=True)

    return fixes_folder_path


FIXES_ROOT_FOLDER = get_fixes_folder()


@dataclass(frozen=True, kw_only=True)
class Distribution:
    """Support by each distribution"""

    distribution_name: str
    distribution_path: Path
    common_path: Path
    supported_brands: frozenset[str]
    supported_models: frozenset[str]
    fixes: frozenset[str]


@dataclass(frozen=True, kw_only=True)
class Brand:
    """Support by each brand"""

    brand_name: str
    brand_paths: frozenset[Path]
    common_paths: frozenset[Path]
    supported_distributions: frozenset[str]
    supported_models: frozenset[str]
    fixes: frozenset[str]


@dataclass(frozen=True, kw_only=True)
class Model:
    """Support by each model"""

    model_name: str
    model_path_documents: frozenset[Path]
    common_path_documents: frozenset[Path]
    brand: str
    distribution_names: frozenset[str]


@dataclass(frozen=True, kw_only=True)
class Fix:
    """Each fix document mapped with dist, model and brand"""

    file_name: str
    file_path: Path
    distribution: str  # Ubuntu, arch etc
    brand: str  # Dell, Framework etc
    model: str  # xps-13-9370, framework-laptop-13 etc
    hw: str  # audio, bluetooth etc


@dataclass(frozen=True, kw_only=True)
class Laphw:
    """Folder structure representation"""

    distributions: frozenset[Distribution]
    brands: frozenset[Brand]
    models: frozenset[Model]
    fixes: frozenset[Fix]


def create_datastructure() -> frozenset[Distribution]:  # should return Laphw
    distributions_data = get_distributions()
    # brands_data = get_brands(distributions_data)

    return distributions_data


def check_dir(path: Path) -> None:
    if not path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")


def get_sub_dir_names(parent: Path) -> list[str]:
    check_dir(parent)
    return [
        dir.name for dir in parent.iterdir() if dir.is_dir() if "common" not in dir.name
    ]


def get_sub_dir_paths(parent: Path) -> list[Path]:
    check_dir(parent)
    return [dir for dir in parent.iterdir() if dir.is_dir()]


def get_supported_distributions() -> list[str]:
    distribution_paths = [dist for dist in FIXES_ROOT_FOLDER.iterdir() if dist.is_dir()]
    return [path.name for path in distribution_paths if path.name != "common"]


@lru_cache(maxsize=1)
def get_distributions() -> frozenset[Distribution]:
    distributions = get_supported_distributions()
    distribution_data = []
    for distribution in distributions:
        supported_brands = []
        brand_paths = []
        supported_models = []
        distribution_path = FIXES_ROOT_FOLDER / distribution
        common_path = distribution_path / "common"
        supported_brands.extend(get_sub_dir_names(distribution_path))
        brand_paths.extend(get_sub_dir_paths(distribution_path))

        for brand_path in brand_paths:
            supported_models.extend(get_sub_dir_names(brand_path))

        fix_file_paths = list(Path(distribution_path).rglob("*.md"))
        fix_file_stem = [hardware_fix.stem for hardware_fix in fix_file_paths]

        distribution_data.append(
            Distribution(
                distribution_name=distribution,
                distribution_path=distribution_path,
                common_path=common_path,
                supported_brands=frozenset(supported_brands),
                supported_models=frozenset(supported_models),
                fixes=frozenset(fix_file_stem),
            )
        )

    return frozenset(distribution_data)


def get_all_supported_brands(
    distribution_data: frozenset[Distribution],
) -> frozenset[str]:
    all_supported_brands: frozenset[str] = frozenset()
    for dist in distribution_data:
        all_supported_brands = all_supported_brands.union(dist.supported_brands)

    return all_supported_brands


def get_all_supported_distributions(
    distribution_data: frozenset[Distribution],
) -> frozenset[str]:
    all_supported_distributions: frozenset[str] = frozenset()

    for dist in distribution_data:
        all_supported_distributions = all_supported_distributions.union(
            dist.distribution_name
        )

    return all_supported_distributions


def get_all_supported_models(
    distribution_data: frozenset[Distribution],
) -> frozenset[str]:
    all_supported_models: frozenset[str] = frozenset()

    for dist in distribution_data:
        all_supported_models = all_supported_models.union(dist.supported_models)

    return all_supported_models


@lru_cache(maxsize=1)
def get_brands(distribution_data: frozenset[Distribution]) -> frozenset[Brand]:
    all_supported_brands = get_all_supported_brands(distribution_data)
    brand_data = []
    for brand in all_supported_brands:
        brand_paths = []
        common_paths = []
        supported_distributions = []
        supported_models = []
        fixes: list[str] = []
        for dist in distribution_data:
            distribution_path = FIXES_ROOT_FOLDER / dist.distribution_name
            if brand in dist.supported_brands:
                supported_distributions.append(dist.distribution_name)

            brand_paths.extend(get_sub_dir_paths(distribution_path))
            brand_paths.extend(
                [brand_path for brand_path in brand_paths if brand in brand_path.name]
            )

            for brand_path in brand_paths:
                common_paths.extend(get_sub_dir_paths(brand_path))
                supported_models.extend(get_sub_dir_names(brand_path))
            common_paths.extend(
                [
                    brand_path
                    for brand_path in common_paths
                    if "common" in brand_path.name
                ]
            )
            supported_models.extend(
                [brand_path for brand_path in supported_models if brand in brand_path]
            )

        brand_data.append(
            Brand(
                brand_name=brand,
                brand_paths=frozenset(brand_paths),
                common_paths=frozenset(common_paths),
                supported_distributions=frozenset(supported_distributions),
                supported_models=frozenset(supported_models),
                fixes=frozenset(fixes),
            )
        )

    return frozenset(brand_data)


#
# @lru_cache(maxsize=1)
# def get_models() -> model:
#     model_names = []
#     model_paths = []
#     fixed_brands = get_brands()
#     for brand_path in fixed_brands.brand_paths:
#         model_names.extend(get_sub_dir_names(brand_path))
#         model_paths.extend(get_sub_dir_paths(brand_path))
#
#     common_folder_paths = [
#         model_path for model_path in model_paths if "common" in model_path.name
#     ]
#
#     model_paths = [
#         model_path for model_path in model_paths if "common" not in model_path.name
#     ]
#
#     return model(
#         model_names=frozenset(model_names),
#         model_paths=frozenset(model_paths),
#         common_folder_paths=frozenset(common_folder_paths),
#     )
#
#
# def get_specific_model(model: str) -> models:
#     all_model_paths = get_models()
#     pprint(all_model_paths)
#     common_path_for_model = [
#         path for path in all_model_paths.common_folder_paths if model in path.name
#     ]
#     model_paths = [path for path in all_model_paths.model_paths if model in path.name]
#
#     return models(
#         model_names=frozenset([model]),
#         model_paths=frozenset(model_paths),
#         common_folder_paths=frozenset(common_path_for_model),
#     )
#
#
# def get_specific_brand(brand: str) -> brands:
#     all_brand_paths = get_brands()
#     common_path_for_model = [
#         path for path in all_brand_paths.common_folder_paths if brand in path.name
#     ]
#     brand_paths = [path for path in all_brand_paths.brand_paths if brand in path.name]
#
#     return brands(
#         brand_names=frozenset([brand]),
#         brand_paths=frozenset(brand_paths),
#         common_folder_paths=frozenset(common_path_for_model),
#     )
#
#
@lru_cache(maxsize=1)
def get_fixes_documents() -> Fix:
    # TODO Need major refactor
    fix_file_paths = list(Path(FIXES_ROOT_FOLDER).rglob("*.md"))
    #  fix_file_paths = list(path(fixes_root_folder).rglob("*.md"))
    # fix_file_names = [file_path.name for file_path in fix_file_paths]
    # fix_file_stem = [hardware_fix.stem for hardware_fix in fix_file_paths]

    return Fix(
        file_name="file_name",
        file_path=fix_file_paths[0],
        distribution="distribution",
        brand="Dell",
        model="framework-laptop-13",
        hw="audio",
    )


def parse_frontmatter(path: Path) -> dict[Any, Any]:
    with open(path, encoding="utf-8") as f:
        post = frontmatter.load(f)
        return post.metadata  # type: ignore[no-any-return]


def is_brand_model_distribution_in_frontmatter(
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


def get_brand_model_distribution(search_string: str, fixes: set[Path]) -> set[Path]:
    """Get all fixes for a brand, model or distributions"""
    found_fixes = []
    for path in fixes:
        if search_string in path.parts:
            found_fixes.append(path)
        if "common" in path.parts:
            if is_brand_model_distribution_in_frontmatter(
                parse_frontmatter(path), search_string
            ):
                found_fixes.append(path)

    return set(found_fixes)


def clear_all_cache() -> None:
    get_distributions.cache_clear()
    # get_brands.cache_clear()
    # get_models.cache_clear()
    # get_fixes_documents.cache_clear()


if __name__ == "__main__":
    clear_all_cache()
    # pprint(get_model_support_for_distr())
    test = create_datastructure()
    # pprint(test)
    # pprint(get_specific_brand("dell"))
    # pprint(get_distributions())

    pprint(get_brands(get_distributions()))
    # pprint(get_models())
    # pprint(get_brand_model_distribution("ubuntu"))
