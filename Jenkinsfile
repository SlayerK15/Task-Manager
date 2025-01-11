pipeline {
    agent any
    
    environment {
        APP_NAME = "task-manager"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build and Deploy') {
            steps {
                script {
                    // Create network if it doesn't exist
                    sh 'docker network create app-network || true'
                    
                    // Stop and remove existing containers
                    sh 'docker-compose down || true'
                    
                    // Deploy using docker-compose
                    sh 'docker-compose up -d --build'
                    
                    // Wait for services to be up
                    sh 'sleep 10'
                    
                    // Verify services are running
                    sh 'docker-compose ps'
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    sh 'curl -f http://localhost:5000 || exit 1'
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker image prune -f'
        }
        success {
            echo 'Successfully built and deployed the Task Manager application!'
        }
        failure {
            script {
                echo 'Build or deployment failed! Check the logs for details.'
                sh 'docker-compose logs'
            }
        }
    }
}
