import unittest
from unittest.mock import patch
from Crawler import extract_links_and_emails, crawl, is_url_allowed

class TestExtractLinksAndEmails(unittest.TestCase):

    def test_extract_links_and_emails(self):
        # Mock HTML content
        html = """
        <html>
        <body>
        <a href="http://example.com/page1">Page 1</a>
        <a href="http://example.com/page2">Page 2</a>
        <a href="http://otherdomain.com/page3">Page 3</a>
        Email: test@example.com
        </body>
        </html>
        """
        domain = "example.com"
        expected_links = ["http://example.com/page1", "http://example.com/page2"]
        expected_emails = ["test@example.com"]

        # Call the function to be tested
        links, emails = extract_links_and_emails("http://example.com", html, domain)

        # Assert the results
        self.assertEqual(links, expected_links)
        self.assertEqual(emails, expected_emails)

    def test_extract_links_and_emails_empty_html(self):
        # Test with empty HTML content
        html = ""
        domain = "example.com"
        expected_links = []
        expected_emails = []

        # Call the function to be tested
        links, emails = extract_links_and_emails("http://example.com", html, domain)

        # Assert the results
        self.assertEqual(links, expected_links)
        self.assertEqual(emails, expected_emails)


if __name__ == '__main__':
    unittest.main()