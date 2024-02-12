IF EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'test_table')
INSERT INTO test_table
VALUES(
    1, 'Kamil'
),
(
    1, 'Aga'
)