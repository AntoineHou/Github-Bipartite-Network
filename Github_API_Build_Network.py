import networkx as nx
from collections import Counter

class Create_Network () : 
    def __init__ (self, list_results, Action , Weights = [1,1,1]) : 
        self.list_results = list_results
        self.Action = Action
        self.Weights = Weights
        #  Weight in the following order : Issues , Commits , Forks 

    def Get_Nodes (self) : 
        Nodes = []
        for i in self.list_results : 
            Nodes.extend(list(set(i['Issues'] + i['Commits'] + i['Forks'])))
        Nodes = list(set(Nodes))
        return Nodes
    
    def Get_Edges (self) : 
        Edges ={}
        for i in self.list_results :
            Users = dict(Counter(i['Issues']*self.Weights[0] + i['Commits']*self.Weights[1] + i['Forks']*self.Weights[2]))
            for key , value in Users.items() :
                    if (key , i['Repository'] ) not in Edges : 
                        Edges[(key , i['Repository'] )] = value
                    else : 
                        Edges[(key , i['Repository'] )] += value
        return  Edges
    
    def Add_Edges (self , G , Edges) : 
        for key , value in Edges.items() : 
            G.add_edge(key[0] , key[1] , weight = value)
        return G
    
    def Create_Network (self) : 
        Edges = self.Get_Edges()
        Nodes = self.Get_Nodes()
        G = nx.Graph()
        G.add_nodes_from(Nodes)
        G = self.Add_Edges(G , Edges)
        return G
    
    def main_network (self) : 
        if self.Action == 'Get Nodes' : 
            return self.Get_Nodes()
        elif self.Action == 'Get Network' :
            return self.Create_Network()
        else :
            print('Error in Action , please choose from [Get Nodes , Get Network]')
            return None

