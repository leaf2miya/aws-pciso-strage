import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src/handler"))

from lambda_function import lambda_handler


def _make_event(key):
    return {
        "Records": [
            {
                "s3": {
                    "object": {"key": key}
                }
            }
        ]
    }


@patch("lambda_function.boto3")
def test_normal_path(mock_boto3):
    mock_table = MagicMock()
    mock_boto3.resource.return_value.Table.return_value = mock_table

    with patch.dict(os.environ, {"DYNAMODB_TABLE": "test-table"}):
        lambda_handler(_make_event("acme/tool/file.txt"), None)

    mock_table.put_item.assert_called_once_with(
        Item={"company": "acme", "soft": "tool"}
    )


@patch("lambda_function.boto3")
def test_url_encoded_path(mock_boto3):
    mock_table = MagicMock()
    mock_boto3.resource.return_value.Table.return_value = mock_table

    with patch.dict(os.environ, {"DYNAMODB_TABLE": "test-table"}):
        lambda_handler(_make_event("acme/tool/file%20name.txt"), None)

    mock_table.put_item.assert_called_once_with(
        Item={"company": "acme", "soft": "tool"}
    )


@patch("lambda_function.boto3")
def test_invalid_path_raises(mock_boto3):
    mock_table = MagicMock()
    mock_boto3.resource.return_value.Table.return_value = mock_table

    with patch.dict(os.environ, {"DYNAMODB_TABLE": "test-table"}):
        with pytest.raises(ValueError):
            lambda_handler(_make_event("no-slash-file.txt"), None)
