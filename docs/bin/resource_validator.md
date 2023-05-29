#


### main
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/resource_validator.py/#L5)
```python
.main(
   security_checks_yaml, output_json_report
)
```

---
Collect responses from required security scans and return.


**Args**

* **security_checks_yaml**  : A json document containing all security checks to be run.
* **output_json_report**  : A json document containing all resources and configuration settings


**Returns**

List of insecure resources.

----


### do_check
[source](https://github.com/tjtharrison/pytmac/blob/main/./bin/resource_validator.py/#L34)
```python
.do_check(
   output_json_report, check_details
)
```

---
Look up a check type in security_checks.json and checks resources using a given function.

Insecure resources are returned in the format:

[{
"name": [The name of the check],
"resource": [List of non-compliant resources],
"description": [Description of what the check does],
"check_query": [The query that returns True to generate this vulnerability type],
"remediation": [Steps that should be taken to remediate the concern],
"severity": [1-4 score on the impact of the insecurity]
---
}]


**Args**

* **output_json_report**  : The json report of resources and configuration
* **check_details**  : A json containing the details for the check to run.


**Returns**

list(dict)
