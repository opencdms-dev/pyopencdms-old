-- Script below drops user with all objects.
-- drop user metadata cascade;

-- Script create user metadata.
create user metadata identified by metadata default tablespace source_data;
grant connect, resource to metadata;
