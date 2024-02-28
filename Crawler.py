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


def is_url_allowed(url):
    try:
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        
        # Fetch the robots.txt file
        response = requests.get(robots_url)
        
        # Check if the robots.txt file exists and is accessible
        if response.status_code == 200:
            rp = RobotFileParser()
            rp.parse(response.text.splitlines())
            return rp.can_fetch("*", url)
        else:
            return True  # If robots.txt is not accessible, assume allowed
    except Exception as e:
        print(f"Error reading robots.txt for {url}: {e}")
        return False

# Function to crawl a webpage
def crawl(url, domain, depth, visited, output_lock):
    if depth == 0 or url in visited or not is_url_allowed(url):
        return ""

    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            links, emails = extract_links_and_emails(url, html, domain)

            output = f"Links found at {url}:\n"
            for link in links:
                # Check if the link belongs to the same domain
                if domain in link:
                    output += f"{link}\n"
                    # Recursively crawl links if depth allows and the URL is allowed
                    if is_url_allowed(link):
                        output += crawl(link, domain, depth - 1, visited, output_lock)
            output += f"Emails found at {url}:\n"
            for email in emails:
                output += f"{email}\n"
            output += '-' * 50 + '\n'

            visited.add(url)  # Update visited set

            return output
    except Exception as e:
        return f"Error while crawling {url}: {e}\n"

    return ""
