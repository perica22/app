from pathlib import Path


def get_version() -> str:
    version_file = Path(__file__).parents[1] / "VERSION"
    return (
        Path(version_file).read_text().strip()
        if Path(version_file).exists()
        else "0.0.1+local.build"
    )


__version__ = get_version()
