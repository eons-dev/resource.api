# APIE Resource Endpoint

An apie resource is the primary component of the [Resource Paradigm](https://github.com/eons-dev/bin_apie/#resource-paradigm).

Resources represent data structures which can be manipulated. The means of manipulating such data are called "operations".
Each resource must specify a map of operations and their associated implementations. For example, a CRUD resource might have:
```python
operations = {
    'create': 'create_implementation_database',
    'read': 'read_implementation_database',
    'update': 'update_implementation_database',
    'delete': 'create_implementation_database'
}
```
Each implementation is injected into the apie list of Endpoints to process directly after *this and before the specified operation.
Only the specified operations will be allowed.

When creating a resource, specify its class name as the name of the resource. For example:
```python
from api_resource import resource
class user(resource):
	def __init__(this, name="user resource"):
		super().__init__(name)
```

NOTE: If you are using the `v1` Endpoint, you do not need to create separate classes for each resource. See [the docs for v1](https://github.com/infrastructure-tech/api_v1) for more info.