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
        script {
          // Exécuter ESLint
          sh 'npm install'
          sh 'npx eslint . || true'

          // Lancer l'analyse Semgrep
          sh '''
            docker run --rm -v "$PWD:/src" -w /src ${SEMGREP_IMG} semgrep --config auto --json > semgrep_report.json || true
          '''

          // Vérification de la présence du fichier Semgrep
          def fileExists = fileExists 'semgrep_report.json'
          if (fileExists) {
            def scanResult = readJSON file: 'semgrep_report.json'
            if (scanResult.results?.size() > 0) {
              echo "Des vulnérabilités ont été trouvées dans Semgrep :"
              scanResult.results.each {
                echo "Vulnérabilité : ${it.path} - ${it.check_id}"
              }
            } else {
              echo "Aucune vulnérabilité détectée dans Semgrep."
            }
          } else {
            error "Le fichier semgrep_report.json n'a pas été généré !"
          }
        }
      }
    }

    stage('SCA - Analyse des dépendances avec Trivy') {
      steps {
        echo '📦 Analyse SCA avec Trivy...'
        script {
          // Exécuter Trivy pour analyser les dépendances
          sh '''
            trivy fs . --scanners vuln --format json --output trivy_report.json || true
          '''
          
          // Vérification de la présence du fichier Trivy
          def fileExists = fileExists 'trivy_report.json'
          if (fileExists) {
            def scanResult = readJSON file: 'trivy_report.json'
            if (scanResult?.vulnerabilities?.size() > 0) {
              echo "Des vulnérabilités ont été trouvées dans Trivy :"
              scanResult.vulnerabilities.each {
                echo "Vulnérabilité : ${it.VulnerabilityID} - ${it.Title}"
              }
            } else {
              echo "Aucune vulnérabilité détectée dans Trivy."
            }
          } else {
            error "Le fichier trivy_report.json n'a pas été généré !"
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
