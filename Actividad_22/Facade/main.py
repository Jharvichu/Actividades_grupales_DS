import json
from pathlib import Path


class StorageBucketModule:
    def __init__(self, name_base, buckets_dir="./buckets"):
        self.name = f"{name_base}-storage-bucket"
        self.buckets_dir = buckets_dir

    def resource(self):
        return {
            "null_resource": {
                "storage_bucket": {
                    "triggers": {"name": self.name},
                    "provisioner": [{
                        "local-exec": {
                            "interpreter": ["python", "-c"],
                            "command": (
                                f"import pathlib; "
                                f"pathlib.Path(r'{self.buckets_dir}/{self.name}').mkdir(parents=True, exist_ok=True)"
                            )
                        }
                    }]
                }
            }
        }

    def outputs(self):
        return {"name": self.name}


class StorageBucketAccessModule:
    def __init__(self, bucket_facade, entity, role):
        self.bucket = bucket_facade
        self.entity = entity
        self.role = role

    def resource(self):
        return {
            "null_resource": {
                "bucket_access": {
                    "triggers": {
                        "bucket": self.bucket["name"],
                        "entity": self.entity,
                        "role": self.role
                    },
                    "depends_on": ["null_resource.storage_bucket"],
                    "provisioner": [{
                        "local-exec": {
                            "interpreter": ["python", "-c"],
                            "command": (
                                f"print('Acceso aplicado al bucket {self.bucket['name']}')"
                            )
                        }
                    }]
                }
            }
        }

# nueva clase
class moduloFacade:
    def __init__(self, name_base, entity, role):
        self.bucket_module = StorageBucketModule(name_base)
        self.bucket_access_module = StorageBucketAccessModule(self.bucket_module.outputs(), entity, role)

    def generate(self):
        with open("bucket.tf.json", "w", encoding="utf-8") as f:
            json.dump({"resource": self.bucket_module.resource()}, f, indent=2)
        with open("bucket_access.tf.json", "w", encoding="utf-8") as f:
            json.dump({"resource": self.bucket_access_module.resource()}, f, indent=2)
        facade_outputs = {
            "output": {
                "bucket_name": {"value": self.bucket_module.name},
                "access_entity": {"value": entity},
                "access_role": {"value": role}
            }
        }
        with open("facade.tf.json", "w", encoding="utf-8") as f:
            json.dump(facade_outputs, f, indent=2)


'''
if __name__ == "__main__":
    bucket_mod = StorageBucketModule("hello-world")
    bucket_facade = bucket_mod.outputs()

    access_mod = StorageBucketAccessModule(
        bucket_facade, "allAuthenticatedUsers", "READER"
    )

    Path(".").mkdir(exist_ok=True)

    with open("bucket.tf.json", "w", encoding="utf-8") as f:
        json.dump({"resource": bucket_mod.resource()}, f, indent=2)

    with open("bucket_access.tf.json", "w", encoding="utf-8") as f:
        json.dump({"resource": access_mod.resource()}, f, indent=2)

    provider_conf = {
        "terraform": {
            "required_providers": {
                "null": {
                    "source": "hashicorp/null",
                    "version": "~> 3.2"
                }
            }
        },
        "provider": {
            "null": {}
        }
    }
    with open("provider.tf.json", "w", encoding="utf-8") as f:
        json.dump(provider_conf, f, indent=2)
'''

if __name__ == "__main__":
    Path(".").mkdir(exist_ok=True)
    # param
    name_base = "hello-world"
    entity = "allAuthenticatedUsers"
    role = "READER"
    # facade
    facade = moduloFacade(name_base, entity, role)
    facade.generate()

    provider_conf = {
        "terraform": {
            "required_providers": {
                "null": {
                    "source": "hashicorp/null",
                    "version": "~> 3.2"
                }
            }
        },
        "provider": {
            "null": {}
        }
    }
    with open("provider.tf.json", "w", encoding="utf-8") as f:
        json.dump(provider_conf, f, indent=2)