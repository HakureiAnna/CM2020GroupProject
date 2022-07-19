pipeline {
	agent any
	
	stages {
		stage('pull') {
			steps {
				echo 'pulled from GitHub'
				bat 'rmdir "caldown/dbserver/data/" /S /Q'
				batr 'md "caldown/dbserver/data/"'
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