pipeline {
	agent any
	
	environment {
		EDAMAM_APP_ID = credentials('EDAMAM_APP_ID')
		EDAMAM_APP_KEY = credentials('EDAMAM_APP_KEY')
	}
	
	stages {
		stage('pull') {
			steps {
				echo 'pulled from GitHub'
			}
		}
		stage('build') {
			steps {			
				bat '(echo app_id=%EDAMAM_APP_ID% & echo app_key=%EDAMAM_APP_KEY%) > caldown/backend/app/secret'
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
			sleep 1
			bat 'docker compose -f caldown/docker-compose.yaml down'
			bat 'rmdir \"caldown/dbserver/data\" /S /Q'
			bat 'docker system prune'
			bat 'mkdir \"caldown/dbserver/data\"'
		}
		
		failure {
			sleep 120
			bat 'docker compose -f caldown/docker-compose.yaml down'
			bat 'rmdir \"caldown/dbserver/data\" /S /Q'
			bat 'docker system prune'
			bat 'mkdir \"caldown/dbserver/data\"'
		}			
	}			
}