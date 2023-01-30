CREATE DATABASE if not exists movies;
use movies;
drop table if exists movie;

CREATE TABLE movie (
  id int NOT NULL AUTO_INCREMENT,
  nombre varchar(255),
  descripcion varchar(5000),
  genero varchar(5000),
  image varchar(5000),
  PRIMARY KEY (id)
);