CREATE TABLE users (
	id VARCHAR(36) PRIMARY KEY,
	username VARCHAR(20),
	password VARCHAR(256),
	datecreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	datelastloggedin TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	status INT NOT NULL
);

CREATE TABLE profiles(
	id VARCHAR(36) PRIMARY KEY,
	age INT NOT NULL,
	weight INT NOT NULL,
	height INT NOT NULL,
	gender INT NOT NULL,
	userid VARCHAR(36),
	datecreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (userid) REFERENCES users(id) ON DELETE CASCADE
);
	

INSERT INTO users(id, username, password, status)
VALUES
(UUID(), 'testuser', (SHA2(CONCAT('password'), 256)), 0);

INSERT INTO profile(id, age, weight, height, gender, userid) 
SELECT
	UUID(), 20, 50, 165, 1, id
FROM users 
WHERE username='testuser'
LIMIT 1;