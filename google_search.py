import sys
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class GoogleSearch:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.search_url = 'https://www.google.com'

    def __del__(self):
        self.driver.close()

    def search(self, q):
        self.driver.get(self.search_url)
        if "Google" in self.driver.title:
            input_field = self.driver.find_element_by_name("q")
            input_field.clear()
            input_field.send_keys(q)
            search_btn = self.driver.find_element_by_name("btnK")
            search_btn.click()
            try:
                r = self.driver.find_element_by_id("recaptcha")
            except NoSuchElementException:
                r = None

            while r:
                try:
                    r = self.driver.find_element_by_id("recaptcha")
                    if r:
                        print("Solve recaptcha!")
                        time.sleep(10)
                except NoSuchElementException:
                    r = None
        else:
            print("check search window")

    def get_next(self):
        btn = self.driver.find_elements_by_id("pnnext")

        if btn:
            return btn
        else:
            return None

    def get_from_page(self):
        elements = self.driver.find_elements_by_xpath("//h3[@class='r']")
        result_data = []
        for elem in elements:
            result_data.append(
                {'text': elem.find_element_by_tag_name('a').text,
                 'url': elem.find_element_by_tag_name('a').get_attribute('href')
                 })
        return result_data

    @staticmethod
    def print_result(result_list):
        for i in result_list:
            print("-"*20 + "\n" +
                  "Text: " + i['text'] + "\n" +
                  "URL: " + i['url'])
        print("-" * 20 + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = ""

    result = []
    g = GoogleSearch()
    print("Search query: " + query)
    g.search(query)
    result = result + g.get_from_page()
    next_btn = g.get_next()
    if next_btn:
        while next_btn:
            next_btn[0].click()
            result = result + g.get_from_page()
            next_btn = g.get_next()

    g.print_result(result)
