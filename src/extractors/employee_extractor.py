thonfrom typing import Dict, List
from urllib.parse import urljoin

from bs4 import BeautifulSoup

class EmployeeExtractor:
    """
    Best-effort extraction of a few public employees from a company page.

    Since LinkedIn markup is complex and frequently changing, this class uses
    generic HTML heuristics:
    - Look for links to /in/<profile> under sections related to employees/people.
    - Infer the employee's position from nearby text.
    """

    @staticmethod
    def extract_employees_from_soup(
        soup: BeautifulSoup,
        base_url: str = "https://www.linkedin.com",
        max_employees: int = 4,
    ) -> List[Dict[str, str]]:
        employees: List[Dict[str, str]] = []

        # Narrow down to containers mentioning "Employees" or "People"
        candidate_sections = []
        for section in soup.find_all(["section", "div"]):
            heading = section.find(["h2", "h3", "h4"], string=True)
            if not heading:
                continue
            heading_txt = heading.get_text(" ", strip=True).lower()
            if any(keyword in heading_txt for keyword in ("employees", "people", "team")):
                candidate_sections.append(section)

        # If none were found, fall back to the whole soup
        if not candidate_sections:
            candidate_sections = [soup]

        seen_urls = set()

        for container in candidate_sections:
            for a in container.find_all("a", href=True):
                href = a["href"]
                if "/in/" not in href:
                    continue

                full_url = urljoin(base_url, href)
                if full_url in seen_urls:
                    continue

                name = a.get_text(" ", strip=True)
                if not name:
                    continue

                # Position / role often around the link in parent or sibling nodes
                position = EmployeeExtractor._infer_position(a)

                employees.append(
                    {
                        "employee_name": name,
                        "employee_position": position or "",
                        "employee_profile_url": full_url,
                    }
                )
                seen_urls.add(full_url)

                if len(employees) >= max_employees:
                    return employees

        return employees

    @staticmethod
    def _infer_position(link_tag) -> str:
        # Look at sibling spans or divs for position text
        for sibling in link_tag.parent.find_all(["span", "div"], recursive=False):
            if sibling is link_tag:
                continue
            txt = sibling.get_text(" ", strip=True)
            if txt and 5 < len(txt) < 120:
                return txt

        # If not found, look slightly higher up
        parent = link_tag.parent
        if parent and parent.parent:
            for el in parent.parent.find_all(["span", "div"], recursive=False):
                txt = el.get_text(" ", strip=True)
                if txt and 5 < len(txt) < 120:
                    return txt

        return ""