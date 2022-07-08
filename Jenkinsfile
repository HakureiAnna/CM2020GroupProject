pipeline {
	agent any
	stages {
		stage('test') {
			steps {
				docker-compose -f caldown/docker-compose.yaml up --build
				pytest caldown/backend/tests
			}
		}
	}
}