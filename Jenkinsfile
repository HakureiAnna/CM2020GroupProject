pipeline {
	agent any
	
	stages {
		stage('test') {
			steps {
				docker-compose up -f .\caldown\docker-compose.yaml --build
				pytest caldown\backend\tests
			}
		} 
	}
}