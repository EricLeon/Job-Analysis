from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd


def get_jobs(keyword, num_jobs, verbose):
    
    """

    Parameters
    ----------

    
    Returns
    ------

    """

    # Set up the URL(s) to scrape
    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'

    # Create instance of Chrome driver and request URL
    options = Options()
    options.add_argument('start-maximized')
    #options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    # Initialise Dataframe to hold jobs
    jobs = []

    
    # Scrape jobs
    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        # TODO: Check what this does?
        time.sleep(4)

        #Test for the "Sign Up" prompts and get rid of them.
        # try:
        #     driver.find_element(by=By.CLASS_NAME, value="selected").click()
        #     time.sleep(3)
        # except ElementClickInterceptedException:
        #     pass

        # try:
        #     driver.find_element(by=By.CLASS_NAME, value="ModalStyle__xBtn___29PT9").click() 
        #     time.sleep(3)
        # except NoSuchElementException:
        #     pass

        
        # Find all the job listing "buttons" (postings)
        # job_buttons = driver.find_elements(by=By.CLASS_NAME, value="react-job-listing")
        # job_buttons = driver.find_elements(by=By.XPATH, value='//*[@id="MainCol"]/div[1]/ul/li[1]')
        all_jobs = driver.find_element(by = By.XPATH, value = '//*[@id="MainCol"]/div[1]/ul')
        job_buttons = all_jobs.find_elements(by=By.CLASS_NAME, value="react-job-listing")

        
        # Navigate to each posting and scrape data
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()
            time.sleep(3)
            collected_successfully = False

            try:
                driver.find_element(by=By.XPATH, value='//*[@id="JAModal"]/div/div[2]/span').click()
                time.sleep(3)
            except NoSuchElementException:
            	pass
            
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element(by=By.XPATH, value='//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]').text
                    print(company_name)
                    # location = driver.find_element_by_xpath('.//div[@class="location"]').text
                    # job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                    # job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

    #         try:
    #             salary_estimate = driver.find_element_by_xpath('.//span[@class="gray small salary"]').text
    #         except NoSuchElementException:
    #             salary_estimate = -1 #You need to set a "not found value. It's important."
            
    #         try:
    #             rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
    #         except NoSuchElementException:
    #             rating = -1 #You need to set a "not found value. It's important."

    #         #Printing for debugging
    #         if verbose:
    #             print("Job Title: {}".format(job_title))
    #             print("Salary Estimate: {}".format(salary_estimate))
    #             print("Job Description: {}".format(job_description[:500]))
    #             print("Rating: {}".format(rating))
    #             print("Company Name: {}".format(company_name))
    #             print("Location: {}".format(location))

    #         #Going to the Company tab...
    #         #clicking on this:
    #         #<div class="tab" data-tab-type="overview"><span>Company</span></div>
    #         try:
    #             driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()

    #             try:
    #                 #<div class="infoEntity">
    #                 #    <label>Headquarters</label>
    #                 #    <span class="value">San Francisco, CA</span>
    #                 #</div>
    #                 headquarters = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
    #             except NoSuchElementException:
    #                 headquarters = -1

    #             try:
    #                 size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
    #             except NoSuchElementException:
    #                 size = -1

    #             try:
    #                 founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
    #             except NoSuchElementException:
    #                 founded = -1

    #             try:
    #                 type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
    #             except NoSuchElementException:
    #                 type_of_ownership = -1

    #             try:
    #                 industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
    #             except NoSuchElementException:
    #                 industry = -1

    #             try:
    #                 sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
    #             except NoSuchElementException:
    #                 sector = -1

    #             try:
    #                 revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
    #             except NoSuchElementException:
    #                 revenue = -1

    #             try:
    #                 competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
    #             except NoSuchElementException:
    #                 competitors = -1

    #         except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
    #             headquarters = -1
    #             size = -1
    #             founded = -1
    #             type_of_ownership = -1
    #             industry = -1
    #             sector = -1
    #             revenue = -1
    #             competitors = -1

                
    #         if verbose:
    #             print("Headquarters: {}".format(headquarters))
    #             print("Size: {}".format(size))
    #             print("Founded: {}".format(founded))
    #             print("Type of Ownership: {}".format(type_of_ownership))
    #             print("Industry: {}".format(industry))
    #             print("Sector: {}".format(sector))
    #             print("Revenue: {}".format(revenue))
    #             print("Competitors: {}".format(competitors))
    #             print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    #         jobs.append({"Job Title" : job_title,
    #         "Salary Estimate" : salary_estimate,
    #         "Job Description" : job_description,
    #         "Rating" : rating,
    #         "Company Name" : company_name,
    #         "Location" : location,
    #         "Headquarters" : headquarters,
    #         "Size" : size,
    #         "Founded" : founded,
    #         "Type of ownership" : type_of_ownership,
    #         "Industry" : industry,
    #         "Sector" : sector,
    #         "Revenue" : revenue,
    #         "Competitors" : competitors})
    #         #add job to jobs

    #     #Clicking on the "next page" button
    #     try:
    #         driver.find_element_by_xpath('.//li[@class="next"]//a').click()
    #     except NoSuchElementException:
    #         print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
    #         break

    # return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.


df = get_jobs("data scientist", 5, False)
print(df)