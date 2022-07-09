import os.path
from bs4 import BeautifulSoup as Bs
import requests
import re
import pyinputplus
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable()


# TODO: Get the soup object
def get_content(picture_theme, pic_size):
    """
    the function requests the content of the page according to the theme
    returns a list of tuples [(link, name)]
    """
    url = "https://unsplash.com/s/photos/"
    response = requests.get(url + picture_theme)
    soup = Bs(response.text, 'html.parser')
    soup_result = soup.find_all('img', class_='YVj9w')
    content_list = []
    for s in soup_result:
        try:
            content_list.append(tuple(needed_picture_size(s, pic_size=pic_size)))
        except Exception as ex:
            logging.info(f"Exception was raised: {ex}")
            pass
    logging.info(content_list)
    return content_list


# TODO: Get the links and the names of the pictures
def needed_picture_size(string, pic_size='100w'):
    """
    the function searches for the links and "alt" names of the FREE pictures and returns them
    """
    needed_size = re.search(
        rf"(?P<url>https?://images\.unsplash\.com/photo-[^\s]+)({size_dictionary[pic_size]})", str(string))
    if bool(needed_size) is True:
        link = needed_size.group(0).split()[0]
        name = str(string).split('"')[1]
        logging.info(link, name)
        return link, name


# TODO: create the folder to download
def make_directory(picture_theme, basic_dir='D:\\pictures'):
    """makes the folder named by the theme the user printed"""
    path = os.path.join(basic_dir, picture_theme)
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    logging.info(path)
    return path


# TODO: write the pics to the directory 'D:\pictures' in the folder by the theme chosen
def writing_to_the_file(path, photo_links):
    """writes the content to the created directory"""
    print("Downloading...")

    counter = 0
    for picture in photo_links:
        url, name = picture
        logging.info(name)
        with open(f"{path}\\{name}.jpg", 'wb') as file:
            result = requests.get(url)
            # noinspection PyBroadException
            try:
                file.write(result.content)
                counter += 1
            except Exception:
                print(f"Error: '{name}' file can not be downloaded")
    # tells how many files have been downloaded
    print(f"{counter} files downloaded")
    # tells how many files in the directory where the files are saved
    print(
        f"{len([entry for entry in os.listdir(path) if os.path.isfile(os.path.join(path, entry))])} files are in folder '{path}'")
    print('The program has finished')


# TODO: Input on the theme of the pics, their size, quantity to download
if __name__ == "__main__":
    # the user chooses the theme
    theme = pyinputplus.inputStr("Enter the theme of the pictures to download:\n").lower().strip()
    print("Which size of images would you like to download?")

    # the user chooses the size (it can be customized before running the code)
    size = pyinputplus.inputMenu(['large', 'regular', 'small']).lower()

    # a dictionary of sizes to parse the necessary size
    size_dictionary = {'large': " 2400w", 'regular': " 1000w", 'small': " 100w"}
    content_list = get_content(theme, size)
    logging.info(len(content_list), *content_list)

    # the user enters the quantity of pictures to download
    quantity = pyinputplus.inputNum(min=1, max=len(content_list), prompt=f"How many pictures do you need? "
                                                                         f"({len(content_list)} maximum)\n")
    array_pictures = content_list[:quantity]
    writing_to_the_file(make_directory(theme, basic_dir='D:\\pictures'), array_pictures)
