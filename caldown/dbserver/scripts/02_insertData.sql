INSERT INTO users(id, username, password, status)
VALUES
(UUID(), 'testuser', (SHA2(CONCAT('password'), 256)), 0);

INSERT INTO profiles(id, age, weight, height, gender, goal, userid) 
SELECT
	UUID(), 20, 50, 165, 'male', 'balanced', id
FROM users 
WHERE username='testuser'
LIMIT 1;