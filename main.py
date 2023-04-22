#!/usr/bin/env python3

import requests
import urllib.request
import os
from datetime import datetime

def get_bing_wallpaper():
    try:
        # Bing Wallpaper API URL
        api_url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"

        # Make an HTTP request to the API
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        # Extract the wallpaper URL
        base_url = "https://www.bing.com"
        wallpaper_url = base_url + data["images"][0]["url"]

        # Check if the wallpaper URL has changed
        last_wallpaper_url_file = "last_wallpaper_url.txt"
        if os.path.exists(last_wallpaper_url_file):
            with open(last_wallpaper_url_file, "r") as f:
                last_wallpaper_url = f.read()
            if wallpaper_url == last_wallpaper_url:
                print("Daily wallpaper has not changed.")
                return

        # Save the new wallpaper URL
        with open(last_wallpaper_url_file, "w") as f:
            f.write(wallpaper_url)

        # Create the "Downloaded_Wallpapers" folder if it doesn't exist
        folder_path = "Downloaded_Wallpapers"
        os.makedirs(folder_path, exist_ok=True)

        # Download the wallpaper
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{current_date}.jpg"
        file_path = os.path.join(folder_path, file_name)
        urllib.request.urlretrieve(wallpaper_url, file_path)

        print(f"Downloaded daily wallpaper: {file_name}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_bing_wallpaper()
