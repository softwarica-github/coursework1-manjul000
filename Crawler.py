import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
from urllib.robotparser import RobotFileParser

# Function to extract links and emails from a webpage
def extract_links_and_emails(url, html, domain):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    emails = []

    # Extracting links
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('http') and domain in href:
            links.append(href)
        elif not href.startswith('http'):
            links.append(urljoin(url, href))

    # Extracting emails using regex
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails.extend(re.findall(email_regex, html))

    return links, emails