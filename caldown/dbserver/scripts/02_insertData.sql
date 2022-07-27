

INSERT INTO users(id, username, password, status)
VALUES
(UUID(), 'testuser', (SHA2(CONCAT('password'), 256)), 0);

INSERT INTO profile(id, age, weight, height, gender, userid) 
SELECT
	UUID(), 20, 50, 165, 1, id
FROM users 
WHERE username='testuser'
LIMIT 1;