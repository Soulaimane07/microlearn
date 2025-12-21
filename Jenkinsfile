pipeline {
    agent any

    stages {

        stage('Cloner le dépôt') {
            steps {
                echo 'Clonage du dépôt GitHub...'
                // Using 'jenkins' branch to test these changes
                git branch: 'main', url: 'https://github.com/Soulaimane07/microlearn.git'
            }
        }

        stage('Build and SonarQube Analysis') {
            parallel {

                stage('Micro1: Data Preparer') {
                    stages {

                        stage('Build Micro1') {
                            steps {
                                dir('services/micro1-data_preparer') {
                                    echo 'Installation des dépendances et tests Micro1...'
                                    script {
                                        bat 'py -3.13 -m venv venv'
                                        bat 'venv\\Scripts\\activate.bat && pip install -r requirements.txt && pip install pytest pytest-cov httpx'
                                        bat 'venv\\Scripts\\activate.bat && set PYTHONPATH=. && pytest --cov=app --cov-report=xml:coverage.xml'
                                    }
                                }
                            }
                        }

                        stage('SonarQube Analysis Micro1') {
                            steps {
                                dir('services/micro1-data_preparer') {
                                    script {
                                        withSonarQubeEnv('SonarQube') {
                                            // Removed 'tool' dependency. Assumes 'sonar-scanner.bat' is in system PATH.
                                            bat "sonar-scanner.bat " +
                                                "-Dsonar.projectKey=MicroLearn-Data-Preparer " +
                                                "-Dsonar.projectName='MicroLearn-Data-Preparer' " +
                                                "-Dsonar.sources=app " +
                                                "-Dsonar.tests=tests " +
                                                "-Dsonar.token=sqa_714a6e276a26633c6d996584753ce7299e8df17e " +
                                                "-Dsonar.python.coverage.reportPaths=coverage.xml"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                stage('Micro2: Model Selector') {
                    stages {

                        stage('Build Micro2') {
                            steps {
                                dir('services/micro2-model_selector') {
                                    echo 'Installation des dépendances et tests Micro2...'
                                    script {
                                        bat 'py -3.13 -m venv venv'
                                        bat 'venv\\Scripts\\activate.bat && pip install -r requirements.txt && pip install pytest pytest-cov httpx'
                                        bat 'venv\\Scripts\\activate.bat && set PYTHONPATH=. && pytest --cov=app --cov-report=xml:coverage.xml'
                                    }
                                }
                            }
                        }

                        stage('SonarQube Analysis Micro2') {
                            steps {
                                dir('services/micro2-model_selector') {
                                    script {
                                        withSonarQubeEnv('SonarQube') {
                                            bat "sonar-scanner.bat " +
                                                "-Dsonar.projectKey=MicroLearn-Model-Selector " +
                                                "-Dsonar.projectName='MicroLearn-Model-Selector' " +
                                                "-Dsonar.sources=app " +
                                                "-Dsonar.tests=tests " +
                                                "-Dsonar.token=sqa_714a6e276a26633c6d996584753ce7299e8df17e " +
                                                "-Dsonar.python.coverage.reportPaths=coverage.xml"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                stage('Micro3: Trainer') {
                    stages {

                        stage('Build Micro3') {
                            steps {
                                dir('services/micro3-trainer') {
                                    echo 'Installation des dépendances et tests Micro3...'
                                    script {
                                        bat 'py -3.13 -m venv venv'
                                        bat 'venv\\Scripts\\activate.bat && pip install -r requirements.txt && pip install pytest pytest-cov httpx'
                                        bat 'venv\\Scripts\\activate.bat && set PYTHONPATH=. && pytest --cov=app --cov-report=xml:coverage.xml'
                                    }
                                }
                            }
                        }

                        stage('SonarQube Analysis Micro3') {
                            steps {
                                dir('services/micro3-trainer') {
                                    script {
                                        withSonarQubeEnv('SonarQube') {
                                            bat "sonar-scanner.bat " +
                                                "-Dsonar.projectKey=MicroLearn-Trainer " +
                                                "-Dsonar.projectName='MicroLearn-Trainer' " +
                                                "-Dsonar.sources=app " +
                                                "-Dsonar.tests=tests " +
                                                "-Dsonar.token=sqa_714a6e276a26633c6d996584753ce7299e8df17e " +
                                                "-Dsonar.python.coverage.reportPaths=coverage.xml"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        stage('Docker Compose') {
            steps {
                echo 'Création et déploiement des conteneurs Docker...'
                script {
                    bat 'docker-compose up -d --build'
                }
            }
        }
    }
}
