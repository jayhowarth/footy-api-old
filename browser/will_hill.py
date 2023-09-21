import re
import time
import asyncio
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs
# import pytest

from playwright.sync_api import Page, expect, Playwright, sync_playwright

def login(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False, slow_mo=50)
    context = browser.new_context()
    page = browser.new_page()

    page.goto('https://sports.williamhill.com/betting/en-gb')
    page.locator('button:has-text("Login")').click()
    time.sleep(2)
    page.locator('input[aria-label="Username input"]').fill('sh0ck3r')
    page.locator('input[aria-label="Password input"]').fill('AR53hole')
    # page.get_by_role('button').get_by_text('Login').click()
    # page.locator('//input[@value="Login"]').click()
    time.sleep(2)
    page.locator('button:has-text("Log In")').click()
    time.sleep(4)

def get_football_scores(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True, slow_mo=50)
    context = browser.new_context()
    page = browser.new_page()

    page.goto('https://sports.williamhill.com/betting/en-gb/football/matches/competition/today/match-betting')

    all_items = page.query_selector_all('.sp-o-market')
    all_stuff = []
    for items in all_items:
        x = items.inner_text()

        all_stuff.append(x)
    print(len(all_stuff[3]))
    # print(all_stuff[1])
    # print(all_stuff[2])


def get_soup():
    page = requests.get('https://sports.williamhill.com/betting/en-gb/football/matches/competition/today/match-betting')
    soup = bs(page.content, 'html.parser')
    s = soup.select('.sp-betName')
    print(s)

def get_selenium():
    driver = webdriver.Chrome()
    driver.get('https://sports.williamhill.com/betting/en-gb/football/matches/competition/today/match-betting')
    stages = driver.find_elements('sp-betName')
    print(stages)
    driver.close()



with sync_playwright() as playwright:
    #login(playwright)
    get_football_scores(playwright)


