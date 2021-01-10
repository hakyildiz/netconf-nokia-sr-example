

_NS_MAP = {
    'nc': 'urn:ietf:params:xml:ns:netconf:base:1.0',
    'nokia-conf': 'urn:nokia.com:sros:ns:yang:sr:conf',
    'nokia-state' : 'urn:nokia.com:sros:ns:yang:sr:state'
}

###############################################################
###################  FILTERS ##################################
###############################################################
MGMT_INT_FILTER = '''
<configure xmlns="%s">
  <system>
    <management-interface/>
  </system>
</configure>
''' % (_NS_MAP['nokia-conf'])

CARD_FILTER = '''
<configure xmlns="%s">
  <card>
  </card>
</configure>
''' % (_NS_MAP['nokia-conf'])

ROUTER_FILTER = '''
<configure xmlns="%s">
  <router>
  </router>
</configure>
''' % (_NS_MAP['nokia-conf'])

SERVICE_FILTER = '''
<configure xmlns="%s">
  <service>
  </service>
</configure>
''' % (_NS_MAP['nokia-conf'])

PORT_FILTER = '''
<configure xmlns="%s">
  <port>
  </port>
</configure>
''' % (_NS_MAP['nokia-conf'])

###############################################################
########### CREATE/EDIT  by using jinja templ. ################
###############################################################

VPRN_1002_CREATE = {
    'ns': _NS_MAP['nokia-conf'],
    'vprns': [
        {
            'operation': 'create',
            'service_name': '1002',
            'customer': '1',
            'as': '65502',
            'ecmp': '64',
            'rd': '65102:1002',
            'resolution': 'any',
            'interfaces': [
                {
                    'operation': 'create',
                    'name': 'myint',
                    'state': 'enable',
                    'ipv4_address': '10.10.20.2',
                    'ipv4_mask': '29'
                }
            ]
        }
    ]
}

VPRN_1002_DELETE = {
    'ns': _NS_MAP['nokia-conf'],
    'vprns': [
        {
            'operation': 'delete',
            'service_name': '1002',
            'customer': '1',
            'interfaces': [
                {
                    'operation': 'delete',
                    'name': 'myint',
                }
            ]
        }
    ]
}

VPRN_1005_CREATE_SR1 = {
    'ns': _NS_MAP['nokia-conf'],
    'vprns': [
        {
            'operation': 'create',
            'service_name': '1005',
            'customer': '1',
            'state': 'enable',
            'as': '65101',
            'ecmp': '64',
            'rd': '65101:1005',
            'resolution': 'any',
            'interfaces': [
                {
                    'operation': 'create',
                    'state': 'enable',
                    'name': 'to_sr2',
                    'ipv4_address': '10.0.0.0',
                    'ipv4_mask': '31',
                    'sap': '1/1/c2/1'
                },
                {
                    'operation': 'create',
                    'state': 'enable',
                    'name': 'lo0',
                    'loopback': 'TRUE',
                    'ipv4_address': '1.1.1.1',
                    'ipv4_mask': '32'
                }
            ],
            'bgp': {
              'import_policy': 'default-bgp-accept',
              'export_policy': 'default-bgp-accept',
              'state': 'enable',
              'groups': [
                  {
                      'name': 'to_SR2_1005',
                      'type': 'external',
                      'family': 'ipv4',
                      'local_as': '65101'
                  }
              ],
            'neighbors': [
                {
                    'address': '10.0.0.1',
                    'group': 'to_SR2_1005',
                    'peer_as': '65102'
                }
              ],
          }
        }
    ]
}

VPRN_1005_DELETE_SR1 = {
    'ns': _NS_MAP['nokia-conf'],
    'vprns': [
        {
            'operation': 'delete',
            'service_name': '1005',
            'customer': '1',
            'interfaces': [
                {
                    'operation': 'delete',
                    'name': 'to_sr2',
                },
                {
                    'operation': 'delete',
                    'name': 'lo0',
                }
            ]
        }
    ]
}

