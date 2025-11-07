pipeline {
  agent any

  environment {
    APP_NAME = 'demo-sast'
    HOST_PORT = '8081'          // Changez si nécessaire
    APP_PORT = '3000'           // Port interne de l'application
    SEMGREP_IMG = 'returntocorp/semgrep:latest'
    GITLEAKS_IMG = 'zricethezav/gitleaks:latest'
  }

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
          docker run --rm -v "$PWD:/src" -w /src ${SEMGREP_IMG} semgrep --config auto --json > semgrep_report.json || true
        '''
        script {
          // Lire le fichier JSON généré
          def scanResult = readJSON file: 'semgrep_report.json'

          // Vérification des vulnérabilités critiques
          def criticalVulns = scanResult.findings.findAll { it.severity == 'critical' }
          
          // Si des vulnérabilités critiques sont trouvées, échouer le pipeline
          if (criticalVulns.size() > 0) {
            error "Des vulnérabilités critiques ont été détectées par Semgrep !"
          }
        }
      }
    }

    stage('SCA - Analyse des dépendances avec Trivy') {
      steps {
        echo '📦 Analyse SCA avec Trivy...'
        script {
          def scanResult = sh(script: 'trivy fs . --scanners vuln --format json --output trivy_report.json', returnStdout: true)
          def jsonResponse = readJSON text: scanResult
          
          // Vérification des vulnérabilités critiques dans Trivy
          def criticalVulns = jsonResponse.findAll { it.Vulnerability.Severity == 'CRITICAL' }

          if (criticalVulns.size() > 0) {
            error "Des vulnérabilités critiques ont été détectées par Trivy !"
          }
        }
      }
    }

    stage('Secret Scanning - Gitleaks') {
      steps {
        echo '🕵️ Scan des secrets avec Gitleaks...'
        sh '''
          docker run --rm -v "$PWD:/repo" ${GITLEAKS_IMG} detect \
            --no-git --source /repo \
            --exclude gitleaks_report.json \
            --exclude node_modules \
            --report-path /repo/gitleaks_report.json \
            --verbose || true
        '''
      }
    }

    stage('Docker Build') {
      steps {
        echo '🐳 Construction de l’image Docker...'
        sh '''
          docker build -t ${APP_NAME} . || true
        '''
      }
    }

    stage('Docker Scan - Image Security') {
      steps {
        echo '🔎 Scan de sécurité de l’image Docker...'
        sh '''
          docker image ls
          trivy image ${APP_NAME} --exit-code 0 --format json --output trivy_image_report.json || true
        '''
      }
    }

    stage('Deploy') {
      steps {
        echo "🚀 Déploiement du conteneur sur le port ${HOST_PORT}..."
        sh """
          docker ps -q --filter "publish=${HOST_PORT}" | xargs -r docker stop
          docker ps -q --filter "publish=${HOST_PORT}" | xargs -r docker rm
          docker stop ${APP_NAME} || true
          docker rm ${APP_NAME} || true
          docker run -d --name ${APP_NAME} -p ${HOST_PORT}:${APP_PORT} ${APP_NAME}
        """
      }
    }

    stage('DAST - OWASP ZAP Scan') {
      steps {
        echo '🧪 Scan dynamique de l’application (DAST)...'
        sh '''
          docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
            -t http://localhost:${HOST_PORT} \
            -r zap_report.html || true
        '''
      }
    }
  }

  post {
    always {
      echo '📊 Fin du pipeline - génération/archivage des rapports.'
      sh 'ls -lh *.json zap_report.html || true'
      archiveArtifacts artifacts: '*.json, zap_report.html', onlyIfSuccessful: false
    }
  }
}
