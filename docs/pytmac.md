#


### main
[source](https://github.com/tjtharrison/pytmac/blob/main/./pytmac.py/#L93)
```python
.main(
   resources_yaml, config_yaml, defaults_yaml, security_checks_yaml, output_dir,
   swagger_json = ''
)
```

---
Primary function used to open up provided config and resource files, generating DFD and output.


**Args**

* **resources_yaml**  : The resources yaml file.
* **config_yaml**  : The config yaml file.
* **defaults_yaml**  : The defaults yaml file.
* **security_checks_yaml**  : The security checks yaml file.
* **output_dir**  : The output directory.
* **swagger_json**  : The swagger json file (Default value = "").


**Returns**

* **bool**  : The return value. True for success, False otherwise.

