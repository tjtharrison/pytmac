#


### config
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/input_validator.py/#L7)
```python
.config(
   config_json
)
```

---
Validate required fields in config.json.


**Args**

* **config_json**  : Json structure containing the app running config


**Returns**

True/False

----


### resources
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/input_validator.py/#L39)
```python
.resources(
   resources_json
)
```

---
Validate required fields in resources.json.


**Args**

* **resources_json**  : Json structure containing the app resources


**Returns**

True/False

----


### defaults
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/input_validator.py/#L145)
```python
.defaults(
   defaults_json
)
```

---
Validate required fields set in defaults.json.


**Args**

* **defaults_json**  : Json structure containing resource defaults


**Returns**

* **bool**  : True/False


----


### swagger
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/input_validator.py/#L166)
```python
.swagger(
   swagger_json
)
```

---
Validate required fields set in swagger.json (If ENABLE_SWAGGER is set to True).


**Args**

* **swagger_json**  : Json structure containing swagger file contents


**Returns**

True/False
