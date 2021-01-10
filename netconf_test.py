import ncclient
from ncclient import manager
from ncclient.xml_ import *
import xmltodict, json, pprint
import jinja2
import logging
import sys
import sr_netconf_constants as constants

host1_username = 'netconfuser'
host1_password = 'mypassword'
host1_ip = '191.168.1.138'
host2_ip = '191.168.1.139'
host2_username = 'netconfuser'
host2_password = 'mypassword'

TEMPLATES = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))


logging.basicConfig(filename='netconf_log', 
                    format='%(asctime)s %(levelname)s %(message)s', 
                    level=logging.INFO)
logger = logging.getLogger()
# handler for print log to CLI also
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def create_connection(host, username, password):
    
    conn = manager.connect(host=host,
                           port='830',
                           username=username,
                           password=password,
                           hostkey_verify=False,
                           device_params={'name':'alu'})
  
    return conn

## read_file
# In: filename
# Out: List containing all non-blank lines from filename
def read_file(filename):
    f = open(filename, 'r')
    output = f.read().splitlines()
    output = [ line for line in output if line ]
    f.close()
    return output

## write_file
# In: filename and contents to be written to the file
# Out: Nothing (returns 0 on completion)
def write_file(filename, contents):
    f = open(filename, 'w+')
    f.write(contents)
    f.close()
    return 0


## edit config target='candidate'
# In: netconf manager connection
# In: config_data (as xml)
# In: config_name for print/log
def nc_edit_config(conn, config_data, config_name = 'config'):
    conn_locked = False
    try:
        conn.lock(target='running')
        conn.lock(target='candidate')
        conn_locked = True
        
        logger.info(conn._session.host + 'conection locked')

        edit_conf_rpc = conn.edit_config(target = 'candidate', 
                                         config = config_data)
        
        conn.commit()
        conn.unlock(target='candidate')
        conn.unlock(target='running')

        logger.info('{} "{}" edited and committed'.format(conn._session.host, config_name))
    
    except Exception as error:

        if "Data already exists" in str(error):
            logger.warning('{} "{}" data already exist'.format(conn._session.host, config_name))
            conn.unlock(target='candidate')
            conn.unlock(target='running')
        
        elif "Data missing" in str(error):
            logger.warning('{} "{}" data missing'.format(conn._session.host, config_name))
            conn.unlock(target='candidate')
            conn.unlock(target='running')
        
        else:
            conn.discard_changes()
            if conn_locked: 
                conn.unlock(target='candidate')
                conn.unlock(target='running')
            raise

## nc_get
# In: netconf manager connection
# In: config_data as a filter, if not stated, get all config
# In: config_name for print/log
# In: format output format
# Out:  return fetched config
# can be used to get running config and also state data
def nc_get(conn, config_data, config_name = 'config', format = 'XML'):
    
    if config_data:
        config = conn.get(filter=('subtree', config_data))
    else:
        config = conn.get()
    
    config = config.data_xml

    logger.info('{} "{}" readed/filtered:'.format(conn._session.host, config_name))
    
    if format.upper() == 'JSON':
          config = xmltodict.parse(config, dict_constructor=dict)
          logger.info(json.dumps(config, indent = 4))
    else:
      logger.info('\n' + config)
    
    return config

## nc_get_config
# In: netconf manager connection
# In: config_data as a filter, if not stated, get all config
# In: config_name for print/log
# In: format output format
# Out:  return fetched config
# can be used to get running/candidate config, but not for state
# put here to be an example
def nc_get_config(conn, config_data = '', config_name = 'config', format = 'XML'):
    
    if config_data:
        config = conn.get_config(source = 'running', 
                                 filter = ('subtree', config_data))
    else :
        config = conn.get_config(source='running')

    config = config.data_xml
    
    logger.info('{} "{}" readed/filtered:'.format(conn._session.host, config_name))
    
    if format.upper() == 'JSON':
        config = xmltodict.parse(config, dict_constructor=dict)
        logger.info(json.dumps(config, indent = 4))
    else:
        logger.info('\n' + config)
    
    return config

