# pattern readwrite locator/{locator mqtt id}/ip
```json
{"ip_addresses":["192.168.1.1/24"]}
```
# pattern readwrite door/{door mqtt id}/display_name
```json
"Door 1"
```
This is a JSON formatted string, not a raw string.
# pattern readwrite door/{door mqtt id}/presence
```json
true
```
The JSON object is parsed into a python structure and converted to a boolean. `1` and `0` or non-empty vs empty strings should work as well.
# pattern readwrite door/{door mqtt id}/open
```json
{"not_after": 123456789}
```
not_after is a UNIX timestamp in seconds, indicating when the open request expires.
# pattern readwrite door/{door mqtt id}/open/confirm
