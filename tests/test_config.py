import io
import yaml
import pytest


REQUIRED_REDIS_KEYS = {"host", "port", "db", "password"}
REQUIRED_S3_KEYS = {"aws_access_key_id", "aws_secret_access_key", "region_name", "bucket"}


def _load_yaml(text):
    return yaml.safe_load(io.StringIO(text))


def test_example_config_is_valid_yaml():
    with open("config.example.yaml", "r") as f:
        config = yaml.safe_load(f)
    assert config is not None


def test_example_config_has_redis_section():
    with open("config.example.yaml", "r") as f:
        config = yaml.safe_load(f)
    assert "redis" in config
    assert REQUIRED_REDIS_KEYS.issubset(config["redis"].keys())


def test_example_config_has_s3_section():
    with open("config.example.yaml", "r") as f:
        config = yaml.safe_load(f)
    assert "s3" in config
    assert REQUIRED_S3_KEYS.issubset(config["s3"].keys())


def test_valid_config_passes_validation():
    raw = """
redis:
  host: localhost
  port: 6379
  db: 0
  password: secret
s3:
  aws_access_key_id: AKIAIOSFODNN7EXAMPLE
  aws_secret_access_key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
  region_name: us-east-1
  bucket: my-bucket
"""
    config = _load_yaml(raw)
    assert config["redis"]["port"] == 6379
    assert config["s3"]["bucket"] == "my-bucket"


def test_config_missing_redis_key_detected():
    raw = """
redis:
  host: localhost
s3:
  aws_access_key_id: key
  aws_secret_access_key: secret
  region_name: us-east-1
  bucket: bucket
"""
    config = _load_yaml(raw)
    missing = REQUIRED_REDIS_KEYS - set(config["redis"].keys())
    assert missing == {"port", "db", "password"}
