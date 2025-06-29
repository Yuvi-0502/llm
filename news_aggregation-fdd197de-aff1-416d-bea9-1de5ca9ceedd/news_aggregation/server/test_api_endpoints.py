#!/usr/bin/env python3
"""
Test script to verify the enhanced API endpoints work correctly
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "test_password"

class APITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.session = requests.Session()
    
    def test_public_endpoints(self):
        """Test public endpoints that don't require authentication"""
        print("Testing Public Endpoints...")
        print("=" * 50)
        
        # Test news status
        print("1. Testing /news/status")
        try:
            response = self.session.get(f"{self.base_url}/news/status")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Total articles: {data.get('total_articles', 'N/A')}")
                print(f"Categories: {len(data.get('categories', []))}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test categories
        print("\n2. Testing /news/categories")
        try:
            response = self.session.get(f"{self.base_url}/news/categories")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Categories found: {len(data.get('categories', []))}")
                for cat in data.get('categories', [])[:3]:  # Show first 3
                    print(f"  - {cat.get('category_name')}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test today's articles
        print("\n3. Testing /news/today")
        try:
            response = self.session.get(f"{self.base_url}/news/today?page=1&limit=5")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                print(f"Articles found: {len(articles)}")
                if articles:
                    print(f"First article: {articles[0].get('title', 'N/A')[:50]}...")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
    
    def test_authentication(self):
        """Test authentication endpoints"""
        print("\nTesting Authentication...")
        print("=" * 50)
        
        # Test registration
        print("1. Testing registration")
        register_data = {
            "username": "test_user",
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        
        try:
            response = self.session.post(f"{self.base_url}/auth/register", json=register_data)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("Registration successful")
            else:
                print(f"Registration response: {response.text}")
        except Exception as e:
            print(f"Registration error: {e}")
        
        # Test login
        print("\n2. Testing login")
        login_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        
        try:
            response = self.session.post(f"{self.base_url}/auth/login", json=login_data)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('access_token')
                print(f"Login successful, token: {self.token[:20]}...")
                # Set token for future requests
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
            else:
                print(f"Login response: {response.text}")
        except Exception as e:
            print(f"Login error: {e}")
    
    def test_authenticated_endpoints(self):
        """Test endpoints that require authentication"""
        if not self.token:
            print("No authentication token available, skipping authenticated tests")
            return
        
        print("\nTesting Authenticated Endpoints...")
        print("=" * 50)
        
        # Test user headlines today
        print("1. Testing /user/headlines/today")
        try:
            response = self.session.get(f"{self.base_url}/user/headlines/today?page=1&limit=5")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                print(f"Articles found: {len(articles)}")
                if articles:
                    print(f"First article: {articles[0].get('title', 'N/A')[:50]}...")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test search
        print("\n2. Testing /user/search")
        try:
            response = self.session.get(f"{self.base_url}/user/search?query=news&page=1&limit=5")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                print(f"Search results: {len(articles)}")
                if articles:
                    print(f"First result: {articles[0].get('title', 'N/A')[:50]}...")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test categories
        print("\n3. Testing /user/categories")
        try:
            response = self.session.get(f"{self.base_url}/user/categories")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                categories = data.get('categories', [])
                print(f"Categories found: {len(categories)}")
                for cat in categories[:3]:  # Show first 3
                    print(f"  - {cat.get('category_name')}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test saved articles
        print("\n4. Testing /user/saved-articles")
        try:
            response = self.session.get(f"{self.base_url}/user/saved-articles?page=1&limit=5")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                print(f"Saved articles: {len(articles)}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
    
    def test_news_fetch(self):
        """Test manual news fetching"""
        print("\nTesting News Fetch...")
        print("=" * 50)
        
        print("1. Testing /news/fetch")
        try:
            response = self.session.post(f"{self.base_url}/news/fetch")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Fetch result: {data.get('message', 'N/A')}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
    
    def test_pagination(self):
        """Test pagination functionality"""
        print("\nTesting Pagination...")
        print("=" * 50)
        
        if not self.token:
            print("No authentication token available, skipping pagination tests")
            return
        
        print("1. Testing pagination with /user/headlines/today")
        try:
            response = self.session.get(f"{self.base_url}/user/headlines/today?page=1&limit=3")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                pagination = data.get('pagination', {})
                print(f"Page: {pagination.get('page')}")
                print(f"Limit: {pagination.get('limit')}")
                print(f"Total: {pagination.get('total')}")
                print(f"Pages: {pagination.get('pages')}")
                print(f"Articles in response: {len(data.get('articles', []))}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("Starting API Endpoint Tests")
        print("=" * 60)
        
        self.test_public_endpoints()
        self.test_authentication()
        self.test_authenticated_endpoints()
        self.test_news_fetch()
        self.test_pagination()
        
        print("\n" + "=" * 60)
        print("API Endpoint Tests Completed!")

def main():
    """Main test function"""
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 