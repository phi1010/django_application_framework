package app.door_commander.sidecar.ldap_export_test


import data.app.door_commander.sidecar.ldap_export.door_entry_uuid_mapping



test_non_membership if {
    not door_entry_uuid_mapping[""] with input as {} with data.ldap as door_entry_uuid_mapping
}

test_direct_membership if {
    # "ED9AE67F-0779-4248-AE46-0167791A73AF" : ["MayOpenNordUG"],
    # "MayOpenNordUG" : ["zugangsberechtigt_nord_ug",],
    # "entryUUID": [
          #          "dfb835dc-e8a5-103f-9f86-7d53f788cc3b"
          #        ],
          #        "memberOf": [
          #          "cn=mitglied,ou=groups,dc=betreiberverein,dc=de",
          #          "cn=zugangsberechtigt_nord_eg,ou=groups,dc=betreiberverein,dc=de",
          #          "cn=zugangsberechtigt_nord_ug,ou=groups,dc=betreiberverein,dc=de"
          #        ],

    "dfb835dc-e8a5-103f-9f86-7d53f788cc3b" in door_entry_uuid_mapping["ED9AE67F-0779-4248-AE46-0167791A73AF"] with input as {} with data.ldap as demo_ldap_data
}
test_recursive_membership if {
    # "D6545C11-CC5A-421E-9D7D-0B2F762C6282" : ["MayOpenFrontDoor"],
    #  "MayOpenFrontDoor" : ["zugangsberechtigt",],
    # "entryUUID": [
          #          "dfb835dc-e8a5-103f-9f86-7d53f788cc3b"
          #        ],
          #        "memberOf": [
          #          "cn=mitglied,ou=groups,dc=betreiberverein,dc=de",
          #          "cn=zugangsberechtigt_nord_eg,ou=groups,dc=betreiberverein,dc=de",
          #          "cn=zugangsberechtigt_nord_ug,ou=groups,dc=betreiberverein,dc=de"
          #        ],

    "dfb835dc-e8a5-103f-9f86-7d53f788cc3b" in door_entry_uuid_mapping["D6545C11-CC5A-421E-9D7D-0B2F762C6282"] with input as {} with data.ldap as demo_ldap_data
}











demo_ldap_data := {
  "groups": [
    {
      "attributes": {
        "cn": [
          "emptygroup"
        ],
        "entryUUID": [
          "dfba0df8-e8a5-103f-9f88-7d53f788cc3b"
        ],
        "memberOf": [],
        "objectClass": [
          "groupOfUniqueNames"
        ],
        "uniqueMember": [
          "cn=empty-membership-placeholder"
        ]
      },
      "dn": "cn=emptygroup,ou=groups,dc=betreiberverein,dc=de"
    },
    {
      "attributes": {
        "cn": [
          "mitglied"
        ],
        "entryUUID": [
          "dfba8120-e8a5-103f-9f89-7d53f788cc3b"
        ],
        "memberOf": [],
        "objectClass": [
          "groupOfUniqueNames"
        ],
        "uniqueMember": [
          "uid=user1,ou=users,dc=betreiberverein,dc=de",
          "uid=user2,ou=users,dc=betreiberverein,dc=de"
        ]
      },
      "dn": "cn=mitglied,ou=groups,dc=betreiberverein,dc=de"
    },
    {
      "attributes": {
        "cn": [
          "zugangsberechtigt_nord_eg"
        ],
        "entryUUID": [
          "dfbbae38-e8a5-103f-9f8a-7d53f788cc3b"
        ],
        "memberOf": [
          "cn=zugangsberechtigt,ou=groups,dc=betreiberverein,dc=de"
        ],
        "objectClass": [
          "groupOfUniqueNames"
        ],
        "uniqueMember": [
          "uid=user1,ou=users,dc=betreiberverein,dc=de",
          "uid=user2,ou=users,dc=betreiberverein,dc=de"
        ]
      },
      "dn": "cn=zugangsberechtigt_nord_eg,ou=groups,dc=betreiberverein,dc=de"
    },
    {
      "attributes": {
        "cn": [
          "zugangsberechtigt_nord_ug"
        ],
        "entryUUID": [
          "dfbcc0ac-e8a5-103f-9f8b-7d53f788cc3b"
        ],
        "memberOf": [
          "cn=zugangsberechtigt,ou=groups,dc=betreiberverein,dc=de"
        ],
        "objectClass": [
          "groupOfUniqueNames"
        ],
        "uniqueMember": [
          "uid=user1,ou=users,dc=betreiberverein,dc=de"
        ]
      },
      "dn": "cn=zugangsberechtigt_nord_ug,ou=groups,dc=betreiberverein,dc=de"
    },
    {
      "attributes": {
        "cn": [
          "zugangsberechtigt"
        ],
        "entryUUID": [
          "dfbd7b3c-e8a5-103f-9f8c-7d53f788cc3b"
        ],
        "memberOf": [],
        "objectClass": [
          "groupOfUniqueNames"
        ],
        "uniqueMember": [
          "cn=zugangsberechtigt_nord_eg,ou=groups,dc=betreiberverein,dc=de",
          "cn=zugangsberechtigt_nord_ug,ou=groups,dc=betreiberverein,dc=de"
        ]
      },
      "dn": "cn=zugangsberechtigt,ou=groups,dc=betreiberverein,dc=de"
    }
  ],
  "users": [
    {
      "attributes": {
        "cn": [
          "Vorname1"
        ],
        "entryUUID": [
          "dfb835dc-e8a5-103f-9f86-7d53f788cc3b"
        ],
        "memberOf": [
          "cn=mitglied,ou=groups,dc=betreiberverein,dc=de",
          "cn=zugangsberechtigt_nord_eg,ou=groups,dc=betreiberverein,dc=de",
          "cn=zugangsberechtigt_nord_ug,ou=groups,dc=betreiberverein,dc=de"
        ],
        "objectClass": [
          "inetOrgPerson",
          "organizationalPerson"
        ],
        "uid": [
          "user1"
        ]
      },
      "dn": "uid=user1,ou=users,dc=betreiberverein,dc=de"
    },
    {
      "attributes": {
        "cn": [
          "Vorname2"
        ],
        "entryUUID": [
          "dfb9395a-e8a5-103f-9f87-7d53f788cc3b"
        ],
        "memberOf": [
          "cn=mitglied,ou=groups,dc=betreiberverein,dc=de",
          "cn=zugangsberechtigt_nord_eg,ou=groups,dc=betreiberverein,dc=de"
        ],
        "objectClass": [
          "inetOrgPerson",
          "organizationalPerson"
        ],
        "uid": [
          "user2"
        ]
      },
      "dn": "uid=user2,ou=users,dc=betreiberverein,dc=de"
    }
  ]
}
