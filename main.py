from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd

list_of_list = []
with open('link.txt', 'r') as file:
    links = file.readlines()
links_list = [x.strip() for x in links]

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)


def sign_in():
    driver.get("https://www.linkedin.com/home")
    time.sleep(3)
    driver.maximize_window()
    time.sleep(3)
    email_input = driver.find_element(By.XPATH, '//*[@id="session_key"]')
    
    email_input.send_keys("*********enter your Linkedin Login Id *****************")
    time.sleep(4)
    password_input = driver.find_element(By.XPATH, '//*[@id="session_password"]')
    
    password_input.send_keys("*********enter your Linkedin Pasword *****************")
    time.sleep(5)
    button = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/form[1]/div[2]/button')
    button.click()
    time.sleep(5)


def scroll_down():
    start = time.time()
    initial_scroll = 0
    finals_sroll = 1000

    while True:
        driver.execute_script(f"window.scrollTo({initial_scroll},{finals_sroll})")
        time.sleep(3)
        initial_scroll = finals_sroll
        finals_sroll += 1000
        end = time.time()
        if round(end - start) > 20:
            break


def return_profile_info(employee_link, count):
    try:
        company = "Nil"
        final_list = []
        full_list = []
        profile = []
        i = 1
        url = employee_link
        driver.get(url)
        time.sleep(3)
        scroll_down()
        source = BeautifulSoup(driver.page_source, "html.parser")

        info = source.find('div', class_='mt2 relative')
        name = info.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip()
        title = info.find('div', class_='text-body-medium break-words').get_text().lstrip().strip()
        location = info.find('span', class_='text-body-small inline t-black--light break-words').get_text().strip()

        profile.append(name)
        profile.append(title)
        profile.append(location)
        try:
            company = info.find('span', class_='pv-text-details__right-panel-item-text hoverable-link-text break-words text'
                                               '-body-small t-black').get_text().strip()
            profile.append(company)

        except:
            pass
        # artdeco-list__item pvs-list__item--line-separated pvs-list__item-
        # -one-column pvs-list--ignore-first-item-top-padding
        # artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column
        # artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column
        experiences = source.find_all('li', class_='artdeco-list__item pvs-list__item--line-separated pvs-list'
                                                   '__item--one-column pvs-list--ignore-first-item-top-padding')

        for x in experiences[0:]:
            all_text = x.getText().split('\n')
            full_list.append(all_text)

        for inner_list in full_list:
            for y in range(0, 10):
                if len(inner_list[y]) > 5:
                    i = 0
                    break
                else:
                    i = 1
            if i == 1:
                final_list = inner_list
                break
        new_list = [x for x in final_list if x != '' and x != ' ']
        half_list = [item[:len(item) // 2] for item in new_list]

        if half_list[1][-1] == 's' or half_list[1][-1] == 'o':
            del half_list[:2]
            to_check1 = half_list[0].replace(',', '').split()
            to_check2 = profile[2].replace(',', '').split()
            if to_check1[-1] == to_check2[-1]:
                del half_list[:1]
        if half_list[0] == "Work email" or half_list[0] == "Workplace" or half_list[0] == "Government ID and 1 other":
            half_list[0] = profile[1]

        job_role_list = half_list[0].replace(',', '').replace('-', ' ').replace('.', '').replace('&', '') \
            .replace('|', '').replace('@', ' ').replace('/', ' ').replace(':', '').split()
        if "Chief" in job_role_list:
            role = "C-Officer"
            num = 0
        elif ("Senior" in job_role_list or "Sr" in job_role_list) and ("President" in job_role_list):
            role = "Senior Vice President"
            num = 1
        elif "SVP" in job_role_list:
            role = "Senior Vice President"
            num = 1
        elif "VP" in job_role_list or "President" in job_role_list or "VicePresident" in job_role_list \
                or "Vice" in job_role_list:
            role = "Vice President"
            num = 2
        elif "AVP" in job_role_list:
            role = "Associate Vice President"
            num = 3
        elif ("Senior" in job_role_list or "Sr" in job_role_list) and ("Director" in job_role_list):
            role = "Senior Director"
            num = 4
        elif "Global" in job_role_list and "Director" in job_role_list:
            role = "Global Director"
            num = 5
        elif ("Associate" in job_role_list or "Assistant" in job_role_list) and "Director" in job_role_list:
            role = "Associate Director"
            num = 7
        elif "Director" in job_role_list:
            role = "Director"
            num = 6
        elif "Global" in job_role_list and "Head" in job_role_list:
            role = "Global Head"
            num = 8
        elif "Head" in job_role_list:
            role = "Head"
            num = 9
        elif "Principle" in job_role_list and "Manager" in job_role_list:
            role = "Principle Manager"
            num = 10
        elif "Lead" in job_role_list and "Manager" in job_role_list:
            role = "Lead Manager"
            num = 11
        elif ("Senior" in job_role_list or "Sr" in job_role_list) and ("Manager" in job_role_list):
            role = "Senior Manager"
            num = 12
        elif ("Associate" in job_role_list or "Assistant" in job_role_list) and "Manager" in job_role_list:
            role = "Associate Manager"
            num = 14
        elif "Manager" in job_role_list:
            role = "Manager"
            num = 13
        elif "Leader" in job_role_list or "leader" in job_role_list:
            role = "Leader"
            num = 15
        elif ("Senior" in job_role_list or "Sr" in job_role_list) and ("Consultant" in job_role_list):
            role = "Senior Consultant"
            num = 18
        elif "Consultant" in job_role_list:
            role = "Consultant"
            num = 19
        elif ("Senior" in job_role_list or "Sr" in job_role_list) and ("Partner" in job_role_list):
            role = "Senior Partner"
            num = 20
        elif "Partner" in job_role_list:
            role = "Partner"
            num = 21
        elif ("Senior" in job_role_list or "Sr" in job_role_list) and ("Specialist" in job_role_list):
            role = "Senior Specialist"
            num = 22
        elif "Specialist" in job_role_list:
            role = "Specialist"
            num = 23
        elif "strategist" in job_role_list:
            role = "strategist"
            num = 24
        elif "Coordinator" in job_role_list:
            role = "Coordinator"
            num = 25
        elif "Representative" in job_role_list:
            role = "Representative"
            num = 26
        elif ("Senior" in job_role_list or "Sr" in job_role_list) and ("Executive" in job_role_list):
            role = "Senior Executive"
            num = 27
        elif "Executive" in job_role_list:
            role = "Executive"
            num = 28
        elif ("Senior" in job_role_list or "Sr" in job_role_list) and ("Analyst" in job_role_list):
            role = "Senior Analyst"
            num = 29
        elif "Analyst" in job_role_list:
            role = "Analyst"
            num = 30
        elif ("Senior" in job_role_list or "Sr" in job_role_list) and ("Engineer" in job_role_list):
            role = "Senior Engineer"
            num = 31
        elif "Engineer" in job_role_list:
            role = "Engineer"
            num = 32
        elif ("Senior" in job_role_list or "Sr" in job_role_list) and ("Developer" in job_role_list):
            role = "Senior Developer"
            num = 33
        elif "Developer" in job_role_list:
            role = "Developer"
            num = 34
        elif "Expert" in job_role_list:
            role = "Expert"
            num = 35
        elif ("Senior" in job_role_list or "Sr" in job_role_list) and ("Associate" in job_role_list):
            role = "Senior Associate"
            num = 36
        elif "Associate" in job_role_list:
            role = "Associate"
            num = 37
        elif ("Senior" in job_role_list or "Sr" in job_role_list) and ("Lead" in job_role_list):
            role = "Senior Lead"
            num = 16
        elif "Lead" in job_role_list or "lead" in job_role_list:
            role = "Lead"
            num = 17
        elif "Intern" in job_role_list:
            role = "Intern"
            num = 38
        else:
            role = "Others"
            num = 39

        com_list = [num, profile[0], half_list[0], role, url, profile[1], company, profile[2]]
        list_of_list.append(com_list)
        print(count)
    except:
        list_of_list.append([0, 0, 0, 0, 0, 0, 0, 0])
        print("error")


sign_in()
count = 0
for link in links_list:
    count += 1
    return_profile_info(employee_link=link, count=count)

df = pd.DataFrame(list_of_list, columns=['Hierarchy N0', 'Name', 'Title', 'Role', 'Url',
                                         'Top Job Title', 'Company Name', 'Location'])
df.to_excel('Linkedin_output.xlsx', index=False)
