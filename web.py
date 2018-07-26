from selenium import webdriver
from math import ceil
import time

driver = webdriver.Chrome('./chromedriver')
url = "http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+California+Berkeley&schoolID=1072&queryoption=TEACHER"
driver.get(url)

def load_pages():
    pages, profs_loaded = 1, 20
    total_professors = int(driver.find_element_by_class_name("professor-count").text)
    total_pages = ceil(total_professors / 20)
    while profs_loaded < total_professors:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        load_more_button = driver.find_element_by_class_name("progressbtnwrap")
        driver.execute_script("arguments[0].click();", load_more_button)
        pages += 1
        profs_loaded += 20
        print(str(pages) + "/" + str(total_pages) + " pages loaded: " + str(round(pages/total_pages*100, 1)) + "%")
        time.sleep(.4)

def get_teacher_ids():
    id_lst = []
    elements = driver.find_elements_by_xpath("//*[contains(@id, 'my-professor-')]")
    for el in elements:
        el_tag = el.find_element_by_tag_name("a")
        remove_button_el = el_tag.find_element_by_class_name("remove-this-button")
        id = remove_button_el.get_attribute("data-id")
        id_lst.append(id)
    return id_lst

    # return [e.find_element_by_tag_name("a").find_element_by_class_name("remove-this-button").get_attribute("data-id")
    #         for e in driver.find_elements_by_xpath("//*[contains(@id, 'my-professor-')]")]
# print(sum([int(e.find_element_by_tag_name("a").find_element_by_class_name("name").find_element_by_class_name("info").text.split(' ')[0]) for e in driver.find_elements_by_xpath("//*[contains(@id, 'my-professor-')]")]))

def write_teacher_ids_to_file(lst):
    with open('output.txt', 'w') as file:
        for i in lst:
            file.write(i+"\n")

def get_teacher_ids_from_file():
    with open('output.txt', 'r') as file:
        return [line.rstrip('\n') for line in file]



if __name__ == '__main__':
    load_pages()
    teacher_ids = get_teacher_ids()
    write_teacher_ids_to_file(teacher_ids)
    teacher_ids = get_teacher_ids_from_file()
    driver.quit()

#TODO wrap everything in try
#TODO dont use xpath