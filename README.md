## NETCONF example for Nokia SR

This repository includes Netconf example for Nokai SR.
* python `ncclient` is used for Netfonf implementation.
* `jinja2` templates is used to prepare XML format for Netconf requests.
* Tested with 20.5.R1 release.

__Repository includes:__
* `nc_edit_config` method to edit candidate config.
* `nc_get` method to receive configuration and state data.
* An example `vprn_test` method to create/delete example VPRN service (service-name=1002) and get configuration after create/delete operation.
* Another examples for creating VPRN service with BGP and get state data:
    * `vprn_bgp_config` method to create example VPRN service (service-name=1005) with BGP config.
    * `vprn_state method` to receive state data for VPRN (service-name=1005) created with above method.
    * `delete_vprn_config` to delete VPRN config (service-name=1005).
* Also example config and state date added to be example.
* Desired method can be run by uncommenting in the main method