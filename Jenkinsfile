pipeline {
	agent any
	
	stages {
		stage('pull') {
			steps {
				dir('caldown/dbserver/data') {
					deletedir()
				}
				echo 'pulled from GitHub'
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