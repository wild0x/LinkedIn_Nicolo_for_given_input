

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

class linkedIn_detail():
    def __init__(self):
        self.input=""
        self.name=""
        self.college=""
        self.current_company=""
        self.current_position=""
        self.current_year_start_end=""
        self.current_location=""
        self.previous_company=""
        self.previous_position=""
        self.previous_year_start_end=""
        self.previous_location=""
		
		
		
def get_link():
    user_detail_list=[]
    input_link = pd.read_csv('Input_example.txt', quoting = 3,names=['input'])
    for row in input_link.itertuples():
        new_object=linkedIn_detail()
        new_object.input=row[1]
        user_detail_list.append(new_object)
    
    return user_detail_list
	
	
	
	
user_detail_list=get_link()




def get_user_detail(user_detail_list):
    
    #Download and Install the selenium webdriver
    #Give the path in executable_path where you have saved the file
    driver = webdriver.Chrome(executable_path='C:\chromedriver_win32\chromedriver.exe')

    #Open the website
    driver.get("https://www.linkedin.com/")

    #Maximize the window
    driver.maximize_window()

    ##Automation 
    email=driver.find_element_by_xpath('//*[@id="login-email"]')
    email.send_keys("mps24.7uk@gmail.com ") # enter your  linkedIn username 

    password=driver.find_element_by_xpath('//*[@id="login-password"]')  
    password.send_keys(" ")  # enter your linkedIn password

    login=driver.find_element_by_xpath('//*[@id="login-submit"]')
    login.click()
    time.sleep(2)
    

    for l1 in user_detail_list:
        
        driver.get(l1.input)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source,'lxml')
        div_whole_tag=soup.find('div',class_="pv-top-card-section__information mt3 ember-view")
         
        #Extract the name of user    
        l1.name=div_whole_tag.find('h1').text.strip() 
        
        #Extract the latest Education of user
        for latest_Edu in div_whole_tag.find_all('h3')[1:2]:
            l1.college=latest_Edu.text.strip()


            

        time.sleep(6)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4.5);")

        soup1 = BeautifulSoup(driver.page_source, 'lxml')
        ul_experinece=soup1.find('section',{'id':'experience-section'})
        for key,a_tag in enumerate(ul_experinece.find_all('a')):
           
            if key==0:
                
                ##series of try and expect block used to take case of empty field
                #Extract the current position
                try:
                    a=a_tag.find('div',class_='pv-entity__summary-info')
                    l1.current_position=a.find('h3').text
                except:
                    l1.current_position=""
                
                #Extract the current company
                try:                
                    for span_company in a.find('span',string="Company Name").fetchNextSiblings():
                        l1.current_company=span_company.text.lstrip()
                except:
                    l1.current_company=""
                
                #Extract the current year_start_end
                try:
                    for span_date in a.find('span',string="Dates Employed").fetchNextSiblings():
                        l1.current_year_start_end=span_date.text.lstrip()
                except:
                    l1.current_year_start_end=""
                
                #Extract the current location
                try:
                    for span_location in a.find('span',string="Location").fetchNextSiblings():
                        l1.current_location=span_location.text.lstrip()
                except:
                    l1.current_location=""
                
            elif key==1:
                  #Extract the previous position              
                try:
                    a=a_tag.find('div',class_='pv-entity__summary-info')
                    l1.previous_position=a.find('h3').text
                except:
                    l1.previous_position=""

                    #Extract the previous company
                try:
                    for span_company in a.find('span',string="Company Name").fetchNextSiblings():
                        l1.previous_company=span_company.text.lstrip()   
                except:
                    l1.previous_company=""                    
                
                #Extract the previous year_start_end
                try:
                    for span_date in a.find('span',string="Dates Employed").fetchNextSiblings():
                        l1.previous_year_start_end=span_date.text.lstrip()
                except:
                    l1.previous_year_start_end=""
                
                #Extract the previous location
                try:
                    for span_location in a.find('span',string="Location").fetchNextSiblings():
                        l1.previous_location=span_location.text.lstrip()
                except:
                    l1.previous_location=""
                    
        time.sleep(5)
        
    driver.close()
    return l1
	
	
	
	


list1=get_user_detail(user_detail_list)

#Converting the Above Ouput into dataframe
Detail=pd.DataFrame(columns=['name','latest Education','Linkedin link','current company','current position','current year start - year end','current location','previous company','previous position','previous year start - year end','previous location'])



for lw in user_detail_list:
    Detail=Detail.append(pd.Series([lw.name,lw.college,lw.input,lw.current_company,lw.current_position,lw.current_year_start_end,lw.current_location,lw.previous_company,lw.previous_position,lw.previous_year_start_end,lw.previous_location], ['name','latest Education','Linkedin link','current company','current position','current year start - year end','current location','previous company','previous position','previous year start - year end','previous location']), ignore_index=True)


#Converting the dataframe into csv
Detail.to_csv("linkedin_complete_output.csv", index=False)	

