#!/usr/bin/python3
# coding: utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    "(KHTML, like Gecko) Chrome/15.0.87"
)

url = "https://translate.google.com/"
# os.system("taskkill /F phantomjs")


class Translate():
    def __init__(self):
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        self.driver.set_page_load_timeout(10)
        self.connect(url)

    def connect(self, url):
        ok = False
        while ok == False:
            try:
                self.driver.get(url)
                ok = True
                # print("...Connected")
            except BaseException:
                ok = False
                print("Can't connect to:", url, " retrying")
                time.sleep(3)

    def __translate(self, text):
        if text == "":
            return ""
        self.connect(url)
        trys = 0
        textArea = self.driver.find_element_by_id("source")
        textArea.send_keys("")
        textArea.send_keys(text)
        translatebutton = self.driver.find_element_by_id("gt-submit")
        result = ""
        # time.sleep(5)
        while len(result) < 1:
            translatebutton.click()
            result = self.driver.find_element_by_id("result_box").text
            if len(result) < 1:
                trys += 1
                if trys > 1:
                    print("Retrying...", trys)
                self.driver.save_screenshot("Trans.png")
                time.sleep(5)
        textArea.send_keys("")
        self.driver.find_element_by_id("result_box").send_keys("")
        result = result.replace(
            "Unesdoc.unesco.org unesdoc.unesco.org",
            "").replace(
            "....",
            ".")
        return result

    def translate(self, text):
        if len(text) < 3000:
            return self.__translate(text)
        else:
            print("Text too long...")
            listofText = text.split("\n")
            finalresult = ""
            p = 1
            print("Splitting in ", len(listofText))
            for phrase in listofText:
                print("Translating piece: ", p, "/", len(listofText))
                self.driver.save_screenshot("Trans.png")
                finalresult = finalresult + self.__translate(phrase) + "\n"
                p += 1
            return finalresult
