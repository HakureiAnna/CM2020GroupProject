pipeline {
	agent any
	
	stages {
		stage('pull') {
			steps {
				echo 'pulled from GitHub'
			}
		}
		stage('build') {
			steps {			
				bat mkdir \"caldown/dbserver/data\"
				bat 'docker compose -f caldown/docker-compose.yaml up --build -d'
				sleep 25
			}
		}
		stage('test') {
			steps {
				bat 'pytest "caldown/backend/tests"'
			}
		} 
		stage('cleanup') {
			steps {
				bat rmdir \"caldown/dbserver/data\" /S /Q
				bat 'docker compose down'
				bat 'docker system prune'
			}
		}
	}
}