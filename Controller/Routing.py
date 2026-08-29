from collections import deque
from ryu.topology import event
from ryu.topology.api import get_switch,get_link
from ryu.base import app_manager
from ryu.controller.handler import set_ev_cls
from Controller.Flow import add_flow
from ryu.lib import hub
class Routing(app_manager.RyuApp):
     def __init__(self,*args,**kwargs):
         super(Routing,self).__init__(*args,**kwargs)
         self.graph={}
         self.path_inst=False
         self.monitor_thread=hub.spawn(self._reroute_loop)
     @set_ev_cls(event.EventSwitchEnter)
     def switch_enter_handler(self,ev):
           switch_id=ev.switch.dp.id
           if switch_id not in self.graph:
                self.graph[switch_id]={}
     @set_ev_cls(event.EventLinkAdd)
     def link_add_handler(self,ev):
              src=ev.link.src.dpid
              dst=ev.link.dst.dpid
              if src not in self.graph:
                  self.graph[src]={}
              if dst not in self.graph:
                  self.graph[dst]={}
              if dst not in self.graph[src]:
                  self.graph[src][dst]=ev.link.src.port_no
              if src not in self.graph[dst]:
                  self.graph[dst][src]=ev.link.dst.port_no
              self.logger.info("Current graph: %s", self.graph)
              if (len(self.graph)>=4 and all(len(neighbors)>=1 for neighbors in self.graph.values()) and not self.path_inst):
                  self.path_inst=True
                  path=bfs_path(self.graph,1,4)
                  ports=path_to_ports(self.graph,path)
                  self.logger.info("Graph is fully connected. Installing paths.")
                  self.install_path(path,ports,"00:00:00:00:00:02")
                  path2 = bfs_path(self.graph, 4, 1)
                  ports2 = path_to_ports(self.graph, path2)
                  self.install_path(path2, ports2, "00:00:00:00:00:01")
     def install_path(self,path,ports,dst_mac):
          for i in range(len(ports)):
               switch_id=path[i]
               out_port=ports[i]
               switch=get_switch(self,switch_id)[0]
               datapath=switch.dp
               parser=datapath.ofproto_parser
               match=parser.OFPMatch(eth_dst=dst_mac)
               actions=[parser.OFPActionOutput(out_port)]
               add_flow(datapath,1,match,actions)
     def _reroute_loop(self):
        while True:
         hub.sleep(15)
         if(len(self.graph)>=4 and all(len(neighbors)>=1 for neighbors in self.graph.values())):
             self.logger.info("Rerouting:Avoiding switch2 now")
             path=bfs_path(self.graph,1,4,avoid={2})
             ports=path_to_ports(self.graph,path)
             self.install_path(path,ports,"00:00:00:00:00:02")
def bfs_path(graph,start,goal,avoid=None):
    if avoid==None:
        avoid=set()
    queue=deque()
    queue.append(start)
    came_from={start:None}
    while queue:
        cur=queue.popleft()
        if cur==goal:
            break
        for neigh in graph[cur]:
            if neigh not in came_from and neigh not in avoid:
                queue.append(neigh)
                came_from[neigh]=cur
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur)
        cur=came_from[cur]
    path.reverse()
    return path
def path_to_ports(graph,path):
     ports=[]
     for i in range(len(path)-1):
          src=path[i]
          dst=path[i+1]
          port=graph[src][dst]
          ports.append(port)
     return ports

if __name__ == "__main__":
    test_graph = {1: {2: 1, 3: 2}, 2: {1: 3, 4: 2}, 3: {1: 1, 4: 3}, 4: {2: 2, 3: 1}}
    path = bfs_path(test_graph, 1, 4)
    print("Path:", path)
    print("Ports:", path_to_ports(test_graph, path))