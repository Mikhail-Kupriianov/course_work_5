CREATE TABLE employers
(
    employer_id varchar(10) PRIMARY KEY,
    employer_name varchar(100) NOT NULL
);

CREATE TABLE vacancies
(
    vacancy_id varchar(10) PRIMARY KEY,
	employer_id varchar(10) NOT NULL,
    vacancy_name varchar(150) NOT NULL,
	url text NOT NULL,
	area varchar(100) NOT NULL,
	salary int
)