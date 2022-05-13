from utils import scrape_reed

# Collect data from Reed for Data Analyst jobs in London
scrape_reed(job_title='Data Analyst', uk_city='london', database_path='reed_jobs.db')