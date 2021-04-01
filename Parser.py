from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import xlsxwriter


class Parser(object):
    """
    The class represents WEB Parser, using ChromeDriver.
    So if you have a list of pages, form where you need to grab some data -
    this parser will grab all the data you need automatically
    and save you a lot of your time and nerve cells! =)

    Args:
        chromedriver:            Path to chromedriver binary.
        deserialize_links_from:  Path to file_with_links.txt to be parsed.
        serialize_data_to:       Path to file.xlsx where parsed data will be saved.
    """

    def __init__(self, chromedriver, deserialize_links_from, serialize_data_to):
        self.chromedriver = chromedriver
        self.deserialize_links_from = deserialize_links_from
        self.serialize_data_to = serialize_data_to

    def __get_locator_data(self, data_type, locator):
        """
        This method gets data from web locators on the page
        """
        # If obtained locator exist - this construction returns count of elements it contains
        try:
            elements_number = len(self.driver.find_elements_by_xpath(locator))
        except NoSuchElementException:
            message = f'Element {locator} was not found'
            print(message)
            elements_number = 1

        # If the resulting locator contains several elements - read them in turn and append results to the list.
        if elements_number > 1:
            elements_list = []
            for i in range(elements_number):
                # For different data types use different methods to get info from locators
                try:
                    if data_type == 'text':
                        element = WebDriverWait(self.driver, 20).until(
                                ec.presence_of_element_located((By.XPATH, locator + f"[{i+1}]"))).text
                    elif data_type == 'href':
                        element = self.driver.find_element_by_xpath(locator + f"[{i+1}]").get_attribute('href')
                    elif data_type == 'src':
                        element = self.driver.find_element_by_xpath(locator + f"[{i+1}]").get_attribute('src')
                # If Timeout or No Such Element Exception reised - show locator and write '' instead of that element
                except (NoSuchElementException, TimeoutException):
                    message = f'Element {locator + f"[{i+1}]"} was not found'
                    print(message)
                    element = ''

                # Append element's value to the list
                elements_list.append(element)

            # Return list of element's values
            return elements_list
        else:
            # If the resulting locator contains one element - read it's value and return it.
            try:
                # For different data types use different methods to get info from locators
                if data_type == 'text':
                    element = WebDriverWait(self.driver, 20).until(
                        ec.presence_of_element_located((By.XPATH, locator))).text
                elif data_type == 'href':
                    element = self.driver.find_element_by_xpath(locator).get_attribute('href')
                elif data_type == 'src':
                    element = self.driver.find_element_by_xpath(locator).get_attribute('src')
            # If Timeout or No Such Element Exception reised - show locator and write '' instead of that element
            except (NoSuchElementException, TimeoutException):
                message = f'Element {locator} was not found'
                print(message)
                element = ''

            # Return element's value
            return element

    @property
    def deserialize_links_from_txt(self):
        """
        This method deserializes all links from file.txt
        """
        # Parse .txt file for URL links
        with open(self.deserialize_links_from) as f:
            links_list = f.readlines()

        # Remove whitespace characters like `\n` at the end of each line and return them as a list
        return [x.strip() for x in links_list]

    def parse_data(self, links_list):
        """
        This method:
        1. Opens each link from the file.txt in Google Chrome using ChromeDriver.
        2. Then parses (collects) the necessary data from the page.
        3. Closes opened page.
        4. Prepares data for storage.

        Once all the data is received, this data is written to the file.xslx,
        the file saves and the program terminates.
        """
        # Make Google Chrome not wait till the page is fully loaded,
        # and proceed execution if all the required elements are already present and located on the page
        self.capa = DesiredCapabilities.CHROME
        self.capa["pageLoadStrategy"] = "none"

        # Open XLSX file to write data into it,
        # set worksheet name,
        # enable text wrapping and
        # set text align parameters
        self.workbook = xlsxwriter.Workbook(self.serialize_data_to)
        self.worksheet = self.workbook.add_worksheet('Films')
        self.data_format = self.workbook.add_format({'text_wrap': True})
        self.data_format.set_align('top')

        # Parse data
        count = 0
        for page_link in links_list:
            # ReInitialize new ChromeDriver session for every loop,
            # because we kill previouse ChromeDriver session at the end of every loop
            self.driver = webdriver.Chrome(self.chromedriver, desired_capabilities=self.capa)

            # Open page
            self.driver.get(page_link)

            # Get all the data from the page, that interests us
            film_name_ua =   Parser.__get_locator_data(self, 'text', '//*[@id="dle-content"]/div/div/div/h1/span')
            film =           Parser.__get_locator_data(
                self, 'src',  '/html/body/div[1]/div[1]/div/div/div[2]/div[2]/div/article/div[2]/div[1]/div[5]/iframe')
            about =          Parser.__get_locator_data(self, 'text', '//*[@id="movie-right"]/div[4]')
            quality =        Parser.__get_locator_data(self, 'text', '//*[@id="movie-left"]/div[4]/div[1]/div[2]')
            year =           Parser.__get_locator_data(self, 'text', '//*[@id="movie-left"]/div[4]/div[2]/div[2]/a')
            country =        Parser.__get_locator_data(self, 'text', '//*[@id="movie-left"]/div[4]/div[3]/div[2]/a')
            genre =          Parser.__get_locator_data(self, 'text', '//*[@id="movie-left"]/div[4]/div[4]/div[2]/a')
            director =       Parser.__get_locator_data(self, 'text', '//*[@id="movie-left"]/div[4]/div[6]/div[2]/a')
            actors =         Parser.__get_locator_data(self, 'text', '//*[@id="movie-left"]/div[4]/div[7]/div[2]/a')
            duration =       Parser.__get_locator_data(self, 'text', '//*[@id="movie-left"]/div[4]/div[8]/div[2]')
            sound_language = Parser.__get_locator_data(self, 'text', '//*[@id="movie-left"]/div[4]/div[9]/div[2]')
            screenshots =    Parser.__get_locator_data(self, 'href', '//*[@id="movie-right"]/div[1]/div[8]/a')

            # List of column titles
            titles = [
                "Film name:       ",
                "Page link:       ",
                "Film:            ",
                "About:           ",
                "Quality:         ",
                "Year:            ",
                "Country:         ",
                "Genre:           ",
                "Director:        ",
                "Actors:          ",
                "Duration:        ",
                "Sound language:  ",
                "Screenshots:     "]

            # Write bold column titles to the XML file if it is 1st loop
            if count == 0:
                print("Writing bold column titles to file.xlsx")
                # Write bold column titles to the file.xlsx
                for col_num, data in enumerate(titles):
                    self.worksheet.write(0, col_num, str(data), self.workbook.add_format({'bold': True}))

            # Print parsed data to the CLI
            print(f"Writing data to file.xlsx about film #{count+1}:")
            print(titles[0], film_name_ua)
            print(titles[1], page_link)
            print(titles[2], film)
            print(titles[3], about)
            print(titles[4], quality)
            print(titles[5], year)
            print(titles[6], country)
            print(titles[7], genre)
            print(titles[8], director)
            print(titles[9], actors)
            print(titles[10], duration)
            print(titles[11], sound_language)
            print(titles[12], screenshots)
            print(" ---------- ---------- ----------")

            # List of all data from the film
            all_film_data = [
                film_name_ua,
                page_link,
                film,
                about,
                quality,
                year,
                country,
                genre,
                director,
                actors,
                duration,
                sound_language,
                screenshots]

            # Write data to the file.xlsx row-by-row
            for col_num, data in enumerate(all_film_data):
                if col_num == 3:
                    self.worksheet.set_column(col_num, col_num, 100)
                elif col_num == 12:
                    self.worksheet.set_column(col_num, col_num, 70)
                else:
                    self.worksheet.set_column(col_num, col_num, 25)

                # Write formatted data to file.xlsx row-by-row
                self.worksheet.write(count+1, col_num, str(data), self.data_format)

            # Loops increment
            count+=1

            # Close ChromeDriver window at the end of every loop
            self.driver.close()

        # Close XLSX file after all parsed data are added
        self.workbook.close()

        # Quit Chrome Driver and finish CLI Parser's execution
        self.driver.quit()
