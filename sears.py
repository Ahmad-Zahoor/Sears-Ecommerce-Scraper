# coding: utf8
from tkinter.filedialog import askopenfile, askopenfilename, askopenfilenames, askdirectory
from importlib.machinery import all_suffixes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from asyncio import sleep
from cProfile import label
# from cgitb import text
import csv
from http import server
from itertools import count
import os
# from pprint import pprint
# from telnetlib import theNULL
from threading import Thread
import tkinter
from turtle import color
from unicodedata import category, numeric
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from subprocess import CREATE_NO_WINDOW
import time
import re
from selenium.common.exceptions import JavascriptException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select
from tkinter import *
from tkinter import messagebox
import pandas as pd
from random import randint
from actions import *
import smtplib
import sys
from datetime import datetime, timedelta
import pytz
import requests
#from PIL import Image, ImageTk
import glob
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.message import EmailMessage
import undetected_chromedriver as uc
import urllib.request
from pathlib import Path
import re
import threading

root = Tk()
root.title("Sears-Products-Data-Software")
#root.iconbitmap("Armand_store.ico")
fram2 = Frame(root)

label6 = Label(fram2, width=55, text="", anchor='w',font=("Helvetica", 10), fg="green")
label6.grid(row=3, column=1, padx=5, pady=5)

running = False

def clock(get_time):
    # pak_date = pytz.timezone("Asia/Karachi")
    # pak_time = datetime.now(pak_date)

    # current_time = pak_time.strftime("%H:%M:%S")
    root.update()
    label6.config(text=get_time)
    label6.after(1000)

def call(getind):
    try:
        root.update()
        emptylabel.configure(text = str(getind))
        root.after(1000)
        #return True
    except tkinter.TclError as e:
        root.destroy()

