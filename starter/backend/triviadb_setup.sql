DROP DATABASE IF EXISTS triviadb;
DROP USER IF EXISTS caryn0;
CREATE DATABASE triviadb;
CREATE USER caryn0 WITH ENCRYPTED PASSWORD 'student';
GRANT ALL PRIVILEGES ON DATABASE triviadb TO caryn0;
ALTER USER caryn0 CREATEDB;
ALTER USER caryn0 WITH SUPERUSER;