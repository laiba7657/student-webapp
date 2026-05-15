pipeline {
    agent any

    environment {
        APP_IMAGE    = "student-webapp:${BUILD_NUMBER}"
        SEL_IMAGE    = "selenium-tests:${BUILD_NUMBER}"
        NETWORK_NAME = "ci-network-${BUILD_NUMBER}"
    }

    stages {

        // ─────────────────────────────────────────────
        stage('Code Build') {
        // ─────────────────────────────────────────────
            steps {
                echo '📦 Stage 1: Building application...'
                sh '''
                    # Install Python deps for unit testing later
                    pip3 install flask==2.3.0 pytest==7.4.0 --quiet --break-system-packages

                    # Build the Docker image for the web app
                    docker build -t ${APP_IMAGE} -f Dockerfile .
                    echo "✅ App Docker image built: ${APP_IMAGE}"
                '''
            }
        }

        // ─────────────────────────────────────────────
        stage('Unit Testing') {
        // ─────────────────────────────────────────────
            steps {
                echo '🧪 Stage 2: Running unit tests...'
                sh '''
                    pip3 install flask==2.3.0 pytest==7.4.0 --quiet
                    python3 -m pytest test_app.py -v --tb=short
                    echo "✅ Unit tests passed!"
                '''
            }
        }

        // ─────────────────────────────────────────────
        stage('Containerized Deployment') {
        // ─────────────────────────────────────────────
            steps {
                echo '🚀 Stage 3: Deploying app in Docker container...'
                sh '''
                    # Create isolated network for this build
                    docker network create ${NETWORK_NAME}

                    # Stop any previous container
                    docker rm -f webapp 2>/dev/null || true

                    # Run the web app container
                    docker run -d \
                        --name webapp \
                        --network ${NETWORK_NAME} \
                        -p 5000:5000 \
                        ${APP_IMAGE}

                    # Wait for app to start
                    sleep 5

                    # Health check
                    curl -f http://localhost:5000 || exit 1
                    echo "✅ App deployed and responding!"
                '''
            }
        }

        // ─────────────────────────────────────────────
        stage('Containerized Selenium Testing') {
        // ─────────────────────────────────────────────
            steps {
                echo '🌐 Stage 4: Running Selenium tests in Docker...'
                sh '''
                    # Build Selenium test image
                    docker build -t ${SEL_IMAGE} -f Dockerfile.selenium .

                    # Run Selenium container on same network as webapp
                    docker run --rm \
                        --network ${NETWORK_NAME} \
                        ${SEL_IMAGE}

                    echo "✅ Selenium tests passed!"
                '''
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up containers and network...'
            sh '''
                docker rm -f webapp 2>/dev/null || true
                docker network rm ${NETWORK_NAME} 2>/dev/null || true
                docker rmi ${APP_IMAGE} 2>/dev/null || true
                docker rmi ${SEL_IMAGE} 2>/dev/null || true
            '''
        }
        success {
            echo '🎉 Pipeline completed SUCCESSFULLY!'
        }
        failure {
            echo '❌ Pipeline FAILED. Check logs above.'
        }
    }
}
