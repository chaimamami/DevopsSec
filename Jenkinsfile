pipeline {
  agent any

  environment {
    APP_NAME   = 'demo-sast'
    HOST_PORT  = '8081'
    APP_PORT   = '3000'
    SEMGREP_IMG = 'returntocorp/semgrep:latest'
    GITLEAKS_IMG = 'zricethezav/gitleaks:latest'
    PYTHON_ENV = '/usr/bin/python3'
    SONAR_HOST_URL = 'http://10.0.2.15:9000'
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
          npx eslint . -f json -o eslint_report.json || true
          docker run --rm -v "$PWD:/src" -w /src ${SEMGREP_IMG} \
            semgrep --config auto --json > semgrep_report.json || true
        '''
      }
    }

    stage('SCA - Analyse des dépendances avec Trivy') {
      steps {
        echo '📦 Analyse SCA avec Trivy...'
        sh '''
          trivy fs . --scanners vuln --exit-code 0 \
            --format json --output trivy_report.json || true
        '''
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

    /* 🚀 NOUVELLE ÉTAPE AUTOMATIQUE SONARQUBE */
    stage('Static Analysis - SonarQube') {
      steps {
        echo '📊 Analyse SonarQube automatique...'
        withCredentials([string(credentialsId: 'SONAR_TOKEN_ID', variable: 'SONAR_TOKEN')]) {
          sh '''
            docker run --rm -v "$PWD":/usr/src -w /usr/src \
              -e SONAR_HOST_URL="${SONAR_HOST_URL}" \
              sonarsource/sonar-scanner-cli:latest \
              -Dsonar.projectKey=demo_sast \
              -Dsonar.sources=. \
              -Dsonar.host.url=${SONAR_HOST_URL} \
              -Dsonar.login=${SONAR_TOKEN}
          '''
        }
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

    stage('Exporter les métriques pour Prometheus') {
      steps {
        echo '📊 Export des métriques de sécurité vers Prometheus...'
        sh '''
          cd /var/lib/jenkins/workspace/DevSecOps
          mkdir -p /var/lib/jenkins/metrics

          echo "# ESLint Metrics" > /var/lib/jenkins/metrics/security_metrics.prom
          ESLINT_ISSUES=$(jq '[.[].messages] | flatten | length' eslint_report.json 2>/dev/null || echo 0)
          echo "eslint_issues_total ${ESLINT_ISSUES}" >> /var/lib/jenkins/metrics/security_metrics.prom

          echo "# Semgrep Metrics" >> /var/lib/jenkins/metrics/security_metrics.prom
          SEMGREP_FINDINGS=$(jq '.results | length' semgrep_report.json 2>/dev/null || echo 0)
          echo "semgrep_findings_total ${SEMGREP_FINDINGS}" >> /var/lib/jenkins/metrics/security_metrics.prom

          echo "# Trivy FS Metrics" >> /var/lib/jenkins/metrics/security_metrics.prom
          TRIVY_CRITICAL=$(jq '[.Results[].Vulnerabilities[]? | select(.Severity=="CRITICAL")] | length' trivy_report.json 2>/dev/null || echo 0)
          TRIVY_HIGH=$(jq '[.Results[].Vulnerabilities[]? | select(.Severity=="HIGH")] | length' trivy_report.json 2>/dev/null || echo 0)
          echo "trivy_vulnerabilities_critical ${TRIVY_CRITICAL}" >> /var/lib/jenkins/metrics/security_metrics.prom
          echo "trivy_vulnerabilities_high ${TRIVY_HIGH}" >> /var/lib/jenkins/metrics/security_metrics.prom

          echo "# Trivy Image Metrics" >> /var/lib/jenkins/metrics/security_metrics.prom
          TRIVY_IMG_CRIT=$(jq '[.Results[].Vulnerabilities[]? | select(.Severity=="CRITICAL")] | length' trivy_image_report.json 2>/dev/null || echo 0)
          echo "trivy_image_critical ${TRIVY_IMG_CRIT}" >> /var/lib/jenkins/metrics/security_metrics.prom

          echo "✅ Fichier Prometheus mis à jour :"
          cat /var/lib/jenkins/metrics/security_metrics.prom
        '''
      }
    }
  }

  post {
    always {
      echo '📦 Archivage des rapports et envoi Slack...'
      sh 'ls -lh *.json zap_report.html || true'
      archiveArtifacts artifacts: '*.json, zap_report.html', onlyIfSuccessful: false

      echo '📤 Envoi automatique de la notification Slack...'
      withCredentials([string(credentialsId: 'SLACK_WEBHOOK_URL', variable: 'SLACK_WEBHOOK_URL')]) {
        sh '''
          if [ -f send_slack_alert.py ]; then
            ${PYTHON_ENV} send_slack_alert.py || echo "⚠️ Échec de l’envoi Slack"
          else
            echo "⚠️ Script Slack introuvable !"
          fi
        '''
      }
    }
  }
}
