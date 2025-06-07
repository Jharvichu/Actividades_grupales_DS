# adapter.py
class MockBucketAdapter:
    def __init__(self, null_block: dict):
        self.null = null_block

    def to_bucket(self) -> dict:
        # Mapear triggers a parámetros de bucket simulado
        name = list(self.null["resource"]["null_resource"].keys())[0]
        return {
            "resource": {
                "mock_cloud_bucket": {
                    name: {"name": name, **self.null["resource"]["null_resource"][name]["triggers"]}
                }
            }
        }