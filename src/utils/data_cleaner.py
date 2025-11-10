thonimport logging
import re
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

WHITESPACE_RE = re.compile(r"\s+")

def clean_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    value = WHITESPACE_RE.sub(" ", value)
    return value or None

def parse_int_from_text(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    digits = re.findall(r"[\d,]+", value)
    if not digits:
        return None
    try:
        return int(digits[0].replace(",", ""))
    except ValueError:
        return None

def normalize_company_data(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize raw scraped data into a clean, consistent structure.
    """
    data: Dict[str, Any] = {}

    data["company_name"] = clean_text(raw.get("company_name"))
    data["universal_name_id"] = extract_universal_name_id(raw.get("source_url"))
    data["background_cover_image_url"] = clean_text(raw.get("background_cover_image_url"))
    data["linkedin_internal_id"] = clean_text(raw.get("linkedin_internal_id"))
    data["industry"] = clean_text(raw.get("industry"))
    data["location"] = clean_text(raw.get("location")) or clean_text(raw.get("headquarters"))
    data["follower_count"] = parse_int_from_text(
        raw.get("follower_count") or raw.get("followers")
    )
    data["tagline"] = clean_text(raw.get("tagline"))
    data["company_size_on_linkedin"] = clean_text(raw.get("company_size_on_linkedin"))
    data["about"] = clean_text(raw.get("about"))
    data["website"] = clean_text(raw.get("website"))
    data["company_size"] = clean_text(raw.get("company_size"))
    data["headquarters"] = clean_text(raw.get("headquarters"))
    data["type"] = clean_text(raw.get("type"))
    data["founded"] = clean_text(raw.get("founded"))
    data["specialties"] = clean_text(raw.get("specialties"))

    locations = raw.get("locations")
    if isinstance(locations, list):
        clean_locations = []
        for loc in locations:
            if not isinstance(loc, dict):
                continue
            addr = clean_text(loc.get("address"))
            map_url = clean_text(loc.get("map_url"))
            if not addr and not map_url:
                continue
            clean_locations.append(
                {
                    "address": addr,
                    "map_url": map_url,
                }
            )
        if clean_locations:
            data["locations"] = clean_locations

    employees = raw.get("employees")
    if isinstance(employees, list):
        clean_employees = []
        for emp in employees:
            if not isinstance(emp, dict):
                continue
            name = clean_text(emp.get("employee_name"))
            if not name:
                continue
            clean_employees.append(
                {
                    "employee_name": name,
                    "employee_position": clean_text(emp.get("employee_position")),
                    "employee_profile_url": clean_text(emp.get("employee_profile_url")),
                }
            )
        if clean_employees:
            data["employees"] = clean_employees

    updates = raw.get("updates")
    if isinstance(updates, list):
        clean_updates = []
        for upd in updates:
            if not isinstance(upd, dict):
                continue
            text = clean_text(upd.get("text"))
            if not text:
                continue
            clean_updates.append(
                {
                    "text": text,
                    "articlePostedDate": clean_text(upd.get("articlePostedDate")),
                    "totalLikes": clean_text(upd.get("totalLikes")),
                }
            )
        if clean_updates:
            data["updates"] = clean_updates

    similar_companies = raw.get("similar_companies")
    if isinstance(similar_companies, list):
        clean_similar = []
        for comp in similar_companies:
            if isinstance(comp, dict):
                name = clean_text(comp.get("name") or comp.get("company_name"))
                url = clean_text(comp.get("url") or comp.get("profile_url"))
                if not name and not url:
                    continue
                clean_similar.append({"company_name": name, "profile_url": url})
            elif isinstance(comp, str):
                comp_name = clean_text(comp)
                if comp_name:
                    clean_similar.append({"company_name": comp_name, "profile_url": None})
        if clean_similar:
            data["similar_companies"] = clean_similar

    # Attach original URL at the end for traceability
    if raw.get("source_url"):
        data["source_url"] = clean_text(raw.get("source_url"))

    logger.debug("Normalized company data: %s", data)
    return data

def extract_universal_name_id(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    # Typical company profile format: https://www.linkedin.com/company/<slug>/
    match = re.search(r"/company/([^/?#]+)/?", url)
    if not match:
        return None
    return match.group(1)