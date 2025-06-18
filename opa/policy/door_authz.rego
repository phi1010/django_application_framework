# This file determines the data delivered to the RPi OPA client instances
package app.door_commander.door_authz

keycloak_users_groups contains {"django_user_uuid":dj_uuid, "keycloak_group_claim":kc_group} if {
    data.django.users[dj_uuid]
    data.django.users[dj_uuid].connections[_].fields.latest_directory_data.resource_access["sesam.zam.haus"].roles[_]=kc_group
}

ldap_users_groups contains {"ldap_user_uuid":ldap_uuid, "ldap_group_cn":ldap_group} if {
    user_dn = data.ldap.users[user_idx].dn
    ldap_uuid = data.ldap.users[user_idx].attributes.entryUUID[_]
    ldap_group = data.ldap.groups[group_idx].attributes.cn[_]
    data.ldap.groups[group_idx].attributes.member[_] = user_dn
}