CREATE TABLE users (
	id VARCHAR(36) PRIMARY KEY,
	username VARCHAR(20) NOT NULL,
	password VARCHAR(256) NOT NULL,
	datecreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	datelastmodified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	status INT NOT NULL
);

CREATE TABLE profiles(
	id VARCHAR(36) PRIMARY KEY,
	age INT NOT NULL,
	weight INT NOT NULL,
	height INT NOT NULL,
	gender VARCHAR(20) NOT NULL,
	goal VARCHAR(20) NOT NULL,
	userid VARCHAR(36) NOT NULL,
	datecreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,	
	FOREIGN KEY (userid) REFERENCES users(id) ON DELETE CASCADE
);
		
CREATE TABLE plans(
	id VARCHAR(36) PRIMARY KEY,
	breakfast_name VARCHAR(256) NOT NULL,
	breakfast_uri VARCHAR(512) NOT NULL,
	breakfast_image VARCHAR(512) NOT NULL,
	breakfast_calories INT NOT NULL,
	lunch_name VARCHAR(256) NOT NULL,
	lunch_uri VARCHAR(512) NOT NULL,
	lunch_image VARCHAR(512) NOT NULL,
	lunch_calories INT NOT NULL,
	dinner_name VARCHAR(256) NOT NULL,
	dinner_uri VARCHAR(512) NOT NULL,
	dinner_image VARCHAR(512) NOT NULL,
	dinner_calories INT NOT NULL,
	userid VARCHAR(36) NOT NULL,
	datecreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	dateplanned DATE NOT NULL,
	FOREIGN KEY (userid) REFERENCES users(id) ON DELETE CASCADE
);