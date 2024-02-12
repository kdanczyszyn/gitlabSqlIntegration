import pytest
import unittest
from unittest.mock import MagicMock, patch
from merge_webhook import MergeRequest, SQLProcessingError
from cfg.database import SQLDatabase


class TestMergeRequestFunctions(unittest.TestCase):
    def test_write_to_database_success(self): 
        merge_request = MergeRequest({})
        with patch("cfg.database.SQLDatabase") as mock_sql_db:
            # SQLDatabase mock
            mock_db_instance = mock_sql_db.return_value
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db_instance.connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor

            test_files_path = '/path/gitlabSqlIntegration/tests/correct'
            
            merge_request._write_to_database(test_files_path, mock_db_instance)

            mock_conn.commit.assert_called_once()

    def test_write_to_database_error(self):
        merge_request = MergeRequest({})
        with patch("cfg.database.SQLDatabase") as mock_sql_db:
            # SQLDatabase mock
            mock_db_instance = mock_sql_db.return_value
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db_instance.connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = Exception("Test exception")

            test_files_path = '/path/gitlabSqlIntegration/tests/rollback'

            with self.assertRaises(SQLProcessingError):
                merge_request._write_to_database(test_files_path, mock_db_instance)

            mock_cursor.rollback.assert_called_once()
