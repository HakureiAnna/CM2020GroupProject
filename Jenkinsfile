pipeline {
	agent any
	
	stages {
		stage('test') {
			steps {
				bat "echo $PATH"
				bat 'docker-compose up -f "caldown/docker-compose.yaml" --build -d'
				sleep 30
				bat 'pytest "caldown/backend/tests"'
			}
		} 
	}
}