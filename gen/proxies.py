"""
    This code is used to associate IP address seen to a switch when partitioning is in place
    If FlowSpace Firewall or FlowVisor is not used, this module is not useful.
"""
import json


D_ADDR = None
DEST_PORT = None
NET = {}
dpid_dict = {}


def load_names_file(device_names):
    default = 'docs/devices_list.json'
    pfile = default if device_names == 0 else device_names

    try:
        with open(pfile) as jfile:
            json_content = json.loads(jfile.read())
    except Exception as error:
        print "Error %s Opening file %s" % (error, pfile)
        return

    global dpid_dict
    dpid_dict = json_content


def insert_ip_port(dest_ip, dest_port):
    """
        Once the TCP/IP packet is dissected and a OpenFlow message type 13
           (PacketOut) is seen, save both destination IP and TCP port
        Args:
            dest_ip: destination IP address
            dest_port: destination TCP port
    """
    global D_ADDR
    global DEST_PORT
    D_ADDR = dest_ip
    DEST_PORT = dest_port


def save_dpid(lldp):
    """
        Get the DPID from the LLDP.c_id
        Args:
            lldp: LLDP class
    """
    global NET

    ip = D_ADDR
    port = DEST_PORT
    try:
        dpid = lldp.c_id.split(':')[1]
    except IndexError:
        dpid = lldp.c_id
    sw_name = get_name_dpid(dpid)
    NET[ip, port] = sw_name


def get_name_dpid(dpid):
    sw_name = dpid_dict.get(dpid)
    if sw_name is not None:
        return sw_name
    return 'OFswitch'


def get_ip_name(ip, port):
    for i, j in NET.iteritems():
        if i == (ip, port):
            return '%s(%s)' % (ip, j)
    return ip
