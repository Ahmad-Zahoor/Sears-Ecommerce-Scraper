from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
from time import sleep
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
import os
import re

def find_element_attribute(driver_arg, xpath, attribute):
    element = WebDriverWait(driver_arg, 20).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    link = element.get_attribute(attribute)
    return link

def find_element_text(driver_arg, xpath):
    element = WebDriverWait(driver_arg, 20).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    return element.text

def wait_for_element(driver_arg, xpath):
    WebDriverWait(driver_arg, 20).until(
        EC.presence_of_element_located((By.XPATH, xpath)))

def human_clicker_click(driver_arg, xpath):
    element = WebDriverWait(driver_arg, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    element.click()

def human_clicker_click_by_id(driver_arg, id):
    element = WebDriverWait(driver_arg, 20).until(
        EC.presence_of_element_located((By.ID, id)))
    element.click()


def human_clicker_js3(driver_arg, xpath, index):
    element = WebDriverWait(driver_arg, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath)))
    driver_arg.execute_script("arguments[0].click();", element[index])


def human_clicker_js_single_el(driver_arg, xpath):
    element = WebDriverWait(driver_arg, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath)))
    randomIndex = random.randrange(len(element))
    driver_arg.execute_script("arguments[0].click();", element[randomIndex])


def human_typer(driver_arg, xpath, text: str):
    element = WebDriverWait(driver_arg, 20).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    for s in text:
        element.send_keys(s)
        sleep(random.uniform(0.03, 0.08))


def human_clicker_js(driver_arg, xpath):
    element = WebDriverWait(driver_arg, 20).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    driver_arg.execute_script("arguments[0].click();", element)


def random_wait(lower_limit, uper_limit):
    time_wait = random.randint(lower_limit, uper_limit)
    sleep(time_wait)


def send_keys_interval(el, string):
    for char in string:
        el.send_keys(char)
        rand_wait = random.uniform(0.04, 0.1)
        sleep(rand_wait)

def check_exists_by_xpath(driver_arg, xpath):
    try:
        element = WebDriverWait(driver_arg, 3).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    except (NoSuchElementException, TimeoutException):
        return False
    
    except NoSuchWindowException as e:
        return "window"
    return True

#++++++++++++++++++++++++++++++++++++++++++++++++++++Zahoor Ahmad Code Contribution Part++++++++++++++++++++

def maxbid_confirmation(maxbid):
    conform = simpledialog.askstring(title="Confirmation",
                                     prompt=f"Your Maximum Bid is {maxbid} Now write confirm in the Box:")
    if conform == None:
        return None
    elif conform == "" or conform != "confirm":
        messagebox.showerror('Maximum Bid', 'Please Enter Confirm in the Box')
        return maxbid_confirmation(maxbid)
    else:
        return conform


def minbid_confirmation(minbid):
    conform = simpledialog.askstring(title="Confirmation",
                                     prompt=f"Your Minimum Bid is {minbid} Now write confirm in the Box:")
    if conform == None:
        return None
    elif conform == "" or conform != "confirm":
        messagebox.showerror('Minimum Bid', 'Please Enter Confirm in the Box')
        return minbid_confirmation(minbid)
    else:
        return conform

def find_price(driver, price_path):
    try:
        #check_price = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,price_path))).text
        check_price = price_path
        # get_price = check_price.split("")
        if ',' in check_price:
            check_price = check_price.replace(',', '')
     
        first = re.findall("\d+\.\d+", check_price)
        try:
            if first !=[]:
                get_price = first[0]

                return get_price
            else:
                second = re.findall("\d+", check_price)
                get_price = second[0]
                
                return get_price
        except Exception as e:
            print(e)
            return False
            # print("Errr")
    except Exception as e:
        print(e)
        return False
        # att_dict["Price"] = "Null"
        # print("No Price")
def find_categories(driver, category_path):
    try:
        category_text = ""
        category = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, category_path)))
        for li in category:
            text = li.text
            category_text +=text+" >"
            # att_dict["Categories"] = category_text
        return category_text
    except Exception as e:
        return False

