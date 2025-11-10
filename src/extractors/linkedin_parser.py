thonimport json
import logging
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from extractors.employee_extractor import EmployeeExtractor

logger = logging.getLogger(__name__)

class LinkedinCompanyParser:
    """
    Scrapes public LinkedIn company pages without authentication.

    Note: LinkedIn changes its markup frequently. This parser focuses on:
    - JSON-LD data (if present)
    - Common meta tags and visible text blocks
    """

    def __init__(self, settings: Optional[Dict[str, Any]] = None) -> None:
        self.settings = settings or {}
        http_settings = self.settings.get("http", {})
        self.timeout = http_settings.get("timeout_seconds", 15)
        self.max_retries = http_settings.get("max_retries", 2)
        self.sleep_between_retries = http_settings.get("sleep_between_retries_seconds", 2)

        headers = http_settings.get("headers") or {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

        self.session = requests.Session()
        self.session.headers.update(headers)

    def _fetch_html(self, url: str) -> Optional[str]:
        """Fetch HTML with basic retry logic."""
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.debug("Fetching URL (attempt %d/%d): %s", attempt, self.max_retries, url)
                resp = self.session.get(url, timeout=self.timeout)
                if resp.status_code >= 400:
                    logger.warning(
                        "Received HTTP %d from %s", resp.status_code, url
                    )
                    continue
                return resp.text
            except requests.RequestException as e:
                logger.warning("Request error while fetching %s: %s", url, e)
                if attempt < self.max_retries:
                    time.sleep(self.sleep_between_retries)
        logger.error("Failed to fetch URL after %d attempts: %s", self.max_retries, url)
        return None

    def parse_company_profile(self, url: str) -> Optional[Dict[str, Any]]:
        html = self._fetch_html(url)
        if not html:
            return None

        soup = BeautifulSoup(html, "lxml")

        company_data: Dict[str, Any] = {
            "source_url": url,
        }

        # JSON-LD (if present)
        json_ld_data = self._extract_json_ld(soup)
        if json_ld_data:
            company_data.update(json_ld_data)

        # Meta tags and visible sections
        company_data.update(self._extract_meta_based_fields(soup))
        company_data.update(self._extract_visible_sections(soup))

        # Employees from page (best-effort)
        employees = EmployeeExtractor.extract_employees_from_soup(
            soup, base_url="https://www.linkedin.com", max_employees=4
        )
        if employees:
            company_data["employees"] = employees

        # Updates / posts (best-effort scraping)
        updates = self._extract_updates(soup)
        if updates:
            company_data["updates"] = updates

        # Fallback for company_name if still missing
        if not company_data.get("company_name"):
            company_data["company_name"] = self._fallback_company_name(soup)

        return company_data

    # -------------------- JSON-LD --------------------

    def _extract_json_ld(self, soup: BeautifulSoup) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        scripts = soup.find_all("script", type="application/ld+json")
        for script in scripts:
            try:
                raw_text = script.string or script.get_text(strip=True)
                if not raw_text:
                    continue
                parsed = json.loads(raw_text)
            except json.JSONDecodeError:
                continue

            # JSON-LD may be a list or a dict
            if isinstance(parsed, list):
                items = parsed
            else:
                items = [parsed]

            for item in items:
                if not isinstance(item, dict):
                    continue
                if item.get("@type") in {"Organization", "Corporation"}:
                    name = item.get("name")
                    description = item.get("description")
                    url = item.get("url")

                    if name:
                        data.setdefault("company_name", name)
                    if description:
                        data.setdefault("about", description)
                    if url:
                        data.setdefault("website", url)
        return data

    # -------------------- Meta-based fields --------------------

    def _extract_meta_based_fields(self, soup: BeautifulSoup) -> Dict[str, Any]:
        data: Dict[str, Any] = {}

        # Title / tagline from <meta> and <title>
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            data["company_name"] = data.get("company_name") or og_title["content"]

        og_desc = soup.find("meta", property="og:description")
        if og_desc and og_desc.get("content"):
            data.setdefault("tagline", og_desc["content"])

        cover_img = soup.find("meta", property="og:image")
        if cover_img and cover_img.get("content"):
            data["background_cover_image_url"] = cover_img["content"]

        # Follower count is sometimes present in meta tags or visible text
        follower_meta = soup.find("meta", attrs={"name": "followersCount"})
        if follower_meta and follower_meta.get("content"):
            data["follower_count"] = follower_meta["content"]

        # Industry may show up in meta tags
        industry_meta = soup.find("meta", attrs={"name": "industry"})
        if industry_meta and industry_meta.get("content"):
            data["industry"] = industry_meta["content"]

        return data

    # -------------------- Visible sections --------------------

    def _extract_visible_sections(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Best-effort scraping of visible sections like About, Headquarters, etc.
        LinkedIn often uses <dt>/<dd> pairs for company info.
        """
        data: Dict[str, Any] = {}

        # About section (look for a section with "About")
        about_text = self._extract_about_section(soup)
        if about_text:
            data.setdefault("about", about_text)

        # Definition lists with labels (e.g., Headquarters, Founded, Company size)
        for dl in soup.find_all("dl"):
            terms = dl.find_all("dt")
            defs = dl.find_all("dd")
            if len(terms) != len(defs) or not terms:
                continue
            for dt, dd in zip(terms, defs):
                label = (dt.get_text(" ", strip=True) or "").lower()
                value = dd.get_text(" ", strip=True) or ""
                if not label or not value:
                    continue

                if "headquarters" in label:
                    data["headquarters"] = value
                elif "founded" in label:
                    data["founded"] = value
                elif "company size" in label:
                    data["company_size"] = value
                elif "industry" in label and "industry" not in data:
                    data["industry"] = value
                elif "website" in label and "website" not in data:
                    # May contain a link
                    a = dd.find("a", href=True)
                    if a:
                        data["website"] = a["href"]
                    else:
                        data["website"] = value
                elif "type" in label:
                    data["type"] = value

        # Locations list - best-effort search for address blocks
        locations = self._extract_locations(soup)
        if locations:
            data["locations"] = locations

        return data

    def _extract_about_section(self, soup: BeautifulSoup) -> Optional[str]:
        # Look for headings containing "About"
        heading_candidates = soup.find_all(["h2", "h3"], string=True)
        for heading in heading_candidates:
            if "about" in heading.get_text(" ", strip=True).lower():
                # About text is often the next sibling or within a nearby div
                parent = heading.parent
                if not parent:
                    continue
                # Look for paragraphs or spans following the heading
                text_chunks: List[str] = []
                for p in parent.find_all(["p", "span"], recursive=True):
                    txt = p.get_text(" ", strip=True)
                    if txt and len(txt) > 30:
                        text_chunks.append(txt)
                if text_chunks:
                    return " ".join(text_chunks)
        return None

    def _extract_locations(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        locations: List[Dict[str, Any]] = []
        # This is intentionally generic: search for elements that look like addresses
        address_blocks = soup.find_all("address")
        for addr in address_blocks:
            text = addr.get_text(" ", strip=True)
            if not text:
                continue
            loc: Dict[str, Any] = {"address": text}
            link = addr.find("a", href=True)
            if link:
                loc["map_url"] = link["href"]
            locations.append(loc)

        # If no <address> tags, heuristically look for elements mentioning "Directions" or "Get directions"
        if not locations:
            for a in soup.find_all("a", href=True):
                label = a.get_text(" ", strip=True).lower()
                if "directions" in label:
                    loc: Dict[str, Any] = {
                        "address": a.get("aria-label", a.get_text(" ", strip=True)),
                        "map_url": a["href"],
                    }
                    locations.append(loc)

        return locations

    # -------------------- Updates / posts --------------------

    def _extract_updates(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Try to scrape recent updates/posts.

        This is highly heuristic: look for post containers that include text,
        relative timestamps (e.g. '1w', '2mo') and engagement counts.
        """
        updates: List[Dict[str, Any]] = []

        # Common pattern: <div> or <article> for feed items.
        candidates = soup.find_all(["article", "div"], attrs={"data-urn": True})
        for container in candidates:
            text_el = container.find(["p", "span"], string=True)
            if not text_el:
                continue
            text = text_el.get_text(" ", strip=True)
            if not text or len(text) < 20:
                continue

            update: Dict[str, Any] = {"text": text}

            # Find something that looks like a relative timestamp (e.g. '1w', '3mo')
            time_el = container.find("span", string=True)
            if time_el:
                ts = time_el.get_text(" ", strip=True)
                if ts and any(ch.isdigit() for ch in ts):
                    update["articlePostedDate"] = ts

            # Simple like count heuristics: numbers followed by 'like' / 'likes'
            for span in container.find_all("span", string=True):
                s_txt = span.get_text(" ", strip=True).lower()
                if "like" in s_txt and any(ch.isdigit() for ch in s_txt):
                    update["totalLikes"] = span.get_text(" ", strip=True)
                    break

            updates.append(update)
            if len(updates) >= 5:
                break

        return updates

    # -------------------- Fallbacks --------------------

    def _fallback_company_name(self, soup: BeautifulSoup) -> Optional[str]:
        if soup.title and soup.title.string:
            title_text = soup.title.string.strip()
            # LinkedIn titles often end with "| LinkedIn"
            parts = title_text.split("|")
            return parts[0].strip() if parts else title_text
        return None