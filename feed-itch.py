import feedparser
import requests
import yaml

def get_itchio_feed(username):
    """
    Retrieves and parses the RSS feed of an Itch.io user's games.

    Args:
        username (str): The Itch.io username.

    Returns:
        list: A list of dictionaries, where each dictionary represents a feed entry.
              Returns None if an error occurs.
    """
    url = f"https://itch.io/games/newest/by-{username}.xml"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        feed = feedparser.parse(response.content)

        if feed.get("entries"):
            return feed.entries
        else:
            print(f"No entries found for {username}.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching feed for {username}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def save_feed_to_yaml(entries, filename="feed.yaml"):
    """
    Saves the feed entries to a YAML file.

    Args:
        entries (list): A list of feed entries.
        filename (str, optional): The name of the YAML file to save to.
                                  Defaults to "feed.yaml".
    """
    if entries:
        try:
            with open(filename, "w") as yaml_file:
                yaml.dump(entries, yaml_file)
            print(f"Feed saved to {filename}")
        except Exception as e:
            print(f"Error saving feed to YAML: {e}")

# Example Usage:
username = "button-masher-brew-games" # Replace with the desired itch.io user name.
feed_entries = get_itchio_feed(username)

if feed_entries:
    save_feed_to_yaml(feed_entries)