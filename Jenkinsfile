pipeline {
	agent any
	
	stages {
		stage('pull') {
			steps {
			}
		}
		stage('build') {
			steps {			
				bat 'docker compose -f caldown/docker-compose.yaml up --build -d'
				sleep 45
			}
		}
		stage('test') {
			steps {
				bat 'pytest "caldown/backend/tests"'
			}
		} 
	}
}