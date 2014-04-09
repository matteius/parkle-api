^^^^^^^^^^^^^^^
Database
^^^^^^^^^^^^^^^

    # SQL create database
    CREATE DATABASE parkledb CHARACTER SET = 'utf8';

    # create user
    CREATE USER 'parkle'@'%' IDENTIFIED BY 'parkle123';

    # give permissions
    GRANT ALL PRIVILEGES ON parkledb.* TO 'parkle'@'%';

    FLUSH PRIVILEGES;
