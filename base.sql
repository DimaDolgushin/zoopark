CREATE TABLE post(
    id INTEGER NOT NULL PRIMARY KEY,
    name_post VARCHAR(100)  NOT NULL
);

CREATE TABLE users(
    id INTEGER NOT NULL PRIMARY KEY,
    login VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
);

CREATE TABLE Personnel(
    id INTEGER NOT NULL PRIMARY KEY,
    surname VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    patronymic VARCHAR(100) NOT NULL UNIQUE
    date_of_birth VARCHAR(100) NOT NULL,
    FOREIGN KEY(Post_id) REFERENCES post(id)
;)

CREATE TABLE Zoo(
    id INTEGER NOT NULL PRIMARY KEY,
    Title VARCHAR(100) NOT NULL,
    Phone VARCHAR(100) NOT NULL,
    City VARCHAR(100) NOT NULL,
);

CREATE TABLE Animals(
    id INTEGER NOT NULL PRIMARY KEY,
    Nickname VARCHAR(100) NOT NULL,
);

    Average_life_expectancy VARCHAR(100) NOT NULL,
    FOREIGN KEY(Homeland_id) REFERENCES Homeland(id)
                  ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY(Class_id) REFERENCES Class(id)
                  ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY(Zoo_id) REFERENCES Zoo(id)
                  ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY(Tickets_id) REFERENCES Tickets(id)
                  ON DELETE CASCADE ON UPDATE NO ACTION,
);

CREATE TABLE Class(
    id INTEGER NOT NULL PRIMARY KEY,
    Name_Class VARCHAR(100) NOT NULL,
);

CREATE TABLE Homeland(
    id INTEGER NOT NULL PRIMARY KEY,
    Name_Homeland VARCHAR(100) NOT NULL,
);

CREATE TABLE Tickets(
    id INTEGER NOT NULL PRIMARY KEY,
    Name_Tickets VARCHAR(100) NOT NULL,
);

INSERT INTO users(login, password)
VALUES ('login','password'),('login1','password1');

INSERT INTO post(Name_post)
VALUES ('Name_post'),('Name_post1');

INSERT INTO Personnel(Name, Surname, patronymic,date_of_birth,)
VALUES ('Name1','Surname1',',patronymic1','date_of_birth1');

INSERT INTO Animals(Nickname, Average_life_expectancy)
VALUES ('Nickname1', 'Average_life_expectancy1');

INSERT INTO Homeland(name_homeland)
VALUES ('name_homeland1');

INSERT INTO Class(Name_class)
VALUES ('Name_class1');

INSERT INTO Tickets(Name_Tickets)
VALUES ('Name_Tickets1');

INSERT INTO Zoo(Title, Phone, City,)
VALUES ('Title1','Phone1',',City1');
