from github import Github
from pprint import pprint


class User () :
    def __init__(self , API_KEY , list_users) -> None:
        self.g = Github(API_KEY , retry=5 , per_page=100)
        self.list_users = list_users


    def get_user (self , g , user_name) : 
        try : 
            user = g.get_user(user_name)
            return user
        except : 
            print('Error in getting user' , user_name)
            return None
    
    def get_dict_user (self,  user , user_name) :
        try : 
            Orgs = [user.company]

            for i in user.get_orgs() :
                Orgs.append(i.login)
            return Orgs
        except :
            print('Error in getting dict_user' , user_name)
            return None
    
    def main_user (self) :
        users = {}
        for i in self.list_users : 
            print('Processing user :' , i)
            user = self.get_user(self.g , i)
            if user is not None : 
                o = self.get_dict_user(user , i)
                if o is not None :
                    users[i] = list(set(o))
        return users



