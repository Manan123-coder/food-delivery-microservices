pipeline {
    agent any

    stages {
        stage('Check Python') {
            steps {
                bat 'where python'
                bat 'python --version'
                bat 'python -m pip --version'
            }
        }
    }
}
