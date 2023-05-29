#


### get_inputs
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/init.py/#L10)
```python
.get_inputs()
```

---
Get user input for project configuration.


**Returns**

Dictionary with user input


**Raises**

* **KeyboardInterrupt**  : if user cancels input


----


### create_directory
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/init.py/#L38)
```python
.create_directory(
   name
)
```

---
Create a directory if it does not exist.


**Args**

* **name**  : Name of directory to create


**Returns**

True if directory was created, False if it already exists


**Raises**

* **OSError**  : if directory cannot be created


----


### create_config_file
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/init.py/#L63)
```python
.create_config_file(
   project_config
)
```

---
Create a config file for the project with user provided values.


**Args**

* **project_config**  : User provided input for project.


**Returns**

True if config file was created


**Raises**

* **OSError**  : if config file cannot be loaded
* **YAMLError**  : if values cannot be updated
* **KeyError**  : if config file cannot be created


----


### create_defaults_file
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/init.py/#L103)
```python
.create_defaults_file(
   project_config
)
```

---
Create a defaults file for the project.


**Args**

* **project_config**  : User provided input for project.


**Returns**

True if defaults file was created


**Raises**

* **OSError**  : if defaults file cannot be loaded
* **YAMLError**  : if values cannot be updated


----


### return_summary
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/init.py/#L129)
```python
.return_summary(
   project_config
)
```

---
Return a summary of the project configuration.


**Args**

* **project_config**  : User provided input for project.


**Returns**

True if summary was returned

----


### create_resources_file
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/init.py/#L156)
```python
.create_resources_file(
   project_config, all_resources
)
```

---
Create a resources file for the project.


**Args**

* **project_config**  : User provided input for project.
* **all_resources**  : json file with all resources


**Returns**

True if resources file was created


**Raises**

* **OSError**  : if resources file cannot be loaded
* **YAMLError**  : if values cannot be updated


----


### get_networks
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/init.py/#L183)
```python
.get_networks()
```

---
Get networks for project configuration.


**Returns**

List of networks

----


### get_users
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/init.py/#L220)
```python
.get_users(
   network, users
)
```

---
Get users for project configuration.


**Args**

* **network**  : Name of network
* **users**  : List of users already added


**Returns**

List of users

----


### get_databases
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/init.py/#L257)
```python
.get_databases(
   network, databases
)
```

---
Get databases for project configuration.


**Args**

* **network**  : Name of network
* **databases**  : List of databases already added


**Returns**

list of databases

----


### get_systems
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/init.py/#L298)
```python
.get_systems(
   network, systems
)
```

---
Get systems for project configuration.


**Args**

* **network**  : Name of network
* **systems**  : List of systems already added


**Returns**

list of systems

----


### get_resource_names
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/init.py/#L337)
```python
.get_resource_names(
   all_resources
)
```

---
Get all resource names from all_resources.


**Args**

* **all_resources**  : json file with all resources


**Returns**

List of resource names

----


### get_links
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/init.py/#L356)
```python
.get_links(
   all_resource_names
)
```

---
Get links for project configuration.


**Args**

* **all_resource_names**  : List of all resource names


**Returns**

List of links

----


### create_settings_file
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/init.py/#L408)
```python
.create_settings_file(
   project_config
)
```

---
Create settings file for project.


**Args**

* **project_config**  : Project configuration


**Returns**

True if successful, False otherwise


**Raises**

* **OSError**  : If unable to create settings file

