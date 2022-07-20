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
				bat 'docker compose -f caldown/docker-compose.yaml up --build -d'
				sleep 25
			}
		}
		stage('test') {
			steps {
				bat 'pytest "caldown/backend/tests"'
			}
		} 
	}
}