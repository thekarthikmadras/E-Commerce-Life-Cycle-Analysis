from pathlib import Path


def get_project_root() -> Path:
    """
    Return the root directory of the project.
    """
    return Path(__file__).resolve().parent.parent


def get_data_dir() -> Path:
    return get_project_root() / "data"


def get_raw_data_dir() -> Path:
    return get_data_dir() / "raw"


def get_processed_data_dir() -> Path:
    return get_data_dir() / "processed"


def get_reports_dir() -> Path:
    return get_project_root() / "reports"


def get_figures_dir() -> Path:
    figures_dir = get_reports_dir() / "figures"
    figures_dir.mkdir(
        parents=True,
        exist_ok=True
    )
    return figures_dir