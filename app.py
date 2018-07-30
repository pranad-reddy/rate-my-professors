"""
Module to programatically extract data from all Berkeley professors from ratemyprofessors.com and store it in a database.
Change url in load_pages() to extract professor data from other universities
"""

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
    """
    Loads entire page of Berkeley professors
    """
    url = "http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+California+Berkeley&schoolID=1072&queryoption=TEACHER"
    driver.get(url)
    pages, profs_loaded = 1, 20
    total_profs = int(driver.find_element_by_class_name("professor-count").text)
    total_pages = ceil(total_profs / 20)
    print("\nLoading pages\n")
    while profs_loaded < total_profs:
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
    """
    Extracts professor ids from fully loaded page and returns list of them
    Returns:
        list: ids of all professors
    """
    print("Extracting professor ids...\n")
    elements = driver.find_elements_by_class_name("remove-this-button")
    return [el.get_attribute("data-id") for el in elements]


def write_professor_ids_to_file(prof_ids):
    """
    Writes list of professor ids to file
    Args:
        prof_ids (list): list of professor ids
    """
    print("Writing " + str(len(prof_ids)) + " professor ids to output.txt\n")
    with open('output.txt', 'w') as file:
        for i in prof_ids:
            file.write(i+"\n")


def get_professor_ids_from_file():
    """
    Returns list of professor ids from file
    Returns:
        list: professor ids
    """
    print("Getting professor ids from output.txt\n")
    with open('output.txt', 'r') as file:
        return [line.rstrip('\n') for line in file]


def extract_professor_data(prof_ids):
    """
    For each professor, loads page and extracts name, name_id, top 3 tags, total number of ratings,
    top 20 (max) comments, rating, difficulty. Aggregrates data into professor object and returns list of them
    Args:
        prof_ids (list): professor ids
    Returns:
        prof_objs (list): professor objects containing their data
    Raises:
        Exception if certain data cannot be extracted
    """
    num_profs = len(prof_ids)
    print("Extracting " + str(num_profs) + " professors' data... (This will take a while)\n")
    t = 0
    prof_objs, failed_extractions = [], []
    for count, id in enumerate(prof_ids, 1):
        print(str(count) + "/" + str(num_profs) + " | " + str(round(count / num_profs * 100, 2)) + "%")
        t+=1
        if t == 10:
            break
        driver.get("http://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(id))
        if "AddRating" in driver.current_url:
            try:
                name = driver.find_element_by_class_name("name").text
                name_id = (name.split(" ")[1] + " " + name[0]).upper()
                prof = Professor(name=name, name_id=name_id, id=id, num_ratings=0)
                prof_objs.append(prof)
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
            prof = Professor(name=first_name + " " + last_name, name_id=name_id, id=id, num_ratings=num_ratings,
                                  rating=rating, difficulty=difficulty, tags=tags, comments=comments)
            prof_objs.append(prof)
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
    return prof_objs


def write_prof_objs_to_file(prof_objs):
    """
    Pickles and writes professor objects to file
    Args:
        prof_objs (list): professor objects
    """
    print("Writing professor objects to pickled_profs.pickle\n")
    with open("pickled_profs.pickle", "wb") as file:
        for prof in prof_objs:
            pickle.dump(prof,  file, pickle.HIGHEST_PROTOCOL)


def get_professor_obs_from_file():
    """
    Gets, unpickles, and returns professor objects from file
    Returns:
        prof_objs (list): professor objects
    """
    print("Getting professor objects to pickled_profs.pickle\n")
    prof_objs = []
    with open("pickled_profs.pickle", "rb") as file:
        while True:
            try:
                prof_objs.append(pickle.load(file))
            except EOFError:
                break
    return prof_objs


if __name__ == '__main__':
    # load_pages()
    # prof_ids = get_professor_ids()
    # write_professor_ids_to_file(prof_ids)
    prof_ids = get_professor_ids_from_file()
    prof_objs = extract_professor_data(prof_ids)
    # write_prof_objs_to_file(prof_objs)
    # prof_objs = get_professor_obs_from_file()
    driver.quit()


#TODO might not be 3 tags,
#TODO at end remove reading and writing files for some methods and just have them as utility methods
#TODO add a readme