from bs4 import BeautifulSoup
import requests
import os


class CommicTracker:
    def __init__(self, saveFile):
        self.trackingComic = {}
        self.saveFile = saveFile
        self.initDict()

    '''
        DICT FUNCTION:

        Create the dict from the save file when called
    '''
    def initDict(self):
        try:
            f = open(self.saveFile)
            for line in f:
                line = line.strip("\n")
                title, updateTime, url = line.split("+")
                self.updateDict(title, updateTime, url)
            f.close()

        except IOError:
            f = open(self.saveFile, "w")
            f.close()

    '''
        Update the main dict when it is called
    '''
    def updateDict(self, title, updateTime, url):
        self.trackingComic[title] = {
            "Latest update": updateTime,
            "URL": url
        }
    
    '''
        This function take all commic in the main dict and save them to the given file
    '''
    def updateSaveFile(self):
        f = open("data.temp", "w")
        for key, value in self.trackingComic.items():
            f.write("%s+%s+%s\n" % (key, value["Latest update"], value["URL"]))
        f.close()
        os.remove(self.saveFile)
        os.rename("data.temp", self.saveFile)
        print("\nSave file had been updated.")

    '''
        Retun the list of Commic tracking
    '''
    def getComicList(self):
        data = []
        for key in self.trackingComic:
            data.append(key)
        return data

    '''
        Receive a name return the url if it in the dict, return "-1" if not
    '''
    def getURL(self, name):
        if name in self.trackingComic:
            return self.trackingComic[name]["URL"]
        return "-1"

    '''
        Receive a name return the latest update if it in the dict, return "-1" if not
    '''
    def getUpdate(self, name):
        if name in self.trackingComic:
            return self.trackingComic[name]["Latest update"]
        return "-1"

    '''
        WEB SRAPING:

        Given a url of a comic, save that comic to the file
    '''
    def addComic(self, url):
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        updateTime = soup.find("ul", class_="row-content-chapter").li.find("span", class_="chapter-time text-nowrap").text
        title = soup.find("div", class_="story-info-right").h1.text

        print(f"\n -> Latest update of this manga is {updateTime}")
        self.updateDict(title, updateTime, url)
        self.updateSaveFile()

    '''
        Recive a url form of the commic and return the latest update time
    '''
    def checkLastestUpdate(self, url):
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        updateTime = soup.find("ul", class_="row-content-chapter").li.find(
            "span", class_="chapter-time text-nowrap").text
        return updateTime

    '''
        INTERAC WITH USER:

        Get user input: Manga name and url promp user to enter again if it not valid, else pass throught to the next phase
    '''
    def prompAddComic(self):
        userIn = input("\nAdd manga url here to track it: ")
        userIn = userIn.strip()

        for key in self.trackingComic:
            if userIn == self.getURL(key):
                print("\nYou already tracking this manga.") 
                return

        try:
            self.addComic(userIn)
            return

        except Exception:
            print("\nYour url is not vaild, please try again")
            print()
            self.prompAddComic()

    '''
        Get user yes/no answer
    '''
    def getYesNo(self, action):
        answer = input(f"\nDo you wish to {action}(yes/no): ")
        answer = answer.strip().lower()
        while answer != "no" and answer != "yes":
            answer = input("\nThat answer is invalid!\nPlease renter your answer: ").strip()
        return answer

    '''
        Ask for the manga name, if typo or new ask to make new else return url
    '''
    def prompCheckComic(self):
        print("\nWhat manga you what to check?")
        userIn = input("\nInput here: ")
        userIn = userIn.strip()

        url = self.getURL(userIn)
        if url == "-1":
            print("\nThe Manga you\'re looking for is not tracked or has a typo.")
            answer = self.getYesNo("tract this manga")
            if answer == "no":
                self.prompCheckComic()
            else:
                self.prompAddComic()
                return "-1", "-1", "-1"
        else:
            lastUpdate = self.getUpdate(userIn)
            return userIn, url, lastUpdate
    
    '''
        Get a name if not exist track it else if not updated return false else return true
    '''
    def checkUpdate(self, title, url, lastUpdate):
        if url == "-1" and lastUpdate == "-1" and title == "-1":
            return
        
        latestUpdate = self.checkLastestUpdate(url)
        print()
        print(latestUpdate)

        if latestUpdate == lastUpdate:
            print("\nSorry new chapter haven\'t out yet T^T")
        elif latestUpdate != lastUpdate:
            print("\nNEW chapter is OUT NOW!!! :))))))")
            self.updateDict(title, latestUpdate, url)
            self.updateSaveFile()


if __name__ == "__main__":
    new = CommicTracker("new.txt")
    print()
    print("Here is the list of manga you are tracking:")
    print("->",new.getComicList())
    print("-> Put nothing if you want to add a new one")
    
    this, that, those = new.prompCheckComic()
    new.checkUpdate(this, that, those)