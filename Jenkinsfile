pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out project...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install pytest httpx'
                bat 'pip install -r user-service/requirements.txt'
                bat 'pip install -r restaurent-service/requirements.txt'
                bat 'pip install -r order-service/requirements.txt'
            }
        }

        stage('Test User Service') {
            steps {
                bat 'cd user-service && pytest'
            }
        }

        stage('Test Restaurant Service') {
            steps {
                bat 'cd restaurent-service && pytest'
            }
        }

        stage('Test Order Service') {
            steps {
                bat 'cd order-service && pytest'
            }
        }

        stage('Build Docker Images') {
            steps {
                bat 'docker compose build'
            }
        }

        stage('Start Application') {
            steps {
                bat 'docker compose up -d'
            }
        }
    }
}
