import toml

from pip_check_updates.config import template, name


def test_constant():
    assert name == "pcufile.toml"
    assert template
    pcu_config = toml.loads(template)
    assert pcu_config["target"] == "latest"
    assert pcu_config["no_ssl_verify"] == False
    assert pcu_config["ignore_warning"] == False
    assert pcu_config["show_full_path"] == False
    assert pcu_config["upgrade"] == False
    assert pcu_config["no_color"] == False
    assert pcu_config["filter"] == []
    assert pcu_config["ignores"] == []
