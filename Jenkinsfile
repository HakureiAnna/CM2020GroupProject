pipeline {
	agent any
	
	stages {
		stage('test') {
			steps {
				sh 'docker-compose up -f .\caldown\docker-compose.yaml --build'
				sh 'pytest caldown\backend\tests'
			}
		} 
	}
}