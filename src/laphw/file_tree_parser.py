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


DISTRIBUTION = 0
BRAND = 1
MODEL = 2
FIX = 3
FILE_PATH_WITH_DIST_BRAND_MODEL = 4
FIXES_ROOT_FOLDER = get_fixes_folder()


@lru_cache(maxsize=1)
def get_all_documents() -> frozenset[Path]:
    absolut_paths = Path(FIXES_ROOT_FOLDER).rglob("*.md")
    relative_paths = {path.relative_to(FIXES_ROOT_FOLDER) for path in absolut_paths}

    return frozenset(relative_paths)


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


@dataclass(frozen=True, kw_only=True)
class FileTreeData:
    all_documents: frozenset[Path]
    all_common_documents: frozenset[Path]
    all_model_documents: frozenset[Path]


@dataclass(frozen=True, kw_only=True)
class FixMatch:
    name: str
    path: Path


def filter_data(
    documents: frozenset[Path],
    search_string: str,
    search_index: int,
    extract_index: int,
) -> frozenset[str]:
    results = []
    for document in documents:
        if search_string in document.parts[search_index]:
            results.append(document.parts[extract_index])

    return frozenset(results)


def get_name_and_path(
    documents: frozenset[Path],
    search_string: str,
    search_index: int,
    extract_index: int,
) -> frozenset[str]:
    results = []
    for document in documents:
        if search_string in document.parts[search_index]:
            results.append(document.parts[extract_index])

    return frozenset(results)


def get_file_tree_data(all_documents: frozenset[Path]) -> FileTreeData:
    all_model_documents = []
    all_common_documents = []
    for document in all_documents:
        if len(Path(document).parts) == FILE_PATH_WITH_DIST_BRAND_MODEL:
            all_model_documents.append(document)

        if "common" in str(document):
            all_common_documents.append(document)

    return FileTreeData(
        all_documents=all_documents,
        all_common_documents=frozenset(all_common_documents),
        all_model_documents=frozenset(all_model_documents),
    )


def get_all_distributions(all_documents: frozenset[Path]) -> frozenset[str]:
    distributions = []
    for document in all_documents:
        path_parts = Path(document).parts
        if "common" not in path_parts[DISTRIBUTION]:
            distributions.append(path_parts[DISTRIBUTION])

    return frozenset(distributions)


def get_all_brands(all_documents: frozenset[Path]) -> frozenset[str]:
    brands = []
    for document in all_documents:
        path_parts = Path(document).parts
        if len(path_parts) == FILE_PATH_WITH_DIST_BRAND_MODEL:
            if "common" not in path_parts[BRAND]:
                brands.append(path_parts[BRAND])

    return frozenset(brands)


def get_all_models(all_documents: frozenset[Path]) -> frozenset[str]:
    all_models = []
    for document in all_documents:
        path_parts = Path(document).parts
        if len(path_parts) == FILE_PATH_WITH_DIST_BRAND_MODEL:
            if "common" not in path_parts[MODEL]:
                all_models.append(path_parts[MODEL])

    return frozenset(all_models)


def get_all_fixes(all_documents: frozenset[Path]) -> frozenset[str]:
    fixes = []
    for document in all_documents:
        fixes.append(document.stem)

    return frozenset(fixes)


def get_models_by_distribution(
    distribution: str, file_tree_data: FileTreeData
) -> frozenset[str]:
    return filter_data(
        documents=file_tree_data.all_model_documents,
        search_string=distribution,
        search_index=DISTRIBUTION,
        extract_index=MODEL,
    )


def get_brands_by_distribution(
    distribution: str, file_tree_data: FileTreeData
) -> frozenset[str]:
    return filter_data(
        file_tree_data.all_model_documents, distribution, DISTRIBUTION, BRAND
    )


def get_fixes_by_distribution(
    distribution: str, file_tree_data: FileTreeData
) -> frozenset[FixMatch]:
    fixes = []

    for model_document in file_tree_data.all_documents:
        if distribution in model_document.parts[DISTRIBUTION]:
            fixes.append(FixMatch(name=model_document.stem, path=model_document))

    return frozenset(fixes)


def get_distributions_by_brand(
    brand: str, file_tree_data: FileTreeData
) -> frozenset[str]:
    return filter_data(
        documents=file_tree_data.all_model_documents,
        search_string=brand,
        search_index=BRAND,
        extract_index=DISTRIBUTION,
    )


def get_models_by_brand(brand: str, file_tree_data: FileTreeData) -> frozenset[str]:
    return filter_data(
        documents=file_tree_data.all_model_documents,
        search_string=brand,
        search_index=BRAND,
        extract_index=MODEL,
    )


def get_fixes_by_brand(brand: str, file_tree_data: FileTreeData) -> frozenset[FixMatch]:
    fixes = []

    for model_document in file_tree_data.all_documents:
        if brand in model_document.parts[BRAND]:
            fixes.append(FixMatch(name=model_document.stem, path=model_document))

    return frozenset(fixes)


def get_distributions_by_model(
    model: str, file_tree_data: FileTreeData
) -> frozenset[str]:
    return filter_data(
        documents=file_tree_data.all_model_documents,
        search_string=model,
        search_index=MODEL,
        extract_index=DISTRIBUTION,
    )


def get_brand_by_model(model: str, file_tree_data: FileTreeData) -> str:
    return list(
        filter_data(
            documents=file_tree_data.all_model_documents,
            search_string=model,
            search_index=MODEL,
            extract_index=BRAND,
        )
    )[0]  # TODO Check if this is safe, it should be only one brand per model


def get_fixes_by_model(model: str, file_tree_data: FileTreeData) -> frozenset[FixMatch]:
    fixes = []

    brand = get_brand_by_model(model, file_tree_data)

    for model_document in file_tree_data.all_documents:
        if brand in model_document.parts[BRAND]:
            if model in model_document.parts[MODEL]:
                fixes.append(FixMatch(name=model_document.stem, path=model_document))
            if "common" in model_document.parts[MODEL]:
                fixes.append(FixMatch(name=model_document.stem, path=model_document))

    return frozenset(fixes)


def clear_all_cache() -> None:
    get_all_documents.cache_clear()


if __name__ == "__main__":
    clear_all_cache()
    all_documents = get_all_documents()
    file_tree_data = get_file_tree_data(all_documents)
    pprint(get_all_documents())
    pprint(get_all_distributions(all_documents))
    pprint(get_file_tree_data(all_documents))
    pprint(get_models_by_distribution("ubuntu", file_tree_data))
    pprint(get_brands_by_distribution("ubuntu", file_tree_data))
    pprint(get_fixes_by_distribution("ubuntu", file_tree_data))
    pprint(get_distributions_by_brand("dell", file_tree_data))
    pprint(get_fixes_by_brand("dell", file_tree_data))
    pprint(get_fixes_by_model("xps-15-9500", file_tree_data))
