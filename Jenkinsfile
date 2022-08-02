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
				sleep 10
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
			sleep 120
			bat 'docker compose -f caldown/docker-compose.yaml down'
			bat 'rmdir \"caldown/dbserver/data\" /S /Q'
			bat 'docker system prune'
			bat 'mkdir \"caldown/dbserver/data\"'
		}
		
		failure {
			sleep 60	
			bat 'docker compose -f caldown/docker-compose.yaml down'
			bat 'rmdir \"caldown/dbserver/data\" /S /Q'
			bat 'docker system prune'
			bat 'mkdir \"caldown/dbserver/data\"'
		}
			
	}			
}