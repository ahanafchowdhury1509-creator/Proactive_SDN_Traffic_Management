from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.controller import MAIN_DISPATCHER
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
class exsw13(app_manager.RyuApp):
     OFP_VERSIONS=[ofproto_v1_3.OFP_VERSION]
     def __init__(self,*args,**kwargs):
            super(exsw13,self).__init__(*args,**kwargs)
            self.mac_to_port={}
     @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
     def switch_features_handler(self,ev):
            datapath=ev.msg.datapath
            ofproto=datapath.ofproto
            parser=datapath.ofproto_parser
            match=parser.OFPMathch()
            actions=[parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,ofproto.OFPCML_NO_BUFFER)])]
            self.add_flow(datapath,0,match,actions)