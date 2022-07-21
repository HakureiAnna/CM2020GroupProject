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
				sleep 25
			}
		}
		stage('test') {
			steps {
				bat 'pytest "caldown/backend/tests"'
			}
		} 
	}
	post {	
		always {
			bat 'docker compose -f caldown/docker-compose.yaml down'
			sleep 20
			bat 'docker system prune'
			bat 'rmdir \"caldown/dbserver/data\" /S /Q'
		}
	}			
}