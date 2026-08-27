from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER,MAIN_DISPATCHER, set_ev_cls
class Flow(app_manager.RyuApp):
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures,CONFIG_DISPATCHER)
    def switch_features_handler(self,ev):
       datapath=ev.msg.datapath
       print("Switch Connected")
       print("DataPath is: ",datapath.id)
       ofp=datapath.ofproto
       parser=datapath.ofproto_parser
       match=parser.OFPMatch(eth_dst="00:00:00:00:00:01")
       actions=[parser.OFPActionOutput(1)]
       inst=parser.OFPFlowMod(
            datapath=datapath,
            priority=100,
            match=match,
            instructions=[
            parser.OFPInstructionActions(
                ofp.OFPIT_APPLY_ACTIONS,
                actions)])
       datapath.send_msg(inst)
       match=parser.OFPMatch(eth_dst="00:00:00:00:00:02")
       actions=[parser.OFPActionOutput(2)]
       inst=parser.OFPFlowMod(datapath=datapath,
                              priority=100,
                              match=match,
                              instructions=[
                                  parser.OFPInstructionActions(
                                      ofp.OFPIT_APPLY_ACTIONS,
                                      actions)
                              ])
       datapath.send_msg(inst)
       match=parser.OFPMatch(eth_dst="00:00:00:00:00:03")   
       actions=[parser.OFPActionOutput(3)]
       inst=parser.OFPFlowMod(datapath=datapath,
                                priority=100,
                                match=match,
                                instructions=[
                                     parser.OFPInstructionActions(
                                          ofp.OFPIT_APPLY_ACTIONS,
                                          actions)
                                ])
       datapath.send_msg(inst)
       match = parser.OFPMatch(
       eth_dst="ff:ff:ff:ff:ff:ff"
            )

       actions = [
        parser.OFPActionOutput(ofp.OFPP_FLOOD)
]

       inst = parser.OFPFlowMod(
       datapath=datapath,
       priority=50,
       match=match,
       instructions=[
        parser.OFPInstructionActions(
            ofp.OFPIT_APPLY_ACTIONS,
            actions
        )
    ]
)
       datapath.send_msg(inst)