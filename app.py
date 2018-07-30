from selenium import webdriver
from math import ceil
from professor import Professor
import pickle
import time

chromeOptions = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images': 2, 'disk-cache-size': 4096}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chromeOptions)


def load_pages():
    url = "http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+California+Berkeley&schoolID=1072&queryoption=TEACHER"
    driver.get(url)
    pages, profs_loaded = 1, 20
    total_professors = int(driver.find_element_by_class_name("professor-count").text)
    total_pages = ceil(total_professors / 20)
    print("\nLoading pages\n")
    while profs_loaded < total_professors:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(.4)
        load_more_button = driver.find_element_by_class_name("progressbtnwrap")
        time.sleep(.4)
        driver.execute_script("arguments[0].click();", load_more_button)
        pages += 1
        profs_loaded += 20
        print(str(pages) + "/" + str(total_pages) + " pages loaded: " + str(round(pages / total_pages * 100, 1)) + "%")
        time.sleep(.4)


def get_professor_ids():
    print("Extracting professor ids...\n")
    elements = driver.find_elements_by_class_name("remove-this-button")
    return [el.get_attribute("data-id") for el in elements]


def write_professor_ids_to_file(lst):
    print("Writing " + str(len(lst)) + " professor ids to output.txt\n")
    with open('output.txt', 'w') as file:
        for i in lst:
            file.write(i+"\n")


def get_professor_ids_from_file():
    print("Getting professor ids from output.txt\n")
    with open('output.txt', 'r') as file:
        return [line.rstrip('\n') for line in file]


def extract_professor_data(professor_ids):
    num_profs = len(professor_ids)
    print("Extracting " + str(num_profs) + " professors' data... (This will take a while)\n")
    t = 0
    professor_objs, failed_extractions = [], []
    for count, id in enumerate(professor_ids, 1):
        print(str(count) + "/" + str(num_profs) + " | " + str(round(count / num_profs * 100, 2)) + "%")
        t+=1
        if t == 10:
            break
        driver.get("http://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(id))
        if "AddRating" in driver.current_url:
            try:
                name = driver.find_element_by_class_name("name").text
                name_id = (name.split(" ")[1] + " " + name[0]).upper()
                professor = Professor(name=name, name_id=name_id, id=id, num_ratings=0)
                professor_objs.append(professor)
            except:
                failed_extractions.append(id)
            continue

        comments = []
        elements = driver.find_elements_by_tag_name("tr")
        for el in elements:
            try:
                comments.append(el.find_element_by_tag_name("p").text)
            except:
                continue
        try:
            last_name = driver.find_element_by_class_name("plname").text
            first_name = driver.find_element_by_class_name("pfname").text
            name_id = (last_name + " " + first_name[0]).upper()
            num_ratings = driver.find_element_by_css_selector("div.table-toggle.rating-count.active").text.split(" ")[0]
            rating = driver.find_element_by_css_selector(".breakdown-container.quality").find_element_by_class_name(
                "grade").text
            difficulty = driver.find_element_by_css_selector(
                ".breakdown-section.difficulty").find_element_by_class_name("grade").text
            tags = [e.text.split(" (")[0] for e in driver.find_elements_by_class_name('tag-box-choosetags')[0:3]]
            professor = Professor(name=first_name + " " + last_name, name_id=name_id, id=id, num_ratings=num_ratings,
                                  rating=rating, difficulty=difficulty, tags=tags, comments=comments)
            professor_objs.append(professor)
        except:
            failed_extractions.append(id)
            continue
    if failed_extractions:
        print("\nIDs of failed professor data extractions:")
        print(failed_extractions)

    # for o in obj:
    #     print()
    #     print("Name: ", o.name)
    #     print("Name ID: ", o.name_id)
    #     print("id: ", o.id)
    #     print("Num ratings: ", o.num_ratings)
    #     print("Rating: ", o.rating)
    #     print("Difficulty: ", o.difficulty)
    #     print("Tags: ", o.tags)
    #     print("Comments: ", o.comments[:3])
    return professor_objs


def write_professor_objs_to_file(professor_objs):
    print("Writing professor objects to pickled_professors.pickle\n")
    with open("pickled_professors.pickle", "wb") as file:
        for professor in professor_objs:
            pickle.dump(professor,  file, pickle.HIGHEST_PROTOCOL)


def get_professor_obs_from_file():
    print("Getting professor objects to pickled_professors.pickle\n")
    professor_objs = []
    with open("pickled_professors.pickle", "rb") as file:
        while True:
            try:
                professor_objs.append(pickle.load(file))
            except EOFError:
                break
    return professor_objs

if __name__ == '__main__':
    # load_pages()
    # professor_ids = get_professor_ids()
    # write_professor_ids_to_file(professor_ids)
    professor_ids = get_professor_ids_from_file()
    professor_objs = extract_professor_data(professor_ids)
    # write_professor_objs_to_file(professor_objs)
    # professor_objs = get_professor_obs_from_file()
    driver.quit()


#TODO might not be 3 tags,
#TODO at end remove reading and writing files for some methods and just have them as utility methods