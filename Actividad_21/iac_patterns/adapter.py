# adapter.py
class MockBucketAdapter:
    def __init__(self, null_block: dict):
        self.null = null_block

    def to_bucket(self) -> dict:
        # Mapear triggers a parámetros de bucket simulado
        null_resource_list = self.null["resource"][0]["null_resource"][0]
        name = list(null_resource_list.keys())[0]
        triggers = null_resource_list[name][0]["triggers"]

        return {
            "resource": [{
                "mock_cloud_bucket": [{
                    name: [{
                        "triggers": triggers
                    }]
                }]
            }]
        }