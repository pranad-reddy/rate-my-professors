from selenium import webdriver      
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from math import ceil
import time


url = "http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+California+Berkeley&schoolID=1072&queryoption=TEACHER"

driver = webdriver.Chrome('./chromedriver')
driver.get(url)

pages = 1
profs_loaded = 20
total_professors = int(driver.find_element_by_class_name("professor-count").text)
total_pages = ceil(total_professors / 20)
while profs_loaded < total_professors:
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(.4)
	load_more_button = driver.find_element_by_class_name("progressbtnwrap")
	driver.execute_script("arguments[0].click();", load_more_button)
	pages+=1
	profs_loaded+=20
	print(str(pages) + "/" + str(total_pages) + " pages loaded: " + str(round(pages/total_pages*100, 1)) + "%")
	time.sleep(.4)

# lst = [e.find_element_by_tag_name("a").find_element_by_class_name("remove-this-button").get_attribute("data-id") for e in driver.find_elements_by_xpath("//*[contains(@id, 'my-professor-')]")]
print(sum([int(e.find_element_by_tag_name("a").find_element_by_class_name("name").find_element_by_class_name("info").text.split(' ')[0]) for e in driver.find_elements_by_xpath("//*[contains(@id, 'my-professor-')]")]))

# with open('output.txt', 'w') as file:  # Use file to refer to the file object
# 	for i in lst:
# 		file.write(i+"\n")
# print(len(lst))
driver.quit()

# with open('output.txt', 'r') as file:
# 	lst=[line.rstrip('\n') for line in file]
# print(len(lst))

#wrap everything in try
#dont use xpath