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
				bat 'mkdir \"caldown/dbserver/data\"'
				bat 'docker compose -f caldown/docker-compose.yaml up --build -d'
				sleep 20
			}
		}
		stage('test') {
			steps {
				bat 'pytest "caldown/backend/tests"'
			}
		} 
		
		stage('cleanup') {
			steps {
				echo 'cleaning up'
			}
		}
	}
	post {	
		success {
			bat 'docker compose -f caldown/docker-compose.yaml down'
			bat 'rmdir \"caldown/dbserver/data\" /S /Q'
			bat 'docker system prune'
		}
	}			
}