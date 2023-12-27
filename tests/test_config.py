from pip_check_updates.config import name, template


def test_constant():
    assert name == "pcufile.toml"
    assert template
    assert template["target"] == "latest"
    assert template["no_ssl_verify"] == False
    assert template["ignore_warning"] == False
    assert template["show_full_path"] == False
    assert template["upgrade"] == False
    assert template["no_color"] == False
    assert template["no_recursive"] == False
    assert template["ignore_additional_labels"] == False
    assert template["filter"] == []
    assert template["ignores"] == []
    assert template["default_venv"] == ".venv"
