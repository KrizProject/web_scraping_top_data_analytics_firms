import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

BASE_URL = "https://www.goodfirms.co"
TARGET_URL = "https://www.goodfirms.co/data-analytics-companies"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def extract_email(text):
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    match = re.search(email_pattern, text)
    return match.group(0) if match else "Not Found"

response = requests.get(TARGET_URL, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

companies = []

company_cards = soup.select(".firm-card")

for card in company_cards:
    name = card.select_one(".firm-name")
    geo = card.select_one(".firm-location a")
    profile_link = card.select_one("a.firm-name")

    company_name = name.text.strip() if name else "N/A"
    company_geo = geo.text.strip() if geo else "N/A"
    company_profile_url = BASE_URL + profile_link["href"] if profile_link else "N/A"

    # Visit company profile to extract website & email
    email = "Not Found"
    website = "N/A"

    try:
        profile_response = requests.get(company_profile_url, headers=headers)
        profile_soup = BeautifulSoup(profile_response.text, "lxml")

        website_tag = profile_soup.select_one("a.visit-website")
        website = website_tag["href"] if website_tag else "N/A"

        page_text = profile_soup.get_text()
        email = extract_email(page_text)

    except Exception as e:
        print(f"Error scraping {company_name}: {e}")

    companies.append({
        "Company Name": company_name,
        "Company URL": website,
        "Company Geo": company_geo,
        "Company Email": email
    })

df = pd.DataFrame(companies)
df.to_csv("data_analytics_companies.csv", index=False)

print("Scraping completed successfully.")
