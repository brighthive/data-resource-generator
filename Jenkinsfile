pipeline {
  agent any
  options {
      // Will set the build timeout at 5 minutes and disable concurrent builds.
      timeout(time: 5, unit: 'MINUTES')
      disableConcurrentBuilds()
  }
  triggers {
      // All builds will happen upon github push
      githubPush()
  }
  stages {
      /*
        Initialize all the pipline parameters and thresholds.
      */
      stage("Initialize") {
        steps {
          initialize()
        }
      }
      /*
        The pre checks will spit out all the pipeline envs and parameters (This stage is added for debugging within Jenkins).
      */
      stage("Pre-Checks") {
        steps {
          sh 'docker images'
        }
      }
      /*
        Will take the files from repo and will run them with a docker container at the root level. (If passes, will cache deps and destory container)
        If no database is required use the following for testing.
        ----------
      */
      stage('Testing') {
        steps {
          script {
            docker.image(env.DOCKER_DB_IMAGE_NAME).withRun("-h ${env.POSTGRES_HOST} -e POSTGRES_USER=${env.POSTGRES_USER} -e POSTGRES_PASSWORD=${env.POSTGRES_PASSWORD}") { db ->
                docker.image(env.DOCKER_DB_IMAGE_NAME).inside("--link ${db.id}:db") {
                    sh '''
                      psql --version
                      export PGPASSWORD=${POSTGRES_PASSWORD}
                      export RETRIES=${RETRIES_DBPING_IN_SECONDS}
                      until psql -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
                        echo "Waiting for postgres server, $((RETRIES-=1)) remaining attempts..."
                        sleep 1
                      done
                      psql -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -c "CREATE DATABASE ${POSTGRES_DATABASE}"
                    '''
                }
                docker.image(env.DOCKER_PYTHON_NAME).inside("-u root:root --link ${db.id}:db") {
                    sh "python --version"
                    sh "apt-get update"
                    sh "apt-get install -y --no-install-recommends gcc git"
                    sh "apt-get install python-dev --assume-yes"
                    sh "pip install --no-cache-dir pipenv"
                    sh "pipenv install --dev"
                    sh "printenv"
                    sh "[ -d static ] || mkdir static"
                    sh "pipenv run pytest"
                }
              }
            }
        }
      }
      /*
        If the testing stage passes, it will be proceed to building the image for the AWS ECR.
      */
      stage('Building Image') {
        when {
          expression {
            env.GIT_BRANCH == env.BRANCH_IMAGE_BUILD_PUSH
          }
        }
        steps {
          sh 'docker build -t $REGISTRY_NAME .'
        }
      }
      /*
        Will publish the image just build on Jenkins to AWS ECR as latest and the current build number
      */
      stage('Publish Image') {
        when {
          expression {
            env.GIT_BRANCH == env.BRANCH_IMAGE_BUILD_PUSH
          }
        }
        steps {
          sh 'aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $REGISTRY_URI/$REGISTRY_NAME'
          sh 'docker tag $REGISTRY_NAME:latest $REGISTRY_URI/$REGISTRY_NAME:latest'
          sh 'docker push $REGISTRY_URI/$REGISTRY_NAME:latest'
          sh 'docker tag $REGISTRY_NAME:latest $REGISTRY_URI/$REGISTRY_NAME:$TAGNAME'
          sh 'docker push $REGISTRY_URI/$REGISTRY_NAME:$TAGNAME'
        }
      }
      /*
        Will clean up the Jenkins server of any cached builds or source. (Only the python and db images are saved so they don't have to be pulled every time)
      */
      stage('Clean Up') {
        when {
          expression {
            env.GIT_BRANCH == env.BRANCH_IMAGE_BUILD_PUSH
          }
        }
        steps {
          sh 'docker rmi $REGISTRY_URI/$REGISTRY_NAME'
          sh 'docker rmi $REGISTRY_NAME:latest'
          sh 'docker rmi $REGISTRY_URI/$REGISTRY_NAME:$TAGNAME'
        }
      }
  }
  post {
      always {
          cleanWs()
      }
  }
}


def initialize() {
    // Docker Defs
    env.DOCKER_DB_IMAGE_NAME = 'postgres:11.1'
    env.DOCKER_PYTHON_NAME = 'python:3.7.4-slim'

    // AWS ERC Parameters / Push Rules
    env.REGISTRY_NAME = 'brighthive/data-resource-generator'
    env.REGISTRY_URI = '396527728813.dkr.ecr.us-east-2.amazonaws.com'
    env.BRANCH_IMAGE_BUILD_PUSH = 'master'
    env.SYSTEM_NAME = 'Jenkins'
    env.AWS_REGION = 'us-east-2'
    env.MAX_ENVIRONMENTNAME_LENGTH = 32
    env.BUILD_VERSION = '0.8.0'
    env.TAGNAME = env.BUILD_VERSION + '-' + env.GIT_COMMIT.substring(0,5)

    // DB Configs
    env.APP_ENV = 'JENKINS'
    env.POSTGRES_HOST = 'localhost'
    env.POSTGRES_PORT = 5432
    env.RETRIES_DBPING_IN_SECONDS = 60
    env.POSTGRES_USER = 'test_user'
    env.POSTGRES_PASSWORD = 'test_password'
    env.POSTGRES_DATABASE = 'data_resource_dev'
}