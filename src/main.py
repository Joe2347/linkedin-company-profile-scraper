thonimport argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from extractors.linkedin_parser import LinkedinCompanyParser
from utils.data_cleaner import normalize_company_data

def setup_logging(level: str = "INFO") -> None:
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )

def load_settings(settings_path: Path) -> Dict[str, Any]:
    if not settings_path.exists():
        logging.warning(
            "Settings file %s not found. Using in-code defaults.",
            settings_path.as_posix(),
        )
        return {}

    try:
        with settings_path.open("r", encoding="utf-8") as f:
            settings = json.load(f)
            if not isinstance(settings, dict):
                logging.warning(
                    "Settings file %s is not a JSON object. Ignoring.",
                    settings_path.as_posix(),
                )
                return {}
            return settings
    except json.JSONDecodeError as e:
        logging.error("Failed to parse settings file %s: %s", settings_path, e)
        return {}
    except OSError as e:
        logging.error("Failed to read settings file %s: %s", settings_path, e)
        return {}

def read_input_urls(input_path: Path) -> List[str]:
    if not input_path.exists():
        logging.error("Input URL file %s not found.", input_path.as_posix())
        return []

    urls: List[str] = []
    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            urls.append(line)

    if not urls:
        logging.warning("No URLs found in %s.", input_path.as_posix())
    else:
        logging.info("Loaded %d URL(s) from %s.", len(urls), input_path.as_posix())
    return urls

def write_output(output_path: Path, data: List[Dict[str, Any]]) -> None:
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logging.info("Wrote scraped data for %d company(ies) to %s.", len(data), output_path.as_posix())
    except OSError as e:
        logging.error("Failed to write output file %s: %s", output_path.as_posix(), e)

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="LinkedIn Company Profile Scraper - Public company data extractor."
    )
    parser.add_argument(
        "--input-file",
        default="data/input_urls.txt",
        help="Path to text file containing LinkedIn company URLs (one per line).",
    )
    parser.add_argument(
        "--output-file",
        default="data/sample_output.json",
        help="Path to JSON file where output will be stored.",
    )
    parser.add_argument(
        "--settings-file",
        default="src/config/settings.example.json",
        help="Path to JSON settings file.",
    )
    return parser.parse_args(argv)

def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)

    project_root = Path(__file__).resolve().parents[1]

    settings_path = (project_root / args.settings_file).resolve()
    input_path = (project_root / args.input_file).resolve()
    output_path = (project_root / args.output_file).resolve()

    settings = load_settings(settings_path)
    log_level = settings.get("logging", {}).get("level", "INFO")
    setup_logging(log_level)

    urls = read_input_urls(input_path)
    if not urls:
        logging.error("No URLs to process. Exiting.")
        return

    parser = LinkedinCompanyParser(settings=settings)
    results: List[Dict[str, Any]] = []

    for idx, url in enumerate(urls, start=1):
        logging.info("Processing %d/%d: %s", idx, len(urls), url)
        try:
            raw_data = parser.parse_company_profile(url)
            if not raw_data:
                logging.warning("No data extracted for URL: %s", url)
                continue
            cleaned = normalize_company_data(raw_data)
            results.append(cleaned)
        except Exception as e:  # Catch-all to avoid breaking the loop
            logging.exception("Unexpected error while processing %s: %s", url, e)

    if results:
        write_output(output_path, results)
    else:
        logging.warning("No company data was successfully scraped.")

if __name__ == "__main__":
    main(sys.argv[1:])