drop table if exists USER_DATA;
create table USER_DATA(
    ID int unsigned NOT NULL auto_increment,
    FIRST_NAME varchar(20) not null,
    LAST_NAME varchar(10) not null,
    EMAIL_ID varchar(30) not null,
    PASSWORD varchar(30) not null,
    CONTACT_NUMBER varchar(12) not null,
    PRIMARY KEY (id)) ENGINE = InnoDB default character set utf8 collate utf8_general_ci;

