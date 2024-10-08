# Scrape and Tokenize whole website for LLMs

This project aims to extract the urls from a website's sitemap, scrape the text from each URL, clean the text, and prepare it for use in a Large Language Model (LLM) by tokenizing the text.

## Features

- **Retry Mechanism**: Robust retry mechanism for handling network issues.
- **Concurrent Scraping**: Efficiently scrape multiple URLs concurrently.
- **Text Cleaning**: Clean and preprocess the extracted text.
- **Logging**: Detailed logging for monitoring the scraping process.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/faisal-fida/web-text-scraper.git
    cd web-text-scraper
    ```

2. Install the required dependencies using Poetry:
    ```sh
    pip install poetry
    poetry install
    ```

3. Activate the virtual environment and run the script:
    ```sh
    poetry shell
    ```

## Usage

1. Update the `sitemap_url` in `main.py` with the URL of the sitemap you want to scrape.
2. Run the script:
    ```sh
    python main.py
    ```

## Project Structure

- `utils.py`: Contains the `RetrySession` class with a custom retry decorator.
- `parser.py`: Contains the `SitemapParser` class for parsing sitemap URLs.
- `scraper.py`: Contains the `Scraper` class for extracting and cleaning text from URLs.
- `main.py`: Main script to orchestrate the scraping process and save the extracted text to files.


