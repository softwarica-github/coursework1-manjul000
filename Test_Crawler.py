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


    def test_extract_links_and_emails_no_links_or_emails(self):
        # Test with HTML content containing no links or emails
        html = """
        <html>
        <body>
        This is a test page with no links or emails.
        </body>
        </html>
        """
        domain = "example.com"
        expected_links = []
        expected_emails = []

        # Call the function to be tested
        links, emails = extract_links_and_emails("http://example.com", html, domain)

        # Assert the results
        self.assertEqual(links, expected_links)
        self.assertEqual(emails, expected_emails)

    @patch('Crawler.requests.get')
    def test_crawl_depth_limit(self, mock_get):
        # Mock response for the requests.get function
        def mocked_get(url, *args, **kwargs):
            class MockResponse:
                def __init__(self, text, status_code):
                    self.text = text
                    self.status_code = status_code
            # Mock HTML content for the response
            if url == 'http://example.com/page1':
                return MockResponse('<a href="http://example.com/page2">Page 2</a>', 200)
            elif url == 'http://example.com/page2':
                return MockResponse('<a href="http://example.com/page3">Page 3</a>', 200)
            elif url == 'http://example.com/page3':
                return MockResponse('<a href="http://example.com/page4">Page 4</a>', 200)
            elif url == 'http://example.com/page4':
                return MockResponse('<a href="http://example.com/page5">Page 5</a>', 200)
            elif url == 'http://example.com/page5':
                return MockResponse('', 200)  # Empty page
            else:
                return MockResponse('', 404)  # Not Found

        # Assign the mocked function to the mock_get parameter
        mock_get.side_effect = mocked_get

        # Call the crawl function with depth limit of 3
        start_url = 'http://example.com/page1'
        domain = 'example.com'
        depth = 3
        visited = set()
        output_lock = None
        output = crawl(start_url, domain, depth, visited, output_lock)

        # Verify that the crawler stops at the specified depth
        self.assertIn('http://example.com/page1', output)
        self.assertIn('http://example.com/page2', output)
        self.assertIn('http://example.com/page3', output)
        self.assertIn('http://example.com/page4', output)
        self.assertNotIn('http://example.com/page5', output)
    
    @patch('Crawler.requests.get')
    def test_robots_txt_checker(self, mock_get):
        # Mock response for the requests.get function
        def mocked_get(url, *args, **kwargs):
            class MockResponse:
                def __init__(self, text, status_code):
                    self.text = text
                    self.status_code = status_code
            # Mock robots.txt content
            if url == 'http://example.com/robots.txt':
                return MockResponse('User-agent: *\nDisallow: /page3', 200)
            else:
                return MockResponse('', 404)

        # Assign the mocked function to the mock_get parameter
        mock_get.side_effect = mocked_get

        # Test URLs
        urls = ['http://example.com/page1', 'http://example.com/page2', 'http://example.com/page3', 'http://example.com/page4']

        # Check if URLs are allowed based on robots.txt rules
        expected_results = [True, True, False, True]

        # Using list comprehension to compare results
        self.assertEqual([is_url_allowed(url) for url in urls], expected_results)


if __name__ == '__main__':
    unittest.main()