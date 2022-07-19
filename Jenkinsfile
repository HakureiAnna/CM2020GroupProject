pipeline {
	agent any
	
	stages {
		stage('pull') {
			steps {
				echo 'pulled from GitHub'
				bat 'rmdir caldown/dbserverdata/ /S /Q'
				batr 'md caldonw/dbserver/data/'
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