#!/usr/bin/env groovy

pipeline {
  agent any
  
  stages {
    stage('Test') {
      steps {
        echo 'Testing...'
        /* Pyflakes, linter, Sloc */
        sh 'python3 -m pylint --output-format=parseable --fail-under=<threshold value> module --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" | tee pylint.log || echo "pylint exited with $?"'
        echo "linting Success, Generating Report"
        recordIssues enabledForFailure: true, aggregatingResults: true, tool: pyLint(pattern: 'pylint.log')
     }
    }
  
    stage('Integrate') {
      when {
        expression {
          currentBuild.result == null || currentBuild.result == 'SUCCESS'
        }
      }

      steps {
        echo 'Integrating...'
        /* TODO : Create Documentation */
        /* TODO : Merge into git development branch */
      }
    }
  }
}
