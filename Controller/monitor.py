from operator import attrgetter
from Controller import switch
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER,DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls 
from ryu.lib import hub
class Monitor(switch.exsw13):
     def __init__(self,*args,**kwargs):
            super(Monitor,self).__init__(*args,**kwargs)
            self.datapaths={}
            self.monitor_thread=hub.spawn(self.__monitor)
     @set_ev_cls(ofp_event.EventOFPStateChange,[MAIN_DISPATCHER,DEAD_DISPATCHER])
     def state_change_handler(self,ev):
            datapath=ev.datapath
            if ev.state==MAIN_DISPATCHER:
                if not datapath.id in self.datapaths:
                    self.logger.debug('register datapath:%016x',datapath.id)
                    self.datapaths[datapath.id]=datapath
            elif ev.state==DEAD_DISPATCHER:
                if datapath.id in self.datapaths:
                    self.logger.debug('unregister datapath:%016x',datapath.id)
                    del self.datapath[datapath.id]
     def __monitor(self):
          while True:
                for dp in self.datapaths.values():
                    self.__request_stats(dp)
                hub.sleep(10)
     def __request_stats(self,datapath):
            self.logger.debug('send stats request: %016x',datapath.id)
            ofproto=datapath.ofproto
            parser=datapath.ofproto_parser
            req=parser.OFPFlowStatsRequest(datapath)
            datapath.send_msg(req)
            req=parser.OFPPortStatsRequest(datapath,0,ofproto.OFPP_ANY)
            datapath.send_msg(req)
     @set_ev_cls(ofp_event.EventOFFlowStatsReply,MAIN_DISPATCHER )
     def flow_stats_reply_handler(self,ev):
           body=ev.msg.body
            