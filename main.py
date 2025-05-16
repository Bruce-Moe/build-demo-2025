# main.py

import requests
import json

# Dummy URL for fetching a list of numbers
# Example data at this URL could be: [10, -5, 20, -15, 30]
# Or: [-1, -2, -3] (to trigger the bug)
# Or: [] (to trigger the bug)
DATA_URL = "https://raw.githubusercontent.com/your_username/your_repo/main/dummy_data.json" # Replace with an actual URL hosting dummy data

def fetch_data(url):
  """
  Fetches a list of numbers from a given URL.

  Args:
    url: The URL to fetch data from.

  Returns:
    A list of numbers, or None if fetching fails.
  """
  try:
    response = requests.get(url)
    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
    data = response.json()
    if isinstance(data, list):
        # Attempt to convert list elements to numbers, handle errors
        processed_data = []
        for item in data:
            try:
                processed_data.append(float(item)) # Convert to float to handle integers and decimals
            except (ValueError, TypeError):
                print(f"Warning: Could not convert item '{item}' to a number. Skipping.")
                continue
        return processed_data
    else:
        print(f"Error: Fetched data is not a list. Type: {type(data)}")
        return None
  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from {url}: {e}")
    return None
  except json.JSONDecodeError:
    print(f"Error decoding JSON from {url}")
    return None


def process_data(data):
  """
  Filters out negative numbers from a list.

  Args:
    data: A list of numbers.

  Returns:
    A new list containing only non-negative numbers.
    Returns an empty list if the input is None or not a list.
  """
  if not isinstance(data, list):
      print("Warning: Input to process_data is not a list.")
      return []

  filtered_data = [num for num in data if num >= 0]
  return filtered_data

def calculate_sum(numbers):
  """
  Calculates the sum of a list of numbers.

  Args:
    numbers: A list of numbers.

  Returns:
    The sum of the numbers.
    Returns None if the input is None or not a list.
    # BUG: Returns None for an empty list instead of 0
  """
  if not isinstance(numbers, list):
      print("Warning: Input to calculate_sum is not a list.")
      return None

  # BUG: This returns None if the list is empty, instead of 0
  # A correct implementation would handle the empty list case explicitly
  # For example: return sum(numbers) if numbers is not None else 0
  return sum(numbers)


def main():
  print(f"Attempting to fetch data from: {DATA_URL}")
  raw_data = fetch_data(DATA_URL)

  if raw_data is not None:
    print(f"Successfully fetched data: {raw_data}")
    processed_data = process_data(raw_data)
    print(f"Processed data (non-negative): {processed_data}")
    total_sum = calculate_sum(processed_data)

    print(f"The calculated sum of the processed data is: {total_sum}")
  else:
    print("Failed to fetch or process data.")


if __name__ == "__main__":
  main()
