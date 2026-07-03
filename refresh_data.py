import logging
from pathlib import Path

from permit_service import load_permit_dataset
from permit_snapshot import save_permit_snapshot


DEFAULT_START_DATE = "2025-01-01"
DEFAULT_PAGE_SIZE = 500
DEFAULT_MAX_PAGES = 2
DEFAULT_OUTPUT_DIRECTORY = Path("data/processed")


def refresh_permit_snapshot(
    start_date: str = DEFAULT_START_DATE,
    page_size: int = DEFAULT_PAGE_SIZE,
    max_pages: int | None = DEFAULT_MAX_PAGES,
    output_directory: str | Path = DEFAULT_OUTPUT_DIRECTORY,
) -> tuple[Path, Path]:
    logging.info("Starting permit snapshot refresh")
    df = load_permit_dataset(
        start_date=start_date,
        page_size=page_size,
        max_pages=max_pages,
        )
    logging.info("Loaded %s permit rows", len(df))
    snapshot_path, metadata_path = save_permit_snapshot(
        df,
        output_directory=output_directory,
        source_start_date=start_date,
        )
    
    logging.info("Saved snapshot to %s", snapshot_path)
    logging.info("Saved metadata to %s", metadata_path)
    return snapshot_path, metadata_path


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    refresh_permit_snapshot()