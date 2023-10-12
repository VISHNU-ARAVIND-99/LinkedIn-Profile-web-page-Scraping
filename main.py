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
        u = employee_link
        url = employee_link
        driver.get(url)
        time.sleep(3)
        scroll_down()
        source = BeautifulSoup(driver.page_source, "html.parser")

        info = source.find('div', class_='mt2 relative')
        name = info.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip()
        title = info.find('div', class_='text-body-medium break-words').get_text().lstrip().strip()
        location = info.find('span', class_='text-body-small inline t-black--light break-words').get_text().strip()

        try:
            company = info.find('span', class_='pv-text-details__right-panel-item-text hoverable-link-text break-words text'
                                               '-body-small t-black').get_text().strip()

        except:
            pass

        url = driver.current_url + '/details/experience/'
        driver.get(url)
        time.sleep(4)
        source = BeautifulSoup(driver.page_source, "html.parser")
        time.sleep(1)
        exp = source.find_all('li',
                              class_='pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
        row = []
        for e in exp:
            row.append(e.getText().split('\n'))
        CurrentCompanyTitle = 'Nil'
        CurrentCompanyName = 'Nil'
        PastCompanyTitle = 'Nil'
        PastCompanyName = 'Nil'
        new_list = []
        for i in row:
            b = [x[:len(x) // 2] for x in i if x != '' and x != ' ']
            new_list.append(b)

        for i in new_list:
            if i[0][-4:] == "logo":
                i.pop(0)
        # for i in new_list:
        #     print(i)
        # print("----------------------")

        c = 1
        for i in new_list:
            if c <= 2:
                if i[2][-4:] == " mos" or i[2][-2:] == "mo" or i[2][-3:] == "yrs":
                    if c == 1:
                        c += 1
                        CurrentCompanyTitle = i[0]
                        if i[1][-9:] == "Full-time":
                            CurrentCompanyName = i[1][:-12]
                        else:
                            CurrentCompanyName = i[1]
                    elif c == 2:
                        c += 1
                        PastCompanyTitle = i[0]
                        if i[1][-9:] == "Full-time":
                            PastCompanyName = i[1][:-12]
                        else:
                            PastCompanyName = i[1]
                elif i[1][-4:] == " mos" or i[1][-2:] == "mo" or i[1][-3:] == "yrs":
                    if i[3][-4:] == " mos" or i[3][-2:] == "mo" or i[3][-3:] == "yrs":
                        if c == 1:
                            c += 1
                            CurrentCompanyTitle = i[2]
                            CurrentCompanyName = i[0]
                        elif c == 2:
                            c += 1
                            PastCompanyTitle = i[2]
                            PastCompanyName = i[0]
                    elif i[3] == "Full-time":
                        if c == 1:
                            c += 1
                            CurrentCompanyTitle = i[2]
                            CurrentCompanyName = i[0]
                        elif c == 2:
                            c += 1
                            PastCompanyTitle = i[2]
                            PastCompanyName = i[0]
                    else:
                        if c == 1:
                            c += 1
                            CurrentCompanyTitle = i[3]
                            CurrentCompanyName = i[0]
                        elif c == 2:
                            c += 1
                            PastCompanyTitle = i[3]
                            PastCompanyName = i[0]

            else:
                break

        job_role_list = CurrentCompanyTitle.replace(',', '').replace('-', ' ').replace('.', '').replace('&', '') \
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

        com_list = [num, name, CurrentCompanyTitle, role, location, PastCompanyTitle, PastCompanyName, u, title,
                    company, CurrentCompanyName]
        list_of_list.append(com_list)
        print(count)
    except:
        list_of_list.append([0, 0, 0, 0, 0, 0, 0, 0])
        print("error")


list_of_list = []
with open('link.txt', 'r') as file:
    links = file.readlines()
links_list = [x.strip() for x in links]

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

sign_in()
count = 0
for link in links_list:
    count += 1
    return_profile_info(employee_link=link, count=count)

df = pd.DataFrame(list_of_list, columns=['Hierarchy N0', 'Name', 'Current Company Title', 'Role', 'Location',
    'Past Company Title', 'Past Company Name', 'Url', 'Top Job Title', 'Top Company Name', 'Current Company Name'])
df.to_excel('Linkedin_output.xlsx', index=False)