def sears_w(driver,get_main_cat_links,create_path,root,getname):
    
    # Code for Opening main Brands
    for ind_b, brand in enumerate(get_main_cat_links, start=1):
        # if ind_b==3:
        #     break
        if ind_b>0:

            start = time.time()

            brand_link,catid = brand

            driver.get(brand_link)
            sleep(7)

            Brand_products = []

            try:
                brandName = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,"//ul[contains(@class,'product-filter-tags')]//a//span[not(contains(text(),'Brand'))]"))).text
            except Exception as e:
                try:
                    brandName = driver.find_element(By.XPATH,'/html[1]/body[1]/app-root[1]/div[1]/app-plp[1]/section[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/ul[1]/li[1]/a[1]/span[2]').text
                except Exception as e:
                    try:
                        brandName = driver.find_element(By.XPATH,'//span[@class="results-for-keyword"]').text
                        brandName = brandName.split("\"")[1]
                    except Exception as e:
                        print("Brand Name not found")
                        break
            

            if "/" in brandName:
                brandName = brandName.replace("/","")
            
            print(f"Brand {brandName} is in process...")

            # Create Brand Folder

            folderpath = f"{create_path}\{brandName}"

            if not os.path.exists(folderpath):
                os.mkdir(folderpath)

            # Code for Scraping categories data
            try:         
                try:
                    filpathf = f"{create_path}\{brandName}_links.csv"
                    # print(filpathf)

                    if not os.path.exists(filpathf):

                        with open(filpathf, 'a', newline='',encoding="utf-8") as output:

                            writer = csv.writer(output)

                            counter = 1

                            all_links = []

                            while(True):
                                sleep(2)
                                
                                try:
                                    gridlist = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"product-box")]/app-product-card/div/a')))
                                    for ind, val in enumerate(gridlist, start=1):
                                        get_link_val = val.get_attribute('href')
                                        # print(get_link_val)
                                        if get_link_val not in all_links:
                                            get_new_data = [get_link_val]
                                            writer.writerow(get_new_data)
                                            all_links.append(get_link_val)
                                    
                                    check_veiw_more_button = check_exists_by_xpath(driver,'//button[text()="Load More"]')

                                    if check_veiw_more_button:
                                        try:
                                            click_load_button = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//button[text()="Load More"]')))
                                            click_load_button.click()
                                            sleep(3)
                                        except Exception as e:
                                            try:
                                                click_load_button = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//button[text()="Load More"]')))
                                                driver.execute_script("arguments[0].click();",click_load_button)
                                                sleep(3)
                                            except Exception as e:
                                                print("Load Button not found")
                                    
                                    else:
                                        break


                                except TimeoutException as e:
                                    print(e)
                                
                                try:
                                    check_hm = check_exists_by_xpath(driver,'//p[text()=" Hmmm... "]')
                                    if check_hm:
                                        break
                                except Exception as e:
                                    pass
                                
                                print(f"Page No: {counter} Scraping Completed.")
                                counter +=1

                except TimeoutException as e:
                    print("Error in Path")
                    print(e)
                
                get_all_data = []
                csv_data = pd.read_csv(filpathf, header=None, index_col=0)
                for row in csv_data.index:
                    get_all_data.append(row)
                
                if len(get_all_data)>0:
                    print(f"Brand: {brandName} have {len(get_all_data)} products and is in process...")
                    # Code for Products Data Scraping

                    for ind2, p_link in enumerate(get_all_data, start=1):
                        
                        if ind2 >0:
                        #     break
                        # else:

                            driver.get(p_link)
                            sleep(5)

                            att_dict = {}
                            
                            # Get Product Name
                            try:
                                title = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="product-right"]/h1[contains(@class,"h2-ui-specs")]'))).text
                                # get_product_name
                            except Exception as e:
                                print("Product Title path not found")
                                    # break
                            
                            # product_url = p_link
                            
                            # Code for Price

                            get_item_price = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//div[@class="product-right"]//span[contains(@class,"pricing-sale-ui")]'))).text if check_exists_by_xpath(driver,'//div[@class="product-right"]//span[contains(@class,"pricing-sale-ui")]') else "Null"

                            check_price = find_price(driver,get_item_price)

                            if check_price:
                                sears_sale_price = check_price
                            else:
                                sears_sale_price = "Null"
                                print("Price path not found")
                            
                            get_cross_price = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//div[@class="product-right"]//del[starts-with(@class,"pricing-crossed-ui")]/span'))).text if check_exists_by_xpath(driver,'//div[@class="product-right"]//del[starts-with(@class,"pricing-crossed-ui")]/span') else "Null"

                            check_regular_price = find_price(driver,get_cross_price)

                            if check_regular_price:
                                sears_regular_price = check_regular_price
                            else:
                                sears_regular_price = "Null"
                                print("Regular price path not found")

                                
                            
                            #att_dict["Brand_Name"] = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,Brand_Name))).text if check_exists_by_xpath(driver,Brand_Name) else "Null"
                            

                            # Code for Categories
                            check_category = find_categories(driver, '//nav[@aria-label="breadcrumb"]/ol/li/a[not(text()="Home")]')

                            if check_category:
                                categories = check_category[:-1] + ''
                            else:
                                print("Category path not found")
                                categories = "Null"
                            
                            #//div[@id="product-overview"]/h2

                            # Get Short Description
                            try:
                                short_description = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//p[contains(@class,"handle-Short-description-tags")]'))).text
                            except Exception as e:
                                short_description = "Null"
                                print("Product Short Description not found")
                            
                            long_description = ""
                            
                            # Code for Long Description
                            check_veiw_more_btn = check_exists_by_xpath(driver,'//p[contains(@class,"view-more-descripton-btn")]/b')
                            if check_veiw_more_btn:
                                try:
                                    click_view_more_button = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,'//p[contains(@class,"view-more-descripton-btn")]/b')))
                                    click_view_more_button.click()
                                    sleep(1)
                                except Exception as e:
                                    try:
                                        click_view_more_button = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,'//p[contains(@class,"view-more-descripton-btn")]/b')))
                                        driver.execute_script("arguments[0].click();",click_view_more_button)
                                        sleep(2)
                                    except Exception as e:
                                        print("Description veiew more button not found")
                                
                            

                                try:
                                    long_description = short_description
                                    get_product = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//p[contains(@class,"handle-long-description-tags")]')))
                                    get_long_description= get_product.text
                                    long_description += '\n' + get_long_description            
                                    
                                except Exception as e:
                                    long_description = "Null"
                                    print("Product Long Discription Path not found")
                            
                            else:
                                long_description = short_description

                            
                            # Code for Product Specifications

                            check_specification_button = check_exists_by_xpath(driver,'//section[contains(@class,"tab-product")]//ul[@role="tablist"]/li/button[text()="Specifications"]')

                            if check_specification_button:
                                try:
                                    click_specification_button = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,'//section[contains(@class,"tab-product")]//ul[@role="tablist"]/li/button[text()="Specifications"]')))
                                    click_specification_button.click()
                                    sleep(1)
                                except Exception as e:
                                    try:
                                        click_specification_button = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,'//section[contains(@class,"tab-product")]//ul[@role="tablist"]/li/button[text()="Specifications"]')))
                                        driver.execute_script("arguments[0].click();",click_specification_button)
                                        sleep(2)
                                    except Exception as e:
                                        print("Description veiew more button not found")
                                try:
                                    item = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Item#")]'))).text
                                    item_number = item.split(":")[1].strip()
                                except Exception as e:
                                    item_number = "Null"
                                    print("Item not found")
                                
                                # Code for Main SKU Start
                                try:
                                    modeln = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Model #")]'))).text
                                    main_sku = modeln.split(":")[1].strip()
                                    att_dict["main_sku"] = main_sku
                                except Exception as e:
                                    att_dict["main_sku"] = "Null"
                                    print("main_sku not found")
                                # Code for Main SKU END

                                
                                att_dict["variation_sku"] = main_sku
                                att_dict["Product URL"] = p_link
                                att_dict["Item"] = item_number

                                #//div[@class="tab-content"]/div/ul                                
                                # check_all_headers = check_exists_by_xpath(driver,'//ul//h5')

                                # if check_all_headers:
                                    
                                #     try:
                                #         all_headers_names = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH,'//ul//h5')))

                                #         for header_ind, header_val in enumerate(all_headers_names, start=1):
                                #             get_h_name = header_val.text

                                #             get_all_headers = []

                                #             try:
                                #                 headers_names = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH,'//h5[contains(text(),"'+str(get_h_name)+'")]//../following-sibling::ul/li/div/div[1]')))

                                #                 for header_name_ind, header_name_val in enumerate(headers_names, start=1):
                                #                     get_hname = header_name_val.text
                                #                     att_dict[get_hname] = driver.find_element(By.XPATH,'//h5[contains(text(),"'+str(get_h_name)+'")]//../following-sibling::ul/li/div/div[text()="'+str(get_hname)+'"]/following-sibling::div').text
                                #             except Exception as e:
                                #                 print(f"Specification not found of {get_h_name}")
                                        
                                #         print(att_dict)
                                #     except Exception as e:
                                #         print("There are some issue in header names")
                                
                                # else:
                                #     print("Headers not found")
                                
                                # print(att_dict)
                            else:
                                print("Specification Not found")
                                break
                            
                             
                            att_dict['type'] = 'simple'
                            att_dict['product_is_main'] = 'Main'
                            att_dict['title'] = title
                            att_dict['short_description'] = short_description
                            att_dict['long_description'] = long_description
                            att_dict['categories'] = categories
                            att_dict['category_ids'] = catid
                            att_dict['tags'] = ""
                            att_dict['attribute_id'] = ""
                            att_dict['attribute'] = ""
                            att_dict['option'] = ""





                            
                            
                            
                            # Code for Images
                            try:
                                check_img_path = check_exists_by_xpath(driver, '(//div[contains(@class,"owl-carousel")])[2]/div/owl-stage//img[@alt="product image"]')
                                if check_img_path:
                                    all_images = ""
                                    get_all_images = driver.find_elements(By.XPATH,'(//div[contains(@class,"owl-carousel")])[2]/div/owl-stage//img[@alt="product image"]')

                                    for ind5, imgv in enumerate(get_all_images, start=1):
                                        try:
                                            imgv.click()
                                            sleep(1)
                                        except Exception as e:
                                            try:
                                                driver.execute_script("arguments[0].click();",imgv)
                                                sleep(1)
                                            except Exception as e:
                                                print("Image not found")

                                        try:
                                            single_image = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,'(//div[contains(@class,"owl-carousel")])[1]//div[contains(@class,"owl-item") and contains(@class,"active")]/div/img'))).get_attribute("src")
                                            all_images += single_image +","
                                            # print("Image Link: ", single_image)
                                        except Exception as e:
                                            print("Image path not found")
                                    att_dict["Images"] = all_images[:-1] + ''
                                    
                                else:
                                    try:
                                        single_image = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'(//div[contains(@class,"owl-carousel")])[1]//div[contains(@class,"owl-item") and contains(@class,"active")]/div/img'))).get_attribute("src")
                                        att_dict["Images"] = single_image
                                        # print("Image Link: ", single_image)
                                    except Exception as e:
                                        print("Image path not found")
                                    
                            except Exception as e:
                                print("Products Images paths not found")
                            
                            att_dict['sears_regular_price'] = sears_regular_price
                            att_dict['sears_sale_price'] = sears_sale_price
                            att_dict['specifications'] = ""
                        
                            
                            
                            if att_dict not in Brand_products:
                                Brand_products.append(att_dict)
                            
                                print("Product No: "+str(ind2) + " Link: " + p_link)

                                data_filpathf =f"{folderpath}\{brandName}"+".csv"

                                if not os.path.exists(data_filpathf):
                                    
                                    df = pd.DataFrame(Brand_products)

                                    df.to_csv(data_filpathf, index=False, encoding='utf-8')
                                
                                else:
                                    # csv_data = pd.read_csv("hello.csv").drop_duplicates(inplace=True)

                                    data = pd.read_csv(data_filpathf)
                                    # data.drop_duplicates(inplace=True)
                                    # df1=data
                                    new_df = pd.DataFrame(Brand_products)
                                    concatdata = pd.concat([data,new_df],ignore_index=True)
                                    concatdata.drop_duplicates(subset=["Product URL"],inplace=True)
                                    concatdata.to_csv(data_filpathf,index=False)

                                    call(ind2)

                else:
                    print("Products are not found")
                    break
                    
    
                            
            except Exception as e:
                print("Issue in Scraping Categories List")
                print(e)
            
            # call(str(ind2))

            stop = time.time()
            duration = stop-start
            my_time = time.strftime('%H:%M:%S', time.localtime(duration))
            clock(my_time)
            
            #print(f"Brand {brandName} have {len(Brand_products)} products")




        
    try:
        driver.close()
    except (WebDriverException,NoSuchWindowException) as e:
        pass
    

