import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_pdfs(url, local_directory):
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the website: {url}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    pdf_links = soup.find_all('a', href=True)
    pdf_links = [link['href'] for link in pdf_links if link['href'].lower().endswith('.pdf')]
    
    for link in pdf_links:
        pdf_url = urljoin(url, link)
        pdf_response = requests.get(pdf_url)
        
        pdf_name = os.path.basename(link)
        pdf_path = os.path.join(local_directory, pdf_name)
        
        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(pdf_response.content)
        
        print(f"Downloaded: {pdf_name}")

if __name__ == "__main__":
    website_url = "https://www.eecs70.org/"
    save_directory = "cs70_marterials"
    download_pdfs(website_url, save_directory)
