---
  - name: Gather device info from NetBox
    uri:
      url: "{{ netbox_url }}/api/dcim/devices/?name={{ inventory_hostname }}"
      method: GET
      validate_certs: false
      return_content: yes
      headers:
        accept: "application/json"
        Authorization: "Token {{ netbox_token }}"
    register: nb_device

  - name: Add zabbix hostasdasd
    local_action:
      module: zabbix_host
      server_url: "http://"
!      login_user: "admin"
!      login_password: "password"
      host_name: "{{ inventory_hostname }}"
      visible_name: "{{ nb_device.json.results[0].name }}"
      description: "{{ nb_device.json.results[0].name }}"
      host_groups:
        - ACCESS
      link_templates:
        - Template Net Juniper SNMPv2
      status: enabled
      state: present
      inventory_mode: automatic
      inventory_zabbix:
        tag: "{{ nb_device.json.results[0].name }}"
        alias: "{{ nb_device.json.results[0].name }}"
        model: "{{ nb_device.json.results[0].device_type.model }}"
        vendor: "{{ nb_device.json.results[0].device_type.manufacturer.name  }}"
      interfaces:
        - type: 2
          main: 1
          useip: 1
          ip: "{{ nb_device.json.results[0].primary_ip.address | ipaddr('address') }}"
          dns: "{{ inventory_hostname }}"
          port: 161
      macros:
        - macro: "{$SNMP_COMMUNITY}"
!          value: "community_string"
      tags:
        - tag: "TENANT"
          value: "SG"