def stop_w(driver):

    get_val = messagebox.askquestion("Exit", "Do you want to close the program",icon = 'warning')
    try:
        if get_val=='yes':
            root.destroy()
            driver.close()
        else:
            pass
    except (NoSuchWindowException,WebDriverException) as e:
        pass

def close_window():

    global running

    get_val = messagebox.askquestion("Exit", "Do you want to close the program",icon = 'warning')

    try:
        if get_val=='yes' and running:
            root.destroy()
            running.close()
        elif get_val=='yes':
            root.destroy()
    except (WebDriverException,NoSuchWindowException) as e:
        pass


def startBot(ents, root):

    global running

    b1.config(state="disabled")
    
    # startIndex    = ents['Start Index'].get()
    get_file   = ents['Add files'].get()
    get_dir = ents['Output folder'].get()
    
    if get_file=="":
        messagebox.showerror('Add files', "Pleas Enter File Name")
        b1.config(state="normal")
    
    elif get_file.isnumeric()==True:
        messagebox.showerror('Add files', "Pleas Enter correct file name")
        b1.config(state="normal")
    elif os.path.exists(get_file)==False:
        messagebox.showerror('Add files', "File not found in the direcotry")
        b1.config(state="normal")
    
    elif get_dir=="":
        messagebox.showerror('Folder', "Pleas Select Output Folder")
        b1.config(state="normal")
    
    elif get_dir.isnumeric()==True:
        messagebox.showerror('Folder', "Pleas Enter Correct output path")
        b1.config(state="normal")
    elif os.path.exists(get_file)==False:
        messagebox.showerror('Folder', "Folder path not found")
        b1.config(state="normal")
    
    else:
        # startIndex = int(ents['Start Index'].get())

        # if startIndex <=0:
        #     messagebox.showerror('Start Index', "Pleas Enter greater then 0 Number")
        #     b1.config(state="normal")
        
        # else:
        #     startIndex = int(ents['Start Index'].get())

        name, extensionf = os.path.splitext(get_file)

        data = []

        if extensionf == '.xlsx':
            excel_data = pd.read_excel(get_file, header=None, index_col=[0,1])
            
            for row in excel_data.index:
                if row not in data:
                    data.append(row)


        elif extensionf == '.txt':
            csv_data = pd.read_csv(get_file, header=None, index_col=0)
            for row in csv_data.index:
                if row not in data:
                    split_data = tuple(row.split(" "))
                    # print(split_data)
                    # sentence = ' '.join(row.split())
                    data.append(split_data)

        else:
            csv_data = pd.read_csv(get_file, header=None, index_col=[0,1],low_memory = False)
            for row in csv_data.index:
                if row not in data:
                    data.append(row)

            

        print("Total Brands are: ")
        print(len(data))
        sleep(1)


        #driver = uc.Chrome(use_subprocess=True,service_creationflags=CREATE_NO_WINDOW)
        driver = uc.Chrome(use_subprocess=True)
        driver.maximize_window()
        time.sleep(5)

        # chrome_options = Options()
        # chrome_options.add_experimental_option("debuggerAddress","localhost:9014")
        # service = Service(executable_path=ChromeDriverManager().install())
        # driver = webdriver.Chrome(service=service,options=chrome_options)
        # #service.creationflags = CREATE_NO_WINDOW
        # driver = webdriver.Chrome(executable_path=r"F:\Furniture\chromedriver.exe",options=chrome_options)
        # driver.maximize_window()
        # sleep(2)

        running = driver

        b1.grid_forget()
        b2 = Button(fram2, text='Stop', command=lambda: stop_w(driver)) #command=root.destroy
        b2.grid(row=4, column=0, padx=5, pady=5)
        
        sears_w(driver,data,get_dir,root,name)



