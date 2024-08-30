import argparse
from bs4 import BeautifulSoup
import re

def extract_job_id_from_html(soup):
    # try to find job ID in a <h1> tag with the specific class
    header_tag = soup.find('h1', class_='h3 dashboard-header__profile-information-name mobile--small-font color--font--white margin--b--s')
    if header_tag:
        header_text = header_tag.get_text(strip=True)
        match = re.match(r'^(\d+)', header_text)
        if match:
            return match.group(1)
    
    # if not found, try to find an <h1> tag containing the words "Job ID"
    job_id_tag = soup.find('h1', string=re.compile(r'Job ID', re.IGNORECASE))
    if job_id_tag:
        job_id_text = job_id_tag.get_text(strip=True)
        match = re.search(r'Job ID\s*:\s*(\d+)', job_id_text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def parse_html_file(filepath, verbose=False):
    with open(filepath, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'lxml')

    data = {}
    job_id = extract_job_id_from_html(soup)
    if job_id:
        data['Job ID'] = job_id

    rows = soup.find_all('tr')  # find all table rows

    for row in rows:
        tds = row.find_all('td')  # find all table data cells
        
        if len(tds) >= 2:
            label_td = tds[0]
            label_text = '\n'.join(label_td.stripped_strings).replace(':', '')
            
            value_td = tds[1]
            value_text = '\n'.join(value_td.stripped_strings)
            
            data[label_text] = value_text

    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse HTML for 2 column table data.")
    parser.add_argument("-f", "--filepath", required=True, help="Path to the HTML file to be parsed.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print parsed data.")

    args = parser.parse_args()

    data = parse_html_file(args.filepath, args.verbose)
    
    if args.verbose:
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print("Parsing completed.")
