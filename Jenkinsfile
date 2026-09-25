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
                bat '"C:\\Users\\lipsa\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pip install pytest httpx'
                bat '"C:\\Users\\lipsa\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pip install -r user-service/requirements.txt'
                bat '"C:\\Users\\lipsa\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pip install -r restaurent-service/requirements.txt'
                bat '"C:\\Users\\lipsa\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -m pip install -r order-service/requirements.txt'
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
    }

    post {
        success {
            echo 'All tests passed successfully!'
        }
        failure {
            echo 'Tests failed. Check the console output.'
        }
    }
}