def open_file(get_field):
    #os.getcwd()
    # downloads_path = str(Path.home() / "Downloads")
    current_dir = os.getcwd()
    fileobj = askopenfilename(initialdir=current_dir,title="Open File", filetypes=[('Xlsx Files', '*.xlsx'),('CSV Files', '*.csv'),('Text Files','*.txt')])
    
    if fileobj:
        get_field.set(fileobj)

def open_dir(get_dir):
    # downloads_path = str(Path.home() / "Downloads")
    filedir = askdirectory(initialdir=os.getcwd(),title="Select Folder")
    if filedir:
        get_dir.set(filedir)


def makeform(root, fields):
    
    all_ents = {}

    for field in fields:
        fram1 = Frame(root)
        if field=="Add files":
            label1 = Label(fram1, width=15, text=field + " :", anchor='w')
            label1.pack(side=LEFT, padx=5, pady=5)
            my_str = StringVar()
            ent = Entry(fram1, width=40, textvariable=my_str)
            ent.insert(0, "")
            browsebtn = Button(fram1, text="Browse",state="normal", command=lambda: open_file(my_str))
            browsebtn.pack(side=RIGHT, padx=5, pady=5)
            ent.pack(side=RIGHT, expand=YES, fill=X, padx=50, pady=5)
            fram1.pack(side=TOP, fill=X, padx=5, pady=5)
            all_ents[field] = ent
        elif field=="Output folder":
            label1 = Label(fram1, width=15, text=field + " :", anchor='w')
            label1.pack(side=LEFT, padx=5, pady=5)
            my_dir = StringVar()
            ent = Entry(fram1, width=40, textvariable=my_dir)
            ent.insert(0, "")
            browsebtn = Button(fram1, text="Browse",state="normal", command=lambda: open_dir(my_dir))
            browsebtn.pack(side=RIGHT, padx=5, pady=5)
            ent.pack(side=RIGHT, expand=YES, fill=X, padx=50, pady=5)
            fram1.pack(side=TOP, fill=X, padx=5, pady=5)
            all_ents[field] = ent
        else:
            label1 = Label(fram1, width=15, text=field + " :", anchor='w')
            ent = Entry(fram1, width=40)
            ent.insert(0, "")
            fram1.pack(side=TOP, fill=X, padx=5, pady=5)
            label1.pack(side=LEFT, padx=5, pady=5)
            ent.pack(side=RIGHT, expand=YES, fill=X, padx=50, pady=5)
            all_ents[field] = ent

        
    return all_ents


