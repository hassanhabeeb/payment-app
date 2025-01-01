pipeline {
    agent any

    environment {
        // Multiple Docker images stored in a single variable with a delimiter (comma-separated)
        DOCKER_IMAGES = "mongo:latest,docker.elastic.co/elasticsearch/elasticsearch:7.9.3,docker.elastic.co/kibana/kibana:7.9.3,docker.elastic.co/logstash/logstash:7.9.3,redis:latest" 
        DOCKER_COMPOSE_PATH = "./docker-compose.yml" // Path to docker-compose.yml
        NEXUS_CREDENTIALS = credentials('nexus-cred') // Jenkins credential ID for Nexus
        SONARQUBE_TOKEN = credentials('react-app') // Jenkins credential ID for SonarQube token
        NEXUS_REPO_URL = '54.244.211.2:8083' // Correct Docker registry URL
        NEXUS_REPO_NAME = 'react-app1' // Repository name
        SONARQUBE_SERVER = 'sonar' // SonarQube server ID in Jenkins
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'git@github.com:hassanhabeeb/payment-app.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv(SONARQUBE_SERVER) {
                        def scannerHome = tool 'sonar'
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=react-app \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=http://35.162.77.248:9000 \
                            -Dsonar.login=${SONARQUBE_TOKEN}
                        """
                    }
                }
            }
        }

        stage('Pull Docker Images') {
            steps {
                script {
                    def images = DOCKER_IMAGES.split(',')
                    images.each { image ->
                        echo "Pulling image: ${image}"
                        sh "docker pull ${image}"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker-compose -f ${DOCKER_COMPOSE_PATH} build"
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                script {
                    def timestamp = new Date().format('yyyyMMddHHmmss')
                    env.DOCKER_IMAGE_VERSIONED = "${NEXUS_REPO_URL}/${NEXUS_REPO_NAME}/react-app:${timestamp}"
                    sh "docker tag react-app:latest ${DOCKER_IMAGE_VERSIONED}"
                }
            }
        }

        stage('Push Docker Image to Nexus') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'nexus-cred', usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
                        sh '''
                            echo $NEXUS_PASS | docker login ${NEXUS_REPO_URL} --username $NEXUS_USER --password-stdin
                            docker push ${DOCKER_IMAGE_VERSIONED}
                        '''
                    }
                }
            }
        }

        stage('Run Application') {
            steps {
                script {
                    sh "docker-compose -f ${DOCKER_COMPOSE_PATH} up -d"
                }
            }
        }
    }
}
