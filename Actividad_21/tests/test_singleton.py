from iac_patterns.singleton import ConfigSingleton 
import datetime

def test_reset():
    c1 = ConfigSingleton("dev")
    created = c1.created_at
    c1.settings["x"] = 1
    c1.reset()
    assert c1.settings == {}
    assert c1.created_at == created

if __name__ == "__main__":
    test_reset()