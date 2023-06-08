import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

class SteamScraper:

    def __init__(self, url):
        self.url = url

    def get_page_content(self):
        # Send a GET request to the URL
        page = requests.get(self.url)
        # Parse the page content with BeautifulSoup and return the soup object
        return BeautifulSoup(page.content, 'html.parser')

    def get_game_sales(self, soup):
        """
        This function gets game sales information from the BeautifulSoup object.
        It returns a list of tuples, where each tuple represents a game and contains its title and price.
        """
        # Find all game entries on the page
        games = soup.find_all('a', {'class': 'search_result_row'})

        output_data = []
        for game in games:
            # Extract game title
            title = game.find('span', {'class': 'title'}).get_text()
            # Try to extract game price, if it fails, the game is free to play
            try:
                price = game.find('div', {'class': 'search_price'}).get_text().strip()
            except:
                price = "Free to Play"

            # Add the game title and price as a tuple to the output list
            output_data.append((title, price))

        return output_data

    def print_game_sales(self, game_sales):
        """
        This function takes a list of game sales information (as returned by get_game_sales) 
        and prints it in a formatted table using PrettyTable.
        """
        # Create a PrettyTable object with "Title" and "Price" as column headers
        table = PrettyTable(["Title", "Price"])
        for game in game_sales:
            # Add each game sale as a row in the table
            table.add_row(game)
        # Print the table
        print(table)


if __name__ == "__main__":
    scraper = SteamScraper('https://store.steampowered.com/search/?filter=topsellers')
    soup = scraper.get_page_content()
    game_sales = scraper.get_game_sales(soup)
    scraper.print_game_sales(game_sales)
