#%%
from github import Github
from pprint import pprint


class Repository () :
    def __init__(self , API_KEY , repositary_name) -> None:
        self.g = Github(API_KEY , retry=5 , per_page=100)
        self.repositary_name = repositary_name

    def get_repo (self ) : 
        try : 
            repo = self.g.get_repo(self.repositary_name)
            return repo
        except : 
            print('Error in getting repo' , self.repositary_name)
            return None
    
class Issues () :

    def __init__(self , repositary_name , repo ,state = 'all') -> None:
        self.repository_name = repositary_name
        self.repo = repo
        self.state = state

    def get_n_issues (self )    :
        try : 
            return self.repo.get_issues(state=self.state).totalCount
        except :
            print('Error in getting n_issues' , self.repository_name)
            return 0
        

    def get_dict_issues (self,  number_of_issues) : 
        users = []
        if number_of_issues > 0 : 
            for i in range(0 , number_of_issues) : 
                try : 
                    users.append(self.repo.get_issues(state=self.state)[i].user.login)
                except : 
                    pass
        return users

    def main_issue (self) : 
        n_issues = self.get_n_issues()
        users = self.get_dict_issues(n_issues )
        return users

class Commits () :
    def __init__(self , repositary_name , repo) -> None:
        self.repository_name = repositary_name
        self.repo = repo
    
    def get_list_commits (self) :
        try : 
            return self.repo.get_commits()
        except : 
            print('Error in getting commits' , self.repository_name)
            return None
    
    def main_commits (self) : 
        commits = self.get_list_commits()
        if commits is None : 
            return None
        else :
            users =[]
            for i in commits : 
                try : 
                    users.append(i.author.login)
                except :
                    pass
            return users

class Forks () :
    def __init__(self , repositary_name , repo) -> None:
        self.repository_name = repositary_name
        self.repo = repo
    
    def get_list_forks (self) :
        try : 
            return self.repo.get_forks()
        except : 
            print('Error in getting forks' , self.repository_name)
            return None
    
    def main_forks (self) :
        forks = self.get_list_forks()
        if forks is None : 
            return None
        else :
            users = []
            for f in forks : 
                users.append((str(f.full_name).split('/')[0]))
            return  users
        
class Get_All () :
    def __init__(self , API_KEY, repositary_name  ) -> None:
        self.repositary_name = repositary_name
        self.repo = Repository(API_KEY , self.repositary_name).get_repo()
        self.Issues = Issues(self.repositary_name , self.repo , state = 'all').main_issue()
        self.Commits = Commits(self.repositary_name , self.repo).main_commits()
        self.Forks = Forks(self.repositary_name , self.repo).main_forks()

    def main (self) :
        return {'Repository' : self.repositary_name , 'Author' : self.repositary_name.split('/')[0] ,
            'Issues' : self.Issues ,'Commits' : self.Commits , 'Forks' : self.Forks}


