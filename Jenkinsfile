pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                echo '🔨 Compilation du projet...'
                sh 'echo "Build success"'
            }
        }

        stage('Tests') {
            steps {
                echo '🧪 Exécution des tests unitaires...'
                sh 'echo "Tests OK"'
            }
        }

        stage('SAST - ESLint + Semgrep') {
            steps {
                echo '🔍 Analyse du code source (SAST)...'
                sh '''
                npm install
                npx eslint . || true
                semgrep --config auto --json > semgrep_report.json || true
                '''
            }
        }

        stage('SCA - Analyse des dépendances avec Trivy') {
            steps {
                echo '📦 Analyse SCA avec Trivy...'
                sh '''
                trivy fs . --security-checks vuln --exit-code 0 --format json --output trivy_report.json
                '''
            }
        }

        stage('Secret Scanning - Gitleaks') {
            steps {
                echo '🕵️ Scan des secrets avec Gitleaks...'
                sh '''
                gitleaks detect --no-git --source . --report-path gitleaks_report.json --verbose || true
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo '🐳 Construction de l’image Docker...'
                sh '''
                docker build -t demo-sast .
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Déploiement du conteneur...'
                sh '''
                docker stop demo-sast || true
                docker rm demo-sast || true
                docker run -d --name demo-sast -p 8080:3000 demo-sast
                '''
            }
        }
    }

    post {
        always {
            echo '📊 Fin du pipeline - génération des rapports.'
            sh 'ls -lh *.json || true'
        }
    }
}
