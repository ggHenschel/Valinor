import networkx as nx
from xml.dom import minidom

class ProcessModel():

    def __init__(self):
        self.Graph = None

    def create_from_file(self,origin_path):
        self.name = str(origin_path).split("/")[-1]
        xmldoc = minidom.parse(origin_path)

        nodeslist = xmldoc.getElementsByTagName('Node')
        edgelist = xmldoc.getElementsByTagName('Edge')

        self.Graph = nx.DiGraph()

        Dict = {-1: -1}

        for node in nodeslist:
            # print(node.attributes['index'].value,str(node.attributes['activity'].value))
            Dict[node.attributes['index'].value] = node.attributes['activity'].value
            self.Graph.add_node(node.attributes['activity'].value)

        Dict.pop(-1)

        StarNode = xmldoc.getElementsByTagName('StartNode')
        EndNode = xmldoc.getElementsByTagName('EndNode')

        for node in StarNode:
            # print(node.attributes['index'].value,str(node.attributes['activity'].value))
            Dict[node.attributes['index'].value] = "StartNode"
            self.Graph.add_node("StartNode")

        for node in EndNode:
            # print(node.attributes['index'].value,str(node.attributes['activity'].value))
            Dict[node.attributes['index'].value] = "EndNode"
            self.Graph.add_node("EndNode")

        for edge in edgelist:
            nodeS = Dict[edge.attributes['sourceIndex'].value]
            nodeT = Dict[edge.attributes['targetIndex'].value]
            minTime = int(edge.getElementsByTagName('Duration')[0].attributes['min'].value)
            meanTime = int(edge.getElementsByTagName('Duration')[0].attributes['mean'].value)
            maxTime = int(edge.getElementsByTagName('Duration')[0].attributes['max'].value)
            self.Graph.add_edge(nodeS, nodeT, minTime=minTime, maxTime=maxTime, meanTime=meanTime)

    # def meanTime(self, start, end):
    #     return path_analisys.TempoMedioEntreGoldStd(self.Graph, start, end)
    #
    # def replay(self, eventlogpath):
    #     log = import_eventLog.import_eventlog(eventlogpath)
    #     self.replay_results = replay.replay_log(log, self.Graph)
    #
    # def findCicles(self):
    #     print("Processo Pode Demorar Alguns Minutos")
    #     ciclos = path_analisys.FindCyles(self.Graph)
    #     return ciclos
    #
    # def case_report(self, log):
    #     if self.replay_results is None:
    #         self.replay(log)
    #     r = replay.export_replay_results(self.replay_results)
    #     s = replay.rebuild_event_log(log, self.replay_results)
    #     return (r, s)
    #
    # def Class_Assistant(self, log, file, save_path=None):
    #     if self.replay_results is None:
    #         self.replay(log)
    #     return replay.Rebuild_Atributes_Log(file, self.replay_results, save_path=save_path)

    def Degree_Centrality(self):
        return nx.degree_centrality(self.Graph)

    def In_Degree_Centrality(self):
        return nx.in_degree_centrality(self.Graph)

    def Out_Degree_Centrality(self):
        return nx.out_degree_centrality(self.Graph)

    def Closeness_Centrality(self):
        return nx.closeness_centrality(self.Graph)

    def Betweenness_Centrality(self):
        return nx.betweenness_centrality(self.Graph)

    def details(self):
        name = self.name
        n_nodes = self.Graph.number_of_nodes()
        n_transitions = self.Graph.number_of_edges()
        return (name,n_nodes,n_transitions)