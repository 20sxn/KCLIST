"""
python implementation of KCLIST, described in " Maximilien Danisch, Oana Balalau, Mauro Sozio. Listing k-cliques in Sparse Real-World Graphs. 2018"
Article available here: https://oanabalalau.com/pdf/kcliques.pdf
"""


class vertex:
    def __init__(self, identifier, neighbor, label):
        self.id = identifier
        self.deg = 0
        self.neigh = neighbor
        self.label = label
        self.degrees = [0 for _ in range(label)]

    
    def add_neigh(self, id_neigh):
        self.deg += 1
        self.degrees[self.label-1] += 1
        self.neigh.append(id_neigh)
        
    def update_deg(self, degree):
        self.deg = degree
        self.degrees[self.label-1] = degree
    
    def update_neigh(self,id_neigh):
        assert self.id < id_neigh
        self.neigh.insert(0, self.neigh.pop(self.neigh.index(id_neigh)))
    
    def revert_degree(self):
        self.deg = self.degrees[self.label-1]
    
class DAG_:
    def __init__(self,G,k):
        V,E = G
        self.adj = []
        for i in range(len(V)):
            self.adj.append(vertex(i,[],k))
        
        for u,v in E:
            if u>v : u,v = v,u
            self.adj[u].add_neigh(v)



def induced_DAG(DAG,u,l):
    """
    Modify DAG to get the induced graph by the neighbourhood of u
    """
    for i in range(DAG.adj[u].deg):
        v = DAG.adj[u].neigh[i]
        if DAG.adj[v].label == l: DAG.adj[v].label = l-1
    
    for i in range(DAG.adj[u].deg):
        v = DAG.adj[u].neigh[i]
        new_deg = 0
        for w in DAG.adj[v].neigh:
            assert u < w
            if DAG.adj[w].label == l-1:
                DAG.adj[v].update_neigh(w)
                new_deg += 1
        DAG.adj[v].update_deg(new_deg)

def listing(l,DAG,C,res):
    if l == 2:
        for u in DAG.adj: #listing all nodes
            if u.label == l: #if u is in the correct subgraph
                for i in range(u.deg):
                    
                    res.append(C|{u.id,u.neigh[i]})
    else:
        for u in DAG.adj:
            if u.label == l:

                induced_DAG(DAG,u.id,l) #labeling
               
                listing(l-1,DAG,C|{u.id},res)

                for i in range(u.deg): #relabeling
                    v = u.neigh[i]
                    DAG.adj[v].label = l
                    DAG.adj[v].revert_degree()

def KCLIST(G,k):
    """
    Return the list of all cliques of size k of G = (V,E) and V = {i for i in range(|V|)}
    """
    DAG = DAG_(G,k)
    res = []
    listing(k,DAG,set(),res)
    return res