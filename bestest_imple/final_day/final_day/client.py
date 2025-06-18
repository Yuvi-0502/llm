#!/usr/bin/env python3
"""
News Aggregator Client Application
A modular console-based client for the News Aggregation API
"""

from client.main_client import NewsAggregatorClient

def main():
    """Main function to start the News Aggregator client"""
    try:
        client = NewsAggregatorClient()
        client.main_menu()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your connection and try again.")

if __name__ == "__main__":
    main() 