VPRN_1005_CREATE_SR2 = {
    'ns': _NS_MAP['nokia-conf'],
    'vprns': [
        {
            'operation': 'create',
            'service_name': '1005',
            'customer': '1',
            'state': 'enable',
            'as': '65102',
            'ecmp': '64',
            'rd': '65102:1005',
            'resolution': 'any',
            'interfaces': [
                {
                    'operation': 'create',
                    'state': 'enable',
                    'name': 'to_sr1',
                    'ipv4_address': '10.0.0.1',
                    'ipv4_mask': '31',
                    'sap': '1/1/c2/1'
                },
                {
                    'operation': 'create',
                    'state': 'enable',
                    'name': 'lo0',
                    'loopback': 'TRUE',
                    'ipv4_address': '2.2.2.2',
                    'ipv4_mask': '32'
                }
            ],
            'bgp': {
              'import_policy': 'default-bgp-accept',
              'export_policy': 'default-bgp-accept',
              'state': 'enable',
              'groups': [
                  {
                      'name': 'to_SR1_1005',
                      'type': 'external',
                      'family': 'ipv4',
                      'local_as': '65102'
                  }
              ],
            'neighbors': [
                {
                    'address': '10.0.0.0',
                    'group': 'to_SR1_1005',
                    'peer_as': '65101'
                }
              ],
          }
        }
    ]
}

VPRN_1005_DELETE_SR2 = {
    'ns': _NS_MAP['nokia-conf'],
    'vprns': [
        {
            'operation': 'delete',
            'service_name': '1005',
            'customer': '1',
            'interfaces': [
                {
                    'operation': 'delete',
                    'name': 'to_sr2',
                },
                {
                    'operation': 'delete',
                    'name': 'lo0',
                }
            ]
        }
    ]
}

PORT_CREATE_SR1 = {
    'ns': _NS_MAP['nokia-conf'],
    'ports': [
        {
            'operation': 'create',
            'state': 'enable',
            'id': '1/1/c2',
            'connector': 'breakout',
            'connector_type': 'c1-100g'
        },
        {
            'operation': 'create',
            'state': 'enable',
            'id': '1/1/c2/1',
            'ethernet_mode': 'access'
        },
    ]
}

PORT_DELETE_SR1 = {
    'ns': _NS_MAP['nokia-conf'],
    'ports': [
        {
            'operation': 'delete',
            'id': '1/1/c2'
        },
        {
            'operation': 'delete',
            'id': '1/1/c2/1'
        },
    ]
}

PORT_CREATE_SR2 = {
    'ns': _NS_MAP['nokia-conf'],
    'ports': [
        {
            'operation': 'create',
            'state': 'enable',
            'id': '1/1/c2',
            'connector': 'breakout',
            'connector_type': 'c1-100g'
        },
        {
            'operation': 'create',
            'state': 'enable',
            'id': '1/1/c2/1',
            'ethernet_mode': 'access'
        },
    ]
}

PORT_DELETE_SR2 = {
    'ns': _NS_MAP['nokia-conf'],
    'ports': [
        {
            'operation': 'delete',
            'id': '1/1/c2'
        },
        {
            'operation': 'delete',
            'id': '1/1/c2/1'
        },
    ]
}
###############################################################
################### CREATE/EDIT examples XML ##################
###############################################################
VPRN_CREATE_1002 = '''
<config>
  <configure xmlns="%s">
    <service>
      <vprn operation="replace">
        <service-name>1002</service-name>
        <customer>1</customer>
        <autonomous-system>65502</autonomous-system>
        <ecmp>64</ecmp>
        <route-distinguisher>65102:20</route-distinguisher>
        <auto-bind-tunnel>
          <resolution>any</resolution>
        </auto-bind-tunnel>
        <interface operation="replace">
          <interface-name>myint</interface-name>
          <admin-state>enable</admin-state>
          <tunnel>true</tunnel>
          <ipv4>
            <addresses>
              <address>
                <ipv4-address>10.10.20.3</ipv4-address>
                <prefix-length>29</prefix-length>
              </address>
            </addresses>
          </ipv4>
        </interface>
      </vprn>
    </service>
  </configure>
</config>
''' % (_NS_MAP['nokia-conf'])
VPRN_DELETE_1002 = '''
<config>
  <configure xmlns="%s">
    <service>
      <vprn operation="delete">
        <service-name>1002</service-name>
        <customer>1</customer>
        <autonomous-system>65502</autonomous-system>
        <ecmp>64</ecmp>
        <route-distinguisher>65102:20</route-distinguisher>
        <auto-bind-tunnel>
          <resolution>any</resolution>
        </auto-bind-tunnel>
        <interface operation="delete">
          <interface-name>myint</interface-name>
          <admin-state>enable</admin-state>
          <tunnel>true</tunnel>
          <ipv4>
            <addresses>
              <address>
                <ipv4-address>10.10.20.2</ipv4-address>
                <prefix-length>29</prefix-length>
              </address>
            </addresses>
          </ipv4>
        </interface>
      </vprn>
    </service>
  </configure>
</config>
''' % (_NS_MAP['nokia-conf'])


