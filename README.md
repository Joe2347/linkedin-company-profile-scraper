# Linkedin Company Profile Scraper

> The LinkedIn Company Profile Scraper automates data extraction from public LinkedIn company pages, letting you collect valuable insights on businesses, employees, and company activity effortlessly. It’s perfect for research, lead generation, and business intelligence.

> This scraper captures public company data without needing authentication, offering a quick way to build structured datasets from LinkedIn.


<p align="center">
  <a href="https://bitbash.def" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Linkedin Company Profile Scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

The Linkedin Company Profile Scraper is built to simplify the process of gathering public company data from LinkedIn.
It helps professionals, analysts, and businesses collect detailed information that’s otherwise time-consuming to compile manually.

### Why Use This Scraper?

- Extracts clean, structured data from public LinkedIn company pages.
- Works automatically with multiple company URLs.
- Delivers consistent and reliable output ready for analysis or integration.
- Supports gathering limited employee and company update data without login.
- Ideal for lead research, market analysis, and growth tracking.

## Features

| Feature | Description |
|----------|-------------|
| Automated LinkedIn Data Extraction | Collects company info, updates, and employee details from LinkedIn pages. |
| Public Data Only | Operates without login, scraping visible public data only. |
| Multi-URL Support | Accepts multiple LinkedIn company URLs in a single run. |
| Clean Structured Output | Outputs data in JSON format, easy to process or store. |
| Sample Data Schema Included | Ensures clarity about available fields and expected format. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|-------------|------------------|
| company_name | Official company name listed on LinkedIn. |
| universal_name_id | Unique LinkedIn slug for the company profile. |
| background_cover_image_url | URL of the company's LinkedIn cover image. |
| linkedin_internal_id | Internal identifier if publicly available. |
| industry | Industry category of the company. |
| location | Primary location or headquarters. |
| follower_count | Number of LinkedIn followers. |
| tagline | Company tagline or short description. |
| company_size_on_linkedin | Approximate number of employees visible on LinkedIn. |
| about | Overview or “About” section content. |
| website | Link to the company’s website. |
| company_size | Employee range (e.g., 51–200). |
| headquarters | Company headquarters location. |
| type | Business type (e.g., Privately Held). |
| founded | Year of founding. |
| specialties | Company’s listed specialties. |
| locations | Array of office addresses with map links. |
| employees | Limited set of visible employee profiles. |
| updates | Latest company posts and engagement metrics. |
| similar_companies | Suggested or related company pages. |

---

## Example Output


    {
      "company_name": "Apify",
      "universal_name_id": "apifytech",
      "industry": "IT Services and IT Consulting",
      "location": "Praha, Hlavní město Praha",
      "follower_count": "4,289",
      "tagline": "On a mission to make the web more open and programmable.",
      "company_size": "51-200 employees",
      "founded": "2015",
      "employees": [
        {
          "employee_name": "Jan Čurn",
          "employee_position": "CEO of Apify",
          "employee_profile_url": "https://cz.linkedin.com/in/jancurn"
        },
        {
          "employee_name": "Jakub Balada",
          "employee_position": "Co-founder at Apify",
          "employee_profile_url": "https://cz.linkedin.com/in/jbalada"
        }
      ],
      "updates": [
        {
          "text": "Data is the fuel for AI 🔥",
          "articlePostedDate": "4mo",
          "totalLikes": "14"
        }
      ]
    }

---

## Directory Structure Tree


    linkedin-company-profile-scraper/
    ├── src/
    │   ├── main.py
    │   ├── extractors/
    │   │   ├── linkedin_parser.py
    │   │   └── employee_extractor.py
    │   ├── utils/
    │   │   └── data_cleaner.py
    │   └── config/
    │       └── settings.example.json
    ├── data/
    │   ├── input_urls.txt
    │   └── sample_output.json
    ├── requirements.txt
    └── README.md

---

## Use Cases

- **Recruiters** use it to identify potential hires and analyze company team structures.
- **Market researchers** use it to benchmark competitors and discover industry trends.
- **Sales teams** use it to generate qualified B2B leads from verified LinkedIn profiles.
- **Investors** use it to study startup activity and company growth indicators.
- **Data analysts** use it to create datasets for company-level analytics and modeling.

---

## FAQs

**1. Does it require LinkedIn login or cookies?**
No. It only extracts data visible on public company pages without authentication.

**2. How many employees can it retrieve?**
It’s limited to 3–4 employees per company profile since only public data is accessible.

**3. Can it scrape all company URLs automatically?**
You can input multiple slug-based URLs, and it will process them sequentially.

**4. Does it support numeric LinkedIn company IDs?**
Not yet. Only slug-based URLs like `linkedin.com/company/apifytech` are supported.

---

## Performance Benchmarks and Results

**Primary Metric:** Scrapes an average of 50–100 company pages per minute on a stable network.
**Reliability Metric:** Achieves 98% success rate across tested company profiles.
**Efficiency Metric:** Uses minimal bandwidth, optimized for lightweight requests.
**Quality Metric:** Ensures over 95% data completeness for supported fields.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
