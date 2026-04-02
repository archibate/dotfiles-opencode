"""Tests for jina-ai skill."""
import sys
import os
import pytest
from unittest.mock import Mock, patch

# Add parent directory to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import jina_tools


@pytest.fixture
def mock_requests_get():
    """Mock requests.get."""
    with patch('jina_tools.requests.get') as mock:
        yield mock


class TestGetHeaders:
    """Test the get_headers function."""
    
    def test_headers_with_api_key(self):
        """Test headers with API key set."""
        with patch.dict(os.environ, {'JINA_API_KEY': 'test_key'}):
            headers = jina_tools.get_headers(use_json=True)
        
        assert headers['Authorization'] == 'Bearer test_key'
        assert headers['X-Return-Format'] == 'json'
    
    def test_headers_without_api_key(self):
        """Test headers without API key."""
        with patch.dict(os.environ, {}, clear=True):
            headers = jina_tools.get_headers(use_json=True)
        
        assert 'Authorization' not in headers
        assert headers['X-Return-Format'] == 'json'
    
    def test_headers_without_json(self):
        """Test headers without JSON format."""
        headers = jina_tools.get_headers(use_json=False)
        assert 'X-Return-Format' not in headers


class TestReadUrl:
    """Test the read_url function."""
    
    def test_read_url_success(self, mock_requests_get):
        """Test successful URL reading."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': {
                'title': 'Test Page',
                'url': 'https://example.com',
                'content': '# Test Content\n\nThis is a test.'
            }
        }
        mock_response.raise_for_status = Mock()
        mock_requests_get.return_value = mock_response
        
        result = jina_tools.read_url('https://example.com')
        
        assert result['title'] == 'Test Page'
        assert result['url'] == 'https://example.com'
        assert result['content_markdown'] == '# Test Content\n\nThis is a test.'
        
        # Verify the correct URL was called
        call_args = mock_requests_get.call_args
        assert 'https://r.jina.ai/https://example.com' in str(call_args)
    
    def test_read_url_missing_fields(self, mock_requests_get):
        """Test URL reading with missing data fields."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': {}
        }
        mock_response.raise_for_status = Mock()
        mock_requests_get.return_value = mock_response
        
        result = jina_tools.read_url('https://example.com')
        
        assert result['title'] == 'Untitled'
        assert result['url'] == 'https://example.com'
        assert result['content_markdown'] == ''
    
    def test_read_url_request_error(self, mock_requests_get):
        """Test URL reading with request error."""
        mock_requests_get.side_effect = Exception("Network error")
        
        with pytest.raises(SystemExit):
            jina_tools.read_url('https://example.com')
    
    def test_read_url_with_api_key(self, mock_requests_get):
        """Test URL reading with API key."""
        mock_response = Mock()
        mock_response.json.return_value = {'data': {}}
        mock_response.raise_for_status = Mock()
        mock_requests_get.return_value = mock_response
        
        with patch.dict(os.environ, {'JINA_API_KEY': 'test_key'}):
            jina_tools.read_url('https://example.com')
        
        # Check that Authorization header was included
        call_kwargs = mock_requests_get.call_args[1]
        assert 'Authorization' in call_kwargs['headers']
        assert call_kwargs['headers']['Authorization'] == 'Bearer test_key'


class TestSearchWeb:
    """Test the search_web function."""
    
    def test_search_web_success(self, mock_requests_get):
        """Test successful web search."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {
                    'title': 'Result 1',
                    'url': 'https://example1.com',
                    'content': 'Content 1'
                },
                {
                    'title': 'Result 2',
                    'url': 'https://example2.com',
                    'content': 'Content 2'
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_requests_get.return_value = mock_response
        
        results = jina_tools.search_web('test query')
        
        assert len(results) == 2
        assert results[0]['title'] == 'Result 1'
        assert results[0]['url'] == 'https://example1.com'
        assert results[0]['content_markdown'] == 'Content 1'
        assert results[1]['title'] == 'Result 2'
    
    def test_search_web_empty_results(self, mock_requests_get):
        """Test search with no results."""
        mock_response = Mock()
        mock_response.json.return_value = {'data': []}
        mock_response.raise_for_status = Mock()
        mock_requests_get.return_value = mock_response
        
        results = jina_tools.search_web('test query')
        
        assert len(results) == 0
    
    def test_search_web_missing_fields(self, mock_requests_get):
        """Test search with missing data fields."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': [
                {
                    # Missing title, url, content
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_requests_get.return_value = mock_response
        
        results = jina_tools.search_web('test query')
        
        assert len(results) == 1
        assert results[0]['title'] == 'Untitled'
        assert results[0]['url'] == ''
        assert results[0]['content_markdown'] == ''
    
    def test_search_web_request_error(self, mock_requests_get):
        """Test search with request error."""
        mock_requests_get.side_effect = Exception("API error")
        
        with pytest.raises(SystemExit):
            jina_tools.search_web('test query')
    
    def test_search_web_with_query_params(self, mock_requests_get):
        """Test that search query is passed correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {'data': []}
        mock_response.raise_for_status = Mock()
        mock_requests_get.return_value = mock_response
        
        jina_tools.search_web('my search query')
        
        # Verify query parameter was passed
        call_kwargs = mock_requests_get.call_args[1]
        assert call_kwargs['params'] == {'q': 'my search query'}


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_read_url_http_error(self, mock_requests_get):
        """Test read_url handles HTTP errors."""
        import requests
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_requests_get.return_value = mock_response
        
        with pytest.raises(SystemExit):
            jina_tools.read_url('https://notfound.com')
    
    def test_search_web_http_error(self, mock_requests_get):
        """Test search_web handles HTTP errors."""
        import requests
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
        mock_requests_get.return_value = mock_response
        
        with pytest.raises(SystemExit):
            jina_tools.search_web('test query')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