DEFAULT_BGP_POLICY_CREATE = '''
<config>
  <configure xmlns="%s">
    <policy-options>
        <policy-statement operation="create">
            <name>default-bgp-accept</name>
            <default-action>
                <action-type>accept</action-type>
            </default-action>
        </policy-statement>
    </policy-options>
  </configure>
</config>
''' % (_NS_MAP['nokia-conf'])

DEFAULT_BGP_POLICY_DELETE = '''
<config>
  <configure xmlns="%s">
    <policy-options>
        <policy-statement operation="delete">
            <name>default-bgp-accept</name>
            <default-action>
                <action-type>accept</action-type>
            </default-action>
        </policy-statement>
    </policy-options>
  </configure>
</config>
''' % (_NS_MAP['nokia-conf'])

VPRN_CREATE_1005 = '''
<config>
  <configure xmlns="%s">
    <service>
        <vprn operation="create">
          <service-name>1005</service-name>
          <admin-state>enable</admin-state>
          <customer>1</customer>
          <autonomous-system>65101</autonomous-system>
          <route-distinguisher>65101:1005</route-distinguisher>
          <auto-bind-tunnel>
            <resolution>any</resolution>
          </auto-bind-tunnel>
          <bgp>
            <admin-state>enable</admin-state>
            <ebgp-default-reject-policy>
              <import>false</import>
              <export>false</export>
            </ebgp-default-reject-policy>
            <import>
              <policy>default-bgp-accept</policy>
            </import>
            <export>
              <policy>default-bgp-accept</policy>
            </export>
            <group>
              <group-name>to_SR2_1005</group-name>
              <type>external</type>
              <family>
                <ipv4>true</ipv4>
              </family>
              <local-as>
                <as-number>65101</as-number>
              </local-as>
            </group>
            <neighbor>
              <ip-address>10.0.0.1</ip-address>
              <group>to_SR2_1005</group>
              <peer-as>65102</peer-as>
            </neighbor>
          </bgp>
          <interface operation="create">
            <interface-name>lo0</interface-name>
            <loopback>true</loopback>
            <admin-state>enable</admin-state>
            <ipv4>
              <primary>
                <address>1.1.1.1</address>
                <prefix-length>32</prefix-length>
              </primary>
            </ipv4>
          </interface>
          <interface operation="create">
            <interface-name>to_sr2</interface-name>
            <admin-state>enable</admin-state>
            <ipv4>
              <primary>
                <address>10.0.0.0</address>
                <prefix-length>31</prefix-length>
              </primary>
            </ipv4>
            <sap>
              <sap-id>1/1/c2/1</sap-id>
            </sap>
          </interface>
        </vprn>
    </service>
  </configure>
</config>
''' % (_NS_MAP['nokia-conf'])


###############################################################
##################### STATE  examples #########################
###############################################################

STATE_ROUTER = '''
<state xmlns="%s">
  <router>
    <router-name>Base</router-name>
      <route-table>
        <unicast>
            <ipv4>
              <route>
              </route>
            </ipv4>
        </unicast>
      </route-table>
  </router>
</state>
''' % (_NS_MAP['nokia-state'])

STATE_ROUTER_1005 = '''
<state xmlns="%s">
  <service>
    <vprn>
      <service-name>1005</service-name>
        <route-table>
          <unicast>
              <ipv4>
                <route>
                </route>
              </ipv4>
          </unicast>
        </route-table>
    </vprn>
  </service>
</state>
''' % (_NS_MAP['nokia-state'])


STATE_ALL = '''
<state xmlns="%s">
</state>
''' % (_NS_MAP['nokia-state'])

###############################################################
######### STATE  examples with string formatting ##############
###############################################################

STATE_VPRN_ROUTE_TABLE = '''
<state xmlns="%s">
  <service>
    <vprn>
      <service-name>{vprn}</service-name>
        <route-table>
          <unicast>
              <ipv4>
                <route>
                </route>
              </ipv4>
          </unicast>
        </route-table>
    </vprn>
  </service>
</state>
''' % (_NS_MAP['nokia-state'])

STATE_VPRN_BGP = '''
<state xmlns="%s">
  <service>
    <vprn>
      <service-name>{vprn}</service-name>
        <bgp>
        </bgp>
    </vprn>
  </service>
</state>
''' % (_NS_MAP['nokia-state'])