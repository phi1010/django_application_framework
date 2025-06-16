# This file determines the data delivered to the RPi OPA client instances
package app.door_commander.door_authz

users_groups contains [dj_uid, kc_group] if {
    data.django.users[dj_uid]
    data.django.users[dj_uid].connections[_].fields.latest_directory_data.resource_access["sesam.zam.haus"].roles[_]=kc_group
}