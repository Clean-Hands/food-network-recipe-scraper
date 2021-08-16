import requests
from bs4 import BeautifulSoup
import re
import os
import threading
import glob

def getValidFilename(s: str) -> str:
    s = str(s).strip()
    return re.sub(r'(?u)[^-\w.\[\]() ]', '', s)

letter = ["123", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "xyz"]
letterNum = -1
duplicates = 0
lastTitle = ""
threads = []
number = -1

class myThread (threading.Thread):

    def __init__(self, threadID, title, URL, letter, letterNum):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.title = title
        self.URL = URL
        self.letter = letter
        self.letterNum = letterNum

    def run(self):
        downloadFile(self.title, self.URL, self.letter, self.letterNum)


def downloadFile(title, URL, letter, letterNum):
    print(f"Downloading: {title} | URL: {URL}")

    download = requests.get(f"http:{URL}")

    filename = f".\Downloads\{letter[letterNum]}\{title}.html"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "wb") as f:
        f.write(download.content)
        print(f"Done! ({title})")
        return


while letterNum <= len(letter):
    letterNum += 1
    files = glob.glob(f".\Downloads\{letter[letterNum]}\*.html")
    fileNames = []
    for file in files:
        posArray = []
        for pos, char in enumerate(file):
            if char == "\\":
                pos += 1
                posArray.append(pos)
        file = file[posArray[-1]:-5]
        fileNames.append(file)
    response = requests.get(f"https://www.foodnetwork.com/recipes/recipes-a-z/{letter[letterNum]}/p/1")
    soup = BeautifulSoup(response.content, "html.parser")

    maxPage = soup.select(" div > section > ul > li > a")
    maxPage = int(maxPage[-2].string)

    page = 1
    while page <= maxPage:

        response = requests.get(f"https://www.foodnetwork.com/recipes/recipes-a-z/{letter[letterNum]}/p/{page}")
        soup = BeautifulSoup(response.content, "html.parser")

        recipes = soup.select("section > div > div > ul > li")

        print(f"-------------------------------------------------------------------------------- letter: {letter[letterNum]} | page: {page}/{maxPage} | {len(recipes)} links found --------------------------------------------------------------------------------")
        for recipe in recipes:
            aRecipe = recipe.select("a")[0]
            title = getValidFilename(aRecipe.string)
            URL = aRecipe.get("href")

            if not URL[-4:] == "html":

                if lastTitle == title.lower():
                    duplicates += 1
                    title = f"{title} ({duplicates})"
                else:
                    duplicates = 0
                    lastTitle = title.lower()

                if title not in fileNames:

                    number += 1

                    if number % 10 == 0:
                        thread0 = myThread(0, title, URL, letter, letterNum)
                        thread0.start()
                        threads.append(thread0)
                    elif number % 10 == 1:
                        thread1 = myThread(1, title, URL, letter, letterNum)
                        thread1.start()
                        threads.append(thread1)
                    elif number % 10 == 2:
                        thread2 = myThread(2, title, URL, letter, letterNum)
                        thread2.start()
                        threads.append(thread2)
                    elif number % 10 == 3:
                        thread3 = myThread(3, title, URL, letter, letterNum)
                        thread3.start()
                        threads.append(thread3)
                    elif number % 10 == 4:
                        thread4 = myThread(4, title, URL, letter, letterNum)
                        thread4.start()
                        threads.append(thread4)
                    elif number % 10 == 5:
                        thread5 = myThread(5, title, URL, letter, letterNum)
                        thread5.start()
                        threads.append(thread5)
                    elif number % 10 == 6:
                        thread6 = myThread(6, title, URL, letter, letterNum)
                        thread6.start()
                        threads.append(thread6)
                    elif number % 10 == 7:
                        thread7 = myThread(7, title, URL, letter, letterNum)
                        thread7.start()
                        threads.append(thread7)
                    elif number % 10 == 8:
                        thread8 = myThread(8, title, URL, letter, letterNum)
                        thread8.start()
                        threads.append(thread8)
                    elif number % 10 == 9:
                        thread9 = myThread(9, title, URL, letter, letterNum)
                        thread9.start()
                        threads.append(thread9)
                        for t in threads:
                            t.join()
                # else:
                    # print(f"skipped: {title}")


        page += 1

print("Fully Completed!")