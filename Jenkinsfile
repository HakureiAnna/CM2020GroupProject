pipeline {
	agent any
	
	stages {
		stage('test') {
			steps {
				bat "echo $PATH"
				bat 'docker-compose up -f "caldown/docker-compose.yaml" --build'
				bat 'pytest "caldown/backend/tests"'
			}
		} 
	}
}