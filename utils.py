import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import math, random, datetime


def get_text(text):
    """
    Requests text attribute of Beautifulsoup response and strips unnecessary space.

    Parameters
    ----------
    text : Beautifulsoup Attribute
        Beautifulsoup attribute to be cleaned.

    Returns
    ------
    clean_text : str
        Data point from HTML source.
    """

    clean_text = text.text.strip()
    return clean_text


def clean_salary(salary):
    """
    Requests text attribute of Beautifulsoup response, strips spaces and replaces characters.

    Parameters
    ----------
    salary : Beautifulsoup Attribute
        Beautifulsoup attribute to be cleaned.

    Returns
    ------
    clean_salary : str
        Data point from HTML source.
    """

    clean_salary = salary.text.strip().replace('£','').replace(',','')
    return clean_salary


def clean_search_term(search_term):
    """
    Transforms users search term into format used in URL.

    Parameters
    ----------
    search_term : str
        Job title the user wants to search for.

    Returns
    ------
    search_term : str
        Formatted search term to be used in the URL requests.
    """

    search_term = search_term.replace(' ','-')
    return search_term.lower()


def export_to_csv(file_name, source_data):
    """
    Exports scraped data to CSV file avoiding encoding issues.

    Parameters
    ----------
    file_name : str
        Desired name of the output CSV file.

    source_data : dataframe
        The scraped data stored during scraping.

    Returns
    ------
    """

    with open(f"{file_name}.csv", 'a', encoding='utf8', errors='replace') as file:
        source_data.to_csv(file, index=False)


def scrape_reed(job_title, uk_city='london', start_page=1, file_name='scraped_data'):
    """
    Scrapes data from Reed job advert website.

    Parameters
    ----------
    job_title : str
        Term to search Reed job advert website for.

    uk_city : str -> default
        The city to search for jobs (Reed only operates in UK cities).
        default -> london

    start_page : int
        The page number on which to start the search.
        default -> 1

    file_name : str
        The desired file name for the output CSV file with the scraped data.
        default -> scraped_data.csv

    Returns
    ------
    df : dataframe
        Dataframe with the scraped data. A CSV file is also created in same directory using file_name.
    """
    
    # Initialise variables
    title_list, link_list, posted_by_list, salary_list = ([] for i in range(4))
    location_list, job_type_list, description_list = ([] for i in range(3))
    today = datetime.date.today().strftime("%d %B %Y")
    current_page = start_page
    jobs_scraped = 0
    job_title = clean_search_term(job_title)
    base_url = f'https://www.reed.co.uk/jobs/{job_title}-jobs-in-{uk_city}?'
    
    # Request first page of results
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find number of pages by dividing # jobs vy jobs/page (25)
    num_pages = math.ceil(
    int(
        soup.find('div',attrs={'class':'page-counter'}).text.strip().split('of ')[1].split(' ')[0].replace(',','')
        )
    /25)
    print(f'{num_pages} page(s) found to scrape...')
    print('-'*10)
    
    # Scrape each listing on every page
    while current_page <= num_pages:

        # Request page and find all job postings on current page
        response = requests.get(f'{base_url}?pageno={current_page}')
        sleep(random.randint(1,3))
        soup = BeautifulSoup(response.text, 'html.parser')
        all_postings = soup.find_all('article', attrs={'class':'job-result-card'})
    
        # Scrape each posting
        for job in all_postings:
            job_title = get_text(job.find(attrs={'class':'job-result-heading__title'}))
            direct_link = 'https://www.reed.co.uk'+job.find(attrs={'class':'job-result-heading__title'}).find('a')['href']
            posted_by = get_text(job.find(attrs={'class':'job-result-heading__posted-by'}).find('a'))
            salary = clean_salary(job.find(attrs={'class':'job-metadata__item job-metadata__item--salary'}))
            location = get_text(job.find(attrs={'class':'job-metadata__item job-metadata__item--location'}).find('span'))
            job_type = get_text(job.find(attrs={'class':'job-metadata__item job-metadata__item--type'}))

            # Get the description from the job posting
            direct_posting = requests.get(direct_link)
            listing_soup = BeautifulSoup(direct_posting.text, 'html.parser')
            description = get_text(listing_soup.find('span', attrs={'itemprop':'description'}))

            # Append scraped data to respective list
            title_list.append(job_title)
            link_list.append(direct_link)
            posted_by_list.append(posted_by)
            salary_list.append(salary)
            location_list.append(location)
            job_type_list.append(job_type)
            description_list.append(description)
            sleep(.2)
        print(f'Page {current_page} scraped successfully')
        current_page += 1
        
    # Create Dataframe
    data_dict = {'job_title':title_list, 'posted_by':posted_by_list, 'salary':salary_list, 'location':location_list,
             'job_type':job_type_list, 'direct_link':link_list, 'job_description':description_list}
    df = pd.DataFrame(data_dict)
    df['scrape_date'] = today


    # Export data to CSV
    export_to_csv(file_name=file_name, source_data=df)
    return df

        










