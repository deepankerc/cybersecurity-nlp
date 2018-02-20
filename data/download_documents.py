"""Script for downloading the documents required for analysis.

All of the raw PDFs download to the DOC_OUTPUT_PATH directory, and a csv that
contains metadata about those PDFs downloads to KEY_FILE.

Run with the -k option to download files from the URLs in the "Original URL"
column in KEY_FILE.
    
    python download_documents.py -k

Otherwise, the script will fetch the URLs from the website. Since there are a
reasonable number of them (~100), the script will prompt the user to double
check the metadata for each downloaded doc. This metadata gets saved into
KEY_FILE

    python download_documents.py

"""

import argparse
from bs4 import BeautifulSoup
from collections import namedtuple
import csv
import logging
import re
import requests
from tqdm import tqdm
from urllib.parse import urljoin

# document URLs
BASE_URL = "https://www.itu.int"
REPOSITORY_PATH = BASE_URL + \
    "/en/ITU-D/Cybersecurity/Pages/National-Strategies-repository.aspx"
DOCUMENT_PATH = \
    "/en/ITU-D/Cybersecurity/Documents/National_Strategies_Repository/"

# output paths
DOC_OUTPUT_PATH = "raw/"
KEY_FILE = "../cybersecurity_nlp/data_utils/document_key.csv"

# value format
LinkAnnotation = namedtuple("LinkAnnotation", ["country", "year"])


def filename_from_url(url):
    return url.split("/")[-1]


def find_docs():
    url_to_annotation = {}
    repo = requests.get(REPOSITORY_PATH)
    soup = BeautifulSoup(repo.content, "lxml")
    all_links = soup.find_all("a")
    for link in all_links:
        href = link.get("href", "")
        if href.startswith(DOCUMENT_PATH):
            country_guess = link.text.strip()
            year_match = re.search(r"[0-9]{4}", filename_from_url(href))
            year_guess = year_match.group(0) if year_match else "Unknown"
            full_url = urljoin(BASE_URL, href)
            if full_url not in url_to_annotation:
                url_to_annotation[full_url] = LinkAnnotation(
                    country_guess, year_guess)
    return url_to_annotation


def validate_guesses(url_to_annotation):
    for k in url_to_annotation.keys():
        annotation = url_to_annotation[k]
        print("Document Name:\n", filename_from_url(k))
        user_country = input("Validate country (%s)? " % annotation.country)
        user_year = input("Validate year (%s)? " % annotation.year)
        print("\n")
        country, year = annotation.country, annotation.year
        if user_country != "":
            country = user_country
        if user_year != "":
            year = user_year
        url_to_annotation[k] = LinkAnnotation(country, year)


def write_key(url_to_annotation):
    logging.info("Writing key...")
    with open(KEY_FILE, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Country", "Year", "File", "OriginalURL"])
        for url, annotation in url_to_annotation.items():
            writer.writerow(
                [annotation.country, annotation.year,
                 filename_from_url(url), url])


def download_docs(urls):
    logging.info("Downloading docs...")
    for url in tqdm(urls):
        doc = requests.get(url)
        with open(DOC_OUTPUT_PATH + filename_from_url(url), "wb") as f:
            f.write(doc.content)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", required=False, action="store_true",
                        help="Download files from the key file.")
    args = parser.parse_args()
    return args


def urls_from_key_file():
    with open(KEY_FILE, "r") as f:
        reader = csv.reader(f)
        all_rows = [row for row in reader]
        i = all_rows[0].index("Original URL")
        all_urls = [row[i] for row in all_rows[1:]]
    return all_urls


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    args = parse_args()
    if not args.key:
        url_to_annotation = find_docs()
        validate_guesses(url_to_annotation)
        write_key(url_to_annotation)
        download_docs(url_to_annotation.keys())
    else:
        urls = urls_from_key_file()
        download_docs(urls)
