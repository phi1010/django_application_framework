package app.door_commander.ldap

queries.users contains {"query":query_pattern, "variables":variables, "attributes":attributes} if {
    query_pattern := "(&(objectClass=inetOrgPerson)(entryUUID={uuid}))"
    uuid := data.django.users[django_id].connections[connection_idx].fields.directory_key
    variables := {"uuid": uuid}
    attributes := ["entryUUID", "memberOf", "uid", "cn", "objectClass"]
}

queries.groups contains {"query":query_pattern, "variables":variables, "attributes":attributes} if {
    query_pattern := "(&(objectClass=groupOfNames)(cn=*))"
    uuid := data.django.users[django_id].connections[connection_idx].fields.directory_key
    variables := {}
    attributes := ["entryUUID", "member", "cn", "objectClass"]
}
