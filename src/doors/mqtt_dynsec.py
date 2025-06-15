#"$CONTROL/dynamic-security/v1/response
"""
[
{
  "responses": [
    {
      "command": "getRole",
      "data": {
        "role": {
          "rolename": "admin",
          "acls": [
            {
              "acltype": "publishClientSend",
              "topic": "$CONTROL/dynamic-security/#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "publishClientSend",
              "topic": "#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "publishClientReceive",
              "topic": "$CONTROL/dynamic-security/#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "publishClientReceive",
              "topic": "$SYS/#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "publishClientReceive",
              "topic": "#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "subscribePattern",
              "topic": "$CONTROL/dynamic-security/#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "subscribePattern",
              "topic": "$SYS/#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "subscribePattern",
              "topic": "#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "unsubscribePattern",
              "topic": "#",
              "priority": 0,
              "allow": true
            }
          ]
        }
      }
    }
  ]
},
{"responses":[{"command":"listRoles","data":{"totalCount":1,"roles":["admin"]}}]}


]
"""