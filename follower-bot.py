#-*- coding: utf-8 -*-

######################################################################
###  MEDIUM FOLLOWER BOT
###  AUTHOR: Arthur Mello
###  CREATION DATE: 23/01/2020
######################################################################

from selenium import webdriver, common
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import random
from flask import Flask, request, render_template
import os

def bot_function(keyword, email_fb, password_fb):
    # Access Medium
    driver = webdriver.Chrome(ChromeDriverManager().install())
    sleep(2)
    driver.get('https://medium.com/')
    sleep(3)
    try:
        cookie_button = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div/div/span/button')
        cookie_button.click()
    except:
        pass
    link = driver.find_element_by_link_text('Sign in')
    link.click()
    sleep(6)

    # Sign in with Facebook
    link = driver.find_element_by_link_text('Sign in with Facebook')
    link.click()
    sleep(2)
    email = driver.find_element_by_name('email')
    email.send_keys(email_fb)
    password = driver.find_element_by_name('pass')
    password.send_keys(password_fb)
    button_login = driver.find_element_by_name('login')
    button_login.click()
    sleep(3)

    # Search for articles
    driver.get('https://medium.com/search')
    search_bar = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div/div[3]/div[1]/header/form/input'
            )
    search_bar.send_keys(keyword)
    sleep(2)

    # Open first 5 articles
    total_counter = 0
    max_articles = 5
    max_set_clappers = 3

    for i in range(max_articles-1):
        print(i)
        sleep(4)
        articles = driver.find_elements_by_class_name("postArticle-content")
        if len(articles) == 0:
            break
        article = articles[i]
        article.click()
        sleep(4)

        # Get list of clappers
        claps = driver.find_element_by_xpath(
                "/html/body/div/div/div[5]/div/div[1]/div/div[4]/div[1]/div[2]/div/h4/button"
                )
        claps.click()
        sleep(5)

        # Follow first users on the list
        counter = 0
        limit = 20
        
        for i in range(max_set_clappers-1):
            sleep(2)
            follow_button_list = driver.find_elements_by_xpath('//button[text()="Follow"]')
            for button in follow_button_list:
                if button.text == 'Follow':
                    try:
                        sleep(2)
                        button.click()
                    except common.exceptions.ElementClickInterceptedException:
                        driver.execute_script("arguments[0].click();", button)
                    counter += 1
                    sleep(1 + random.random())
                    if counter >= limit:
                        break
            # Show more people who clapped
            try:
                show_claps_button = driver.find_element_by_xpath(
                        '/html/body/div[2]/div/div[1]/div/div[12]/button'
                        )
                sleep(2)
                show_claps_button.click()
            except common.exceptions.StaleElementReferenceException as e:
                print(e)
                sleep(5)
                try:
                    show_claps_button.click()
                except common.exceptions.ElementClickInterceptedException:
                        driver.execute_script("arguments[0].click();", show_claps_button)
                        
            except common.exceptions.ElementClickInterceptedException:
                        driver.execute_script("arguments[0].click();", show_claps_button)
            except:
                driver.execute_script("arguments[0].click();", show_claps_button)
                break
        driver.back()
        total_counter += counter
    print(f'{total_counter} users followed successfully!')
    driver.quit()

# Flask app
TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')

app = Flask(__name__, template_folder=TEMPLATE_DIR,
            static_folder=STATIC_DIR)

@app.route('/')
def my_form():
    app.root_path = os.path.dirname(os.path.abspath(__file__))
    return render_template('basic.html')

@app.route('/', methods=["POST","GET"])
def bot():
    keyword = request.form['keyword']
    email_fb = request.form['email_fb']
    password_fb = request.form['password_fb']
    return bot_function(keyword, email_fb, password_fb)

    
if __name__ == '__main__':
    app.run(debug=True)