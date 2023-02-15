config = {
    "systems": {
        "public_facing": True,
        "has_waf": True,
        "requires_encryption": False,
        "requires_authentication": False,
        "has_secure_password_policy": False,
        "is_hardened": True,
    },
    "containers": {
        "public_facing": True,
        "has_waf": True,
        "requires_encryption": False,
        "requires_authentication": False,
        "has_secure_password_policy": False,
        "is_hardened": True,
    },
}

if (
    not config["containers"]["public_facing"]
    or not config["containers"]["has_waf"]
    or not config["containers"]["requires_encryption"]
):
    print("FAIL")