# an example VPRN create and delete method
# includes edit-config and get config
def vprn_test():

    conn = create_connection(host1_ip, host1_username, host1_password)

    # VPRN 1002 CREATE
    template = TEMPLATES.get_template('vprn.j2')
    config = template.render(constants.VPRN_1002_CREATE)

    nc_edit_config(conn, config, 'VPRN 1002 CREATE')

    config_reply = nc_get(conn, constants.SERVICE_FILTER, 'VPRN config', 'JSON')
    
    """
    # parse reply (dict)
    vprn_list = config_reply['rpc-reply']['data']['configure']['service']['vprn']
    for vprn in vprn_list:
        print('vprn name : {} '.format(vprn['service-name']))
    """

    # VPRN 1002 DELETE
    template = TEMPLATES.get_template('vprn.j2')
    config = template.render(constants.VPRN_1002_DELETE)

    nc_edit_config(conn, config, 'VPRN 1002 DELETE')

    config_reply = nc_get(conn, constants.SERVICE_FILTER, 'VPRN config')
    
    conn.close_session()

# VPRN configure method includes
# connect device (includes 2 different SR configuration)
# make port configuration
# make default-BGP-policy (accept all)
# make VPRN configuration including interfaces and BGP
# also after the configuration-edit, related configurations fetched
def vprn_bgp_config():
   
    #####################################################################
    ######################  Configure SR-1 ##############################
    #####################################################################
    # Connection to SR-1
    conn = create_connection(host1_ip, host1_username, host1_password)

    # PORT CREATE SR-1
    template = TEMPLATES.get_template('port.j2')
    config = template.render(constants.PORT_CREATE_SR1)

    nc_edit_config(conn, config, 'PORT create config')

    nc_get(conn, constants.PORT_FILTER, 'PORT config')

    # Default BGP Policy SR-1
    nc_edit_config(conn, constants.DEFAULT_BGP_POLICY_CREATE, 'Default BGP pol.')
    

    # VPRN 1005 CREATE SR-1
    template = TEMPLATES.get_template('vprn.j2')
    config = template.render(constants.VPRN_1005_CREATE_SR1)

    nc_edit_config(conn, config, 'VPRN 1005 CREATE')

    nc_get(conn, constants.SERVICE_FILTER, 'VPRN config')

    conn.close_session()
    

    #####################################################################
    ######################  Configure SR-2 ##############################
    #####################################################################
    # Connection to SR-2
    conn = create_connection(host2_ip, host2_username, host2_password)

    # PORT CREATE SR-2
    template = TEMPLATES.get_template('port.j2')
    config = template.render(constants.PORT_CREATE_SR2)

    nc_edit_config(conn, config, 'PORT create config')

    nc_get(conn, constants.PORT_FILTER, 'PORT config')

    # Default BGP Policy SR-2
    nc_edit_config(conn, constants.DEFAULT_BGP_POLICY_CREATE, 'Default BGP pol.')
    
    # VPRN 1005 CREATE SR-2
    template = TEMPLATES.get_template('vprn.j2')
    config = template.render(constants.VPRN_1005_CREATE_SR2)

    nc_edit_config(conn, config, 'VPRN 1005 CREATE')

    nc_get(conn, constants.SERVICE_FILTER, 'VPRN config')

    conn.close_session()

