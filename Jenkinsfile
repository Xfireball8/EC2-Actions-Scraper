#!/usr/bin/env groovy

pipeline {
  agent any
  
  stages {
    stage('Test') {
      steps {
        echo 'Testing...'
        /* Pyflakes, linter, Sloc */
        sh 'make' 
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
