pipeline {
  agent any

  environment {
    SLACK_CHANNEL = "#ci"
    STACK_JOB = "dms/dms_stack/master"
  }

  stages {
    stage("Deploy Production") {
      when {branch 'master'}

      steps {
        build job: "${STACK_JOB}", parameters: [string(name: "RANCHER_ENVIRONMENT", value: "production")]
      }
    }

    stage("Deploy Staging") {
      when {branch 'develop'}

      steps {
        build job: "${STACK_JOB}", parameters: [string(name: "RANCHER_ENVIRONMENT", value: "staging")]
      }
    }
  }

  post {
    success {
      slackSend channel: env.SLACK_CHANNEL, color: "good", message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} builded successfully. (<${env.JOB_URL}|Open>)"
    }

    failure {
      slackSend channel: env.SLACK_CHANNEL, color: "danger", message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} has failed. (<${env.JOB_URL}|Open>)"
    }
  }
}
