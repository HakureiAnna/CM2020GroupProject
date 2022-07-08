pipeline {
	agent any
	
	stages {
		stage('test') {
			steps {
				bat "echo $PATH"
				bat 'docker compose -f caldown/docker-compose.yaml up'
				sleep 30
				bat 'pytest "caldown/backend/tests"'
			}
		} 
	}
}