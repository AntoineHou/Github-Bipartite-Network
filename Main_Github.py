from Github_API_Get_Users import Get_All
from Github_API_Meta_Users import User
from Github_API_Build_Network import Create_Network
from Github_API_Node_Update import Update_Network

List_Repository = ['whai362/TDA-ReCTS' , 'Zeqiang-Lai/DPHSIR']
TOKEN = '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'
Network_Type = 'Institution'

def Get_results (TOKEN ,List_Repository) : 
    List_Results = []
    for i in List_Repository : 
        List_Results.append(Get_All(TOKEN , i).main())
    return List_Results

Results = Get_results(TOKEN , List_Repository )
List_Users = Create_Network(Results, 'Get Nodes').main_network()
G = Create_Network(Results , 'Get Network').main_network()
Users_Data = User(TOKEN , List_Users ).main_user()
G = Update_Network(G , Users_Data , Results , Network_Type).main_update()


