from bs4 import BeautifulSoup

class Message:
    user = ""
    message = ""
    def __init__(self, user, message):
        self.user = user
        self.message = message

    def __repr__(self):
        return("User: " + self.user + " Message: " + self.message)

class Parsed:
    filename = ""
    messages = []
    soup = None

    def __init__(self, fn):
        self.filename = fn
        with open(self.filename, 'r') as f:
            self.soup = BeautifulSoup(f, 'lxml')
        self.getMessages()

    def getMessages(self):
        allMessages = self.soup.findAll("div", {"class": "message"})
        for msg in allMessages:
            user = msg.find("span", {"class": "user"}).text
            ptag = msg.find_next('p')
            if (ptag.text == ""):
                ptag = msg.next_sibling.next_sibling
                if (ptag == None or ptag.text == "" or len(ptag.text.strip()) == 0):
                    continue
            self.messages.append(Message(user, ptag.text))

    def __repr__(self):
        retStr = ""
        for msg in self.messages:
            retStr += "User: " + msg.user + " Message: " + msg.message + "\n"
        return retStr
