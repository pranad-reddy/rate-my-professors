from selenium import webdriver
from math import ceil
import time
from teacher import Teacher
driver = webdriver.Chrome('./chromedriver')


def load_pages():
    url = "http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+California+Berkeley&schoolID=1072&queryoption=TEACHER"
    driver.get(url)
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


def get_url(id):
    return "http://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(id)

def write_teacher_ratings_to_file(teacher_ids):
    teacher_objs = []

    # for id in teacher_ids:
    id = teacher_ids[0]
    url = get_url(id)
    driver.get(url)
    comments = []
    elements = driver.find_elements_by_tag_name("tr")
    for el in elements:
        try:
            assert(el.find_element_by_tag_name("td").get_attribute("class") == "rating")
            comment = el.find_elements_by_tag_name("td")[2].find_element_by_tag_name("p").text
            comments.append(comment)
        except Exception as e:
            continue
    last_name = driver.find_element_by_class_name("plname").text
    first_name = driver.find_element_by_class_name("pfname").text[:1]
    name = last_name + " " + first_name
    rating = driver.find_element_by_css_selector(".breakdown-container.quality").find_element_by_class_name("grade").text
    difficulty = driver.find_element_by_css_selector(".breakdown-section.difficulty").find_element_by_class_name("grade").text
    teacher = Teacher(name=name, rating=rating, difficulty=difficulty, comments=comments)
    teacher_objs.append(teacher)
    # print("Name: ", teacher_objs[0].name)
    # print("Rating: ", teacher_objs[0].rating)
    # print("Difficulty: ", teacher_objs[0].difficulty)
    # print("Comments: ", len(teacher_objs[0].comments))

    #TODO handle 0 ratings/no difficulty/rating issue
    #TODO get all teacher objects
    #TODO Write to file (pickled)


if __name__ == '__main__':
    # load_pages()
    # teacher_ids = get_teacher_ids()
    # write_teacher_ids_to_file(teacher_ids)
    teacher_ids = get_teacher_ids_from_file()
    write_teacher_ratings_to_file(teacher_ids)
    driver.quit()
    # TODO


#TODO wrap everything in try, put driver.quit in all to save resources
#TODO dont use xpath