fields = (["Add files","Output folder"])

# root = Tk()

entries = makeform(root, fields)


label2 = Label(fram2, width=10, text="Start Counter:", anchor='w')
label2.grid(row=1, column=0, padx=5, pady=5)

emptylabel = Label(fram2, width=10)
emptylabel.grid(row=1, column=1, padx=10, pady=5)

# label3 = Label(fram2, width=10, text="Note:", anchor='w', foreground='red')
# label3.grid(row=2, column=0, padx=5, pady=5)

# label4 = Label(fram2, width=55, text="After You Hit the start button it will start after minimum 50 seconds", anchor='w')
# label4.grid(row=2, column=1, padx=5, pady=5)

label5 = Label(fram2, width=10, text="Current Time:", anchor='w')
label5.grid(row=3, column=0, padx=5, pady=5)



# threading.Thread(target=clock()).start()

fram2.pack(side=BOTTOM, padx=5, pady=5)

#command=lambda: threading.Thread(target=run_weekly, args=(parent,), daemon=True).start()

b1 = Button(fram2, text='Start',state="normal", command=lambda: threading.Thread(target=startBot, args=(entries,  root,)).start()) #, daemon=True

#b1 = Button(fram2, text='Start', command=lambda: startBot(entries,  root))
b1.grid(row=4, column=0, padx=5, pady=5)

# b2 = Button(fram2, text='Stop', command=root.destroy)
# b2.grid(row=4, column=1, padx=5, pady=5)

root.protocol("WM_DELETE_WINDOW",close_window)
root.mainloop()