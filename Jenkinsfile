pipeline {
  agent any

  environment {
    APP_NAME = 'demo-sast'
    HOST_PORT = '8081'          // Changez si nécessaire
    APP_PORT  = '3000'          // Port interne de l'application
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
          # ESLint (local au projet)
          npm install
          npx eslint . || true

          # Semgrep via container (pas besoin d’être installé sur Jenkins)
          docker run --rm -v "$PWD:/src" -w /src ${SEMGREP_IMG} \
            semgrep --config auto --json > semgrep_report.json || true
        '''
      }
    }

    stage('SCA - Analyse des dépendances avec Trivy') {
      steps {
        echo '📦 Analyse SCA avec Trivy...'
        sh '''
          # Scanne les dépendances (npm) du repo
          trivy fs . --scanners vuln --exit-code 0 \
            --format json --output trivy_report.json
        '''
      }
    }

    stage('Secret Scanning - Gitleaks') {
      steps {
        echo '🕵️ Scan des secrets avec Gitleaks...'
        sh '''
          # Gitleaks via container, ignore son propre rapport et node_modules
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
          docker build -t ${APP_NAME} .
        '''
      }
    }

    stage('Docker Scan - Image Security') {
      steps {
        echo '🔎 Scan de sécurité de l’image Docker...'
        sh '''
          # Liste des images Docker
          docker image ls

          # Scanne l'image locale "demo-sast" pour les vulnérabilités
          trivy image ${APP_NAME} --exit-code 0 --format json --output trivy_image_report.json
        '''
      }
    }

    stage('Deploy') {
      steps {
        echo "🚀 Déploiement du conteneur sur le port ${HOST_PORT}..."
        sh """
          # Arrête/retire tout conteneur qui publie déjà ${HOST_PORT}
          docker ps -q --filter "publish=${HOST_PORT}" | xargs -r docker stop
          docker ps -q --filter "publish=${HOST_PORT}" | xargs -r docker rm

          # Nettoie l'ancien conteneur s'il existe
          docker stop ${APP_NAME} || true
          docker rm ${APP_NAME} || true

          # Lance la nouvelle version sur HOST:${HOST_PORT} -> CONTAINER:${APP_PORT}
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
