import networkx as nx 

class Update_Network () :
    def __init__(self , G , Users , Results ,Network_Type = 'Individual' ) -> None:
        self.G = G
        self.Users = Users
        self.Results = Results
        self.Network_Type = Network_Type
    
    def Update_Nodes (self ,G) :
        for node in G.nodes :
            if node in self.Users :
                nx.set_node_attributes(G, {node : {'type' : 'user' , 'institution' : self.Users[node][0]}})
            else :
                nx.set_node_attributes(G, {node : {'type' : 'repository' , 'institution' : None}})
        return G

    def Update_Edges (self, G) :
        Author_Repo = []
        for i in self.Results :
            Author_Repo.append((i['Author'] , i['Repository']))
        for edge in G.edges :
            if edge in Author_Repo :
                G.edges[edge]['type'] = 'author'
            else :
                G.edges[edge]['type'] = 'contributor'
        return G
    
    def Update_Network (self) :
        G = self.G
        G = self.Update_Nodes(G)
        G = self.Update_Edges(G)
        return G
    
    def flatten (self, l) :
        return [item for sublist in l for item in sublist]
    
    def Get_Institutions_And_Nodes (self) :
        Institutions = list(set(self.flatten(list(self.Users.values()))))
        # delete None
        Institutions = [i for i in Institutions if i]
        Nodes_Institutions = { i : [] for i in Institutions}
        for key , value in self.Users.items() :
            for i in value :
                if i :
                    Nodes_Institutions[i].append(key)
        return  Nodes_Institutions

    
    def Merge_Nodes (self , G  , Institution_Nodes ) :
        New_G = nx.Graph()
        for node in list(Institution_Nodes.keys()) :
            New_G.add_node(node)
            nx.set_node_attributes(G, {node : {'type' : 'institution'}})

        for items in self.Results :
            New_G.add_node(items['Repository'])
            nx.set_node_attributes(G, {items['Repository'] : {'type' : 'repository'}})
        
        for nodes in list(set(self.flatten(self.Get_Institutions_And_Nodes().values()))) :
            P_e = G.edges(nodes , data = True)
            for n1 , n2 , att in P_e :
                for inst in self.Users[n1] :
                    if inst and (inst , n2) not in New_G.edges() :
                        New_G.add_edge(inst , n2 , weight = att['weight'] )
                    elif inst and (inst , n2) in New_G.edges() :
                        New_G.edges[(inst , n2)]['weight'] += att['weight']
        return New_G
        
    def main_update (self) :
        G = self.Update_Network()
        if self.Network_Type == 'Individual' :
            pass 
        elif self.Network_Type == 'Institution' :
            Institution_Nodes = self.Get_Institutions_And_Nodes()
            G = self.Merge_Nodes(G , Institution_Nodes)
        else :
            print('Error in Network_Type , please choose from [Individual , Institution]')
            return None
        return G 
