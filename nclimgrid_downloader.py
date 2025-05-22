import requests
import os

class NClimGridDownloader:
    BASE_URL = "https://www.ncei.noaa.gov/data/nclimgrid-daily/access/averages"
    VARIABLES = ["prcp", "tmax", "tmin"]
    FILENAME_SUFFIX = "-scaled.csv"  # Based on current file content, adjust if needed

    def __init__(self, default_download_path="noaa_data", default_average_type="div"):
        """
        Initializes the NClimGridDownloader.

        Args:
            default_download_path (str): Default base directory to save downloaded files.
            default_average_type (str): Default type of average (e.g., 'div').
        """
        self.default_download_path = default_download_path
        self.default_average_type = default_average_type
        self.months = [f"{m:02d}" for m in range(1, 13)]

    def _ensure_directory_exists(self, path):
        """Ensures that a directory exists, creating it if necessary."""
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory: {path}")

    def download_data(self, start_year, end_year, download_path=None, average_type=None):
        """
        Downloads nClimGrid-daily area-averaged data for a specified range of years and variables.

        Args:
            start_year (int): The beginning year for data download.
            end_year (int): The ending year for data download.
            download_path (str, optional): The directory to save downloaded files.
                                           Defaults to self.default_download_path.
            average_type (str, optional): The type of average (e.g., 'div').
                                          Defaults to self.default_average_type.
        """
        current_download_path = download_path if download_path is not None else self.default_download_path
        current_average_type = average_type if average_type is not None else self.default_average_type

        self._ensure_directory_exists(current_download_path)

        for year in range(start_year, end_year + 1):
            year_str = str(year)
            year_specific_download_path = os.path.join(current_download_path, year_str)
            self._ensure_directory_exists(year_specific_download_path)

            for var in self.VARIABLES:
                for month_str in self.months:
                    filename = f"{var}-{year_str}{month_str}-{current_average_type}{self.FILENAME_SUFFIX}"
                    file_url = f"{self.BASE_URL}/{year_str}/{filename}"
                    local_filepath = os.path.join(year_specific_download_path, filename)

                    print(f"Attempting to download: {file_url}")
                    try:
                        response = requests.get(file_url, stream=True, timeout=30)
                        response.raise_for_status()  # Raise an exception for HTTP errors

                        with open(local_filepath, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        print(f"Successfully downloaded: {local_filepath}")

                    except requests.exceptions.HTTPError as e:
                        if e.response.status_code == 404:
                            print(f"File not found (404): {file_url}. Skipping.")
                        else:
                            print(f"HTTP error downloading {file_url}: {e}")
                    except requests.exceptions.RequestException as e:
                        print(f"Error downloading {file_url}: {e}")
                    except Exception as e:
                        print(f"An unexpected error occurred for {file_url}: {e}")

if __name__ == '__main__':
    # Example usage:
    # To use this script, you need to have the 'requests' library installed.
    # You can install it by running: pip install requests

    # Instantiate the downloader with default settings
    downloader = NClimGridDownloader()

    # Or with custom default settings for the instance
    # downloader = NClimGridDownloader(default_download_path="my_custom_noaa_data", default_average_type="stn")

    # print("Starting download process...")
    
    # Example: Download data for 2023 using instance defaults 
    # (e.g., "noaa_data" path, "div" average type if using default constructor)
    # downloader.download_data(start_year=2023, end_year=2023)

    # Example: Download data for 2022, overriding defaults for this specific call
    # downloader.download_data(2022, 2022, download_path="custom_path_for_2022", average_type="div")
    
    # Example: Download data for a single month (by setting start_year and end_year to the same year)
    # To download specific months, you would need to modify the download_data method or create a new one,
    # as it currently downloads all months for the given year range.

    print("nClimGrid data downloader script (OOP version).")
    print("To use, instantiate NClimGridDownloader and call its download_data method.")
    print("Example calls:")
    print("  downloader = NClimGridDownloader()")
    print("  downloader.download_data(2020, 2020) # Downloads to 'noaa_data', average_type 'div'")
    print("  downloader.download_data(2021, 2021, download_path=\"custom_path\", average_type=\"stn\")")

