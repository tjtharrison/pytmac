#


### resources
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/get_config.py/#L10)
```python
.resources(
   file
)
```

---
Return a list of resources to be included in the package.


**Args**

* **file**  : File to load resources from


**Returns**

List of resources


**Raises**

* **FileNotFoundError**  : If file is not found
* **YAMLError**  : If file is not valid YAML


----


### config
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/get_config.py/#L39)
```python
.config(
   file
)
```

---
Return a list of config to be included in the package.


**Args**

* **file**  : File to load resources from


**Returns**

List of resources


**Raises**

* **FileNotFoundError**  : If file is not found
* **YAMLError**  : If file is not valid YAML


----


### defaults
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/get_config.py/#L68)
```python
.defaults(
   file
)
```

---
Return a list of defaults to be included in the package.


**Args**

* **file**  : File to load resources from


**Returns**

List of resources


**Raises**

* **FileNotFoundError**  : If file is not found
* **YAMLError**  : If file is not valid YAML


----


### security_checks
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/get_config.py/#L97)
```python
.security_checks(
   file
)
```

---
Return a list of security_checks to be included in the package.


**Args**

* **file**  : File to load resources from


**Returns**

List of resources


**Raises**

* **FileNotFoundError**  : If file is not found
* **YAMLError**  : If file is not valid YAML


----


### swagger
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/get_config.py/#L131)
```python
.swagger(
   file
)
```

---
Get and return swagger file contents.


**Args**

* **file**  : File to load resources from


**Returns**

List of resources


**Raises**

* **FileNotFoundError**  : If file is not found
* **Exception**  : If file is not valid JSON


----


### settings
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/get_config.py/#L164)
```python
.settings()
```

---
Get and return settings file contents from .pytmac file.


**Returns**

settings file contents


**Raises**

* **FileNotFoundError**  : If file is not found
* **YAMLError**  : If file is not valid YAML

