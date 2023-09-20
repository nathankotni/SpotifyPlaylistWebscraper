import installLibraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd


#Author ~ Nathan Kotni


inputType = input("Enter 1 to submit playlist name and description or enter 2 to submit playlist link directly: ")
inputType = str(inputType)
while inputType != '1' and inputType != '2':
    print('Faulty input')
    inputType = input("Inputs can only be 1 or 2. Enter 1 to submit playlist link or enter 2 to submit playlist name and description: ")
    inputType = str(inputType)
if inputType == '2':
    url = input("Enter URL: ")
    url = url.strip()
else:
    playlistName = input("Enter playlist name: ")
    playlistDesc = input("Enter playlist description: ")

    convString = playlistName + ' ' + playlistDesc
    searchString = ''

    for charac in convString:
        if charac == ' ':
            searchString += '%20'
        elif charac == ':':
            searchString += '%3A'
        elif charac == '&':
            searchString += '%26'
        elif charac == '#':
            searchString += '%23'
        elif charac == '@':
            searchString += '%40'
        elif charac == '\\':
            searchString += '/'
        elif charac == '/':
            searchString += '%2F'
        elif charac == ';':
            searchString += '%3B'
        elif charac == '^':
            searchString += '%5E'
        elif charac == '$':
            searchString += '%24'
        elif charac == '`':
            searchString += '%60'
        elif charac == '+':
            searchString += '%2B'
        elif charac == '=':
            searchString += '%3D'
        else:
            searchString += charac

    url = 'https://open.spotify.com/search/' + searchString +'/playlists'

    options = Options()
    options.add_argument('--headless=new')

    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

    driver.get(url)

    time.sleep(2)

    playlistName = playlistName.strip()

    try:
        playlist = driver.find_element(By.XPATH, "//div [contains( text(), '"+ playlistName +"')]")
    except:
        print('Playlist not found. Please run the program again and make sure ' + 
            'to include the complete and accurate playlist name and description' + 
            ' or directly enter a playlist link.')
        exit()
    parent = playlist.find_element(By.XPATH, './..')
    grandparent = playlist.find_element(By.XPATH, './..')
    accountText = grandparent.find_element(By.XPATH, "//span [contains( text(), 'By')]").text

    accountText = accountText.replace('By ', '')
    confirmation = input("Is " + accountText + " the creator of the playlist? (y/n) ")
    confirmation = confirmation.lower()
    while confirmation != 'y' and confirmation != 'n':
        print('Faulty input')
        confirmation = input("Your answer must be y or n, is " + accountText + " the creator of the playlist? (y/n) ")

    if confirmation == 'n':
        print('Please run the program again and make sure to include the complete ' + 
            'and accurate playlist name and description or directly enter a playlist link.')
        exit()

    url = parent.get_attribute("href")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(url)


time.sleep(2)

playlistName = driver.find_element(By.XPATH, "//*[@id='main']/div/div[2]/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/main/div[1]/section/div[1]/div[5]/span[2]/h1").text

playlistList = []


grid = driver.find_element(By.XPATH, "//div [@role='grid']")
numSongs = (int)(grid.get_attribute("aria-rowcount"))

firstSong = driver.find_element(By.XPATH, "//*[@aria-rowindex=1]")
firstSong.click()
actions = ActionChains(driver) 
for _ in range(numSongs):
    actions.send_keys(Keys.DOWN)
    actions.perform()
    time.sleep(0.015)
for _ in range(numSongs):
    actions.send_keys(Keys.UP)
    actions.perform()
    time.sleep(0.015)

numSongs = (int)(grid.get_attribute("aria-rowcount"))
numSongs -= 1

songCounter = 1
for _ in range(numSongs):
    songXPath = "//*[@aria-rowindex='" + str(songCounter + 1) +"']"
    actions.send_keys(Keys.DOWN)
    actions.perform()
    time.sleep(0.01)
    latestSong = driver.find_element(By.XPATH, songXPath)

    entryDict = {}
    while True:
        try:
            nameButton = driver.find_element(By.XPATH, songXPath + "/div/div[1]/div/button")
            break
        except:
            time.sleep(0.3)

    nameAndArtist = nameButton.get_attribute("aria-label")
    nameAndArtist = nameAndArtist[5:]
    name = ''
    artist = ''

    if nameAndArtist.count(' by ') == 1:
        nameAndArtist = nameAndArtist.split(' by ')
        name = nameAndArtist[0]
        artist = nameAndArtist[1]
    else:
        length = nameAndArtist.count(' by ')
        nameAndArtistList = nameAndArtist.split(' by ')
        artist = nameAndArtist[length]
        name = driver.find_element(By.XPATH, songXPath + "/div/div[2]/div/a/div").text


    entryDict['Index'] = songCounter

    entryDict['Name'] = name

    entryDict['Artist(s)'] = artist

    album = driver.find_element(By.XPATH, songXPath + "/div/div[3]/span/a").text
    entryDict['Album'] = album

    songDuration = driver.find_element(By.XPATH, songXPath + "/div/div[5]/div").text
    entryDict['Song Duration'] = songDuration

    dateAdded = driver.find_element(By.XPATH, songXPath + "/div/div[4]/span").text
    entryDict['Date Added'] = dateAdded

    playlistList.append(entryDict)
    songCounter += 1


df = pd.DataFrame(playlistList)
csvName = playlistName + ".csv"
df.to_csv(csvName, index = False)


time.sleep(3)

