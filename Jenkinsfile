#!/usr/bin/env groovy

pipeline {
  agent any
  
  stages {
    stage('Test') {
      steps {
        echo 'Testing...'
        /* TODO : Test for vulnerability */

        /* TODO : Test for Code Quality */
/*       pylint app/ec2CheatsheetScraper/spiders/actionsscraper.py
  */    
        /* TODO : Units∂ Tests */

        /* TODO : Test for image vulnerability */
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