# Fetches VPRN state (route-table and BGP) of the devices
# this method added as a seperate method (not in vprn_bgp_config method)
# in order to call seperately
def vprn_state():

    # wait for bgp
    #sleep(30)
    #####################################################################
    ######################  Get VPRN States #############################
    #####################################################################
    # Connection to SR-1
    # state gilter with string formatting
    conn = create_connection(host1_ip, host1_username, host1_password)
    state_filter = constants.STATE_VPRN_ROUTE_TABLE.format(vprn='1005')
    state_vprn_route_table = nc_get(conn, state_filter, 'VPRN ROUTE TABLE STATE')

    state_filter = constants.STATE_VPRN_BGP.format(vprn='1005')
    state_vprn_bgp = nc_get(conn, state_filter, 'ROUTER BGP STATE')
    
    conn.close_session()

    # Connection to SR-2
    # state gilter with string formatting
    conn = create_connection(host2_ip, host2_username, host2_password)
    state_filter = constants.STATE_VPRN_ROUTE_TABLE.format(vprn='1005')
    config = nc_get(conn, state_filter, 'ROUTER STATE')

    state_filter = constants.STATE_VPRN_ROUTE_TABLE.format(vprn='1005')
    state_vprn_route_table = nc_get(conn, state_filter, 'VPRN ROUTE TABLE STATE')

    state_filter = constants.STATE_VPRN_BGP.format(vprn='1005')
    state_vprn_bgp = nc_get(conn, state_filter, 'ROUTER BGP STATE')

# deletes VRPN configs done in vprn_bgp_config method
# also deletes port and default-BGP-policy configs
def delete_vprn_config():

    #####################################################################
    # SR-1
    #####################################################################
    conn = create_connection(host1_ip, host1_username, host1_password)

    # VPRN 1005 DELETE SR-1
    template = TEMPLATES.get_template('vprn.j2')
    config = template.render(constants.VPRN_1005_DELETE_SR1)

    nc_edit_config(conn, config, 'VPRN 1005 DELETE')

    nc_get_config(conn, constants.SERVICE_FILTER, 'VPRN config')

    # Default BGP Policy SR-1
    nc_edit_config(conn, constants.DEFAULT_BGP_POLICY_DELETE, 'Default BGP pol.')


    # PORT DELETE SR-1
    template = TEMPLATES.get_template('port.j2')
    config = template.render(constants.PORT_DELETE_SR1)

    nc_edit_config(conn, config, 'PORT DELETE config')

    nc_get_config(conn, constants.PORT_FILTER, 'PORT config')

    conn.close_session()

    #####################################################################
    # SR-2
    #####################################################################
    conn = create_connection(host2_ip, host2_username, host2_password)

    # VPRN 1005 DELETE SR-2
    template = TEMPLATES.get_template('vprn.j2')
    config = template.render(constants.VPRN_1005_DELETE_SR2)

    nc_edit_config(conn, config, 'VPRN 1005 DELETE')

    nc_get_config(conn, constants.SERVICE_FILTER, 'VPRN config')

    # Default BGP Policy SR-2
    nc_edit_config(conn, constants.DEFAULT_BGP_POLICY_DELETE, 'Default BGP pol.')   

    # PORT DELETE SR-2
    template = TEMPLATES.get_template('port.j2')
    config = template.render(constants.PORT_DELETE_SR2)

    nc_edit_config(conn, config, 'PORT DELETE config')

    nc_get_config(conn, constants.PORT_FILTER, 'PORT config')

    conn.close_session()

def main():

    try:
        """
        basic vprn create and delete in same method
        """
        vprn_test()

        """
        vrpn create in 2 different SR with BGP ###
        """
        #vprn_bgp_config()
        #vprn_state()
        #delete_vprn_config()

        """
        some trials
        """
        #conn = create_connection(host1_ip, host1_username, host1_password)
        #filter = constants.STATE_VPRN_BGP.format(vprn='1005')
        #filter = constants.STATE_ALL
        #config = nc_get(conn, filter, 'ROUTER STATE')
        #conn.close_session()
        #write_file(conn._session.host, config.data_xml)

    except Exception as error:
        logger.info('Error:\n' + str(error))
        
        if hasattr(error, 'info'):
            logger.info('Error info:\n' + str(error.info))


if __name__ == "__main__":
  main()
