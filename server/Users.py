#the class that define user and which argumentes the user will have
class User:
    def __init__(self,username_,password_,email_,name_):
        self.username = username_
        self.password = password_
        self.email = email_
        self.name = name_
        self.activeInChat = False
    #login check, check if password and username is equal to self.password and self.username
    def isTheUser(self,username_,password_):
        if password_ == self.password and username_ == self.username:
            return True
        else:
            return False
#class that handle the created users and put them in a list
class CollectionOfUsers:
    def __init__(self):
        self.list_of_users = []
    #add a new user and save it into the list_of_users
    #first check if the username already exist
    def add_user(self,username_,password_,email_,name_):
        usernameExists = False
        for user in self.list_of_users:
            if user.username == username_:
                usernameExists = True
                break
        if usernameExists == True:
            return False
        else:
            user = User(username_,password_,email_,name_)
            self.list_of_users.append(user)
            return True
    #check if the user is active in the chat or not
    def doesThisUserExistAndNotActive(self,username_,password_):
        for user in self.list_of_users:
            if user.isTheUser(username_,password_):
                if user.activeInChat == False:
                    user.activeInChat = True
                    return True
                else:
                    return False
        return False
    #this method handles the inactiveusers by set activeinchat to false
    def inactiveUser(self,usernameToInactive):
        for user in self.list_of_users:
            if user.username == usernameToInactive:
                user.activeInChat = False
    #this method handles the remove of a user
    def remove_user(self,username_):
        for i in range(self.list_of_users):
            if self.list_of_users[i].username == username_:
                self.list_of_users.pop(i)
                return True

        return False
    #this method gives u all info about a user by thier username
    def getUserObjByUsername(self,username_):
        for i in range(self.list_of_users):
            if self.list_of_users[i].username == username_:
                return self.list_of_users[i]

        return "non"
    #handles the read of users from a txt file users.
    #then save the user by using the method add_user
    def readUsersFromFile(self):
        try:
            file = open("users.txt",'r')
            allLines = file.read().split('\n')
            file.close()
        except:
            return False

        index_of_current_line = 0

        while True:
            username = allLines[index_of_current_line]
            index_of_current_line+=1
            if username == "":
                return True

            password = allLines[index_of_current_line]
            index_of_current_line += 1
            if password == "":
                return False

            email = allLines[index_of_current_line]
            index_of_current_line += 1
            if email == "":
                return False

            name = allLines[index_of_current_line]
            index_of_current_line += 1
            if name == "":
                return False

            emptyLine = allLines[index_of_current_line]
            index_of_current_line+=1
            if emptyLine != "":
                return False

            self.add_user(username,password,email,name)

            if index_of_current_line == len(allLines):
                return True

    #write users to a file so we can save them
    def writeUsersToFile(self):
        allContent = ""

        for user in self.list_of_users:
            allContent+=user.username+"\n"
            allContent+=user.password+"\n"
            allContent+=user.email+"\n"
            allContent+=user.name+"\n"
            allContent+="\n"

        try:
            file = open("users.txt",'w')
            file.write(allContent)
            file.close()
            return True
        except:
            return False
