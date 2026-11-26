==================== 1. MAVEN JAVA ====================
cd D:\Desktop
mvn archetype:generate "-DgroupId=com.example" "-DartifactId=maven-java-app" "-DarchetypeArtifactId=maven-archetype-quickstart" "-DarchetypeVersion=1.4" "-DinteractiveMode=false"
cd maven-java-app
notepad pom.xml
# in Notepad set maven.compiler.source and maven.compiler.target to 17, save
mvn clean
mvn install
mvn test
mvn package
java -cp target/maven-java-app-1.0-SNAPSHOT.jar com.example.App

# push (empty public repo first; if remote exists use: git remote set-url origin URL)
git init
git branch -M main
Set-Content -Path .gitignore -Value "target/" -Encoding ascii
git add .
git commit -m "Initial Maven Java project"
git remote add origin https://github.com/zaynul2311/testrepo.git
git push -u origin main
# if push gives 403: delete saved GitHub login in Credential Manager, or upload pom.xml + src via GitHub website (Add file > Upload files)


==================== 2. MAVEN WEB ====================
cd D:\Desktop
mvn archetype:generate "-DgroupId=com.example" "-DartifactId=maven-web-app" "-DarchetypeArtifactId=maven-archetype-webapp" "-DarchetypeVersion=1.4" "-DinteractiveMode=false"
cd maven-web-app
mvn clean
mvn install
mvn test
mvn package
dir target\*.war
# upload pom.xml + src to an empty public GitHub repo (e.g. maven-web-app)
# if Java version error: add the same two compiler properties (17) as section 1


==================== 3. JENKINS JAVA (freestyle) ====================
# JOB 1: MavenJava_Test
New Item > MavenJava_Test > Freestyle > OK
Build Environment > tick "Delete workspace before build starts"
Add build step > Copy artifacts from another project
  Project name: MavenJava_Build | Stable build only: tick | Artifacts to copy: **/*
Add build step > Invoke top-level Maven targets > Maven Version: YOUR_MAVEN_NAME > Goals: test
Post-build > Archive the artifacts > **/*
Save

# JOB 2: MavenJava_Build
New Item > MavenJava_Build > Freestyle > OK
Source Code Management > Git > https://github.com/zaynul2311/testrepo.git > Branch */main
Add build step > Invoke top-level Maven targets > Goals: clean
Add build step > Invoke top-level Maven targets > Goals: install
Post-build > Archive the artifacts > **/*
Post-build > Build other projects > MavenJava_Test > only if build is stable
Save

# VIEW
Dashboard > "+" > MavenJava_Pipeline > Build Pipeline View > Create
Layout: upstream/downstream > Initial job: MavenJava_Build > OK
Click Run > click black box on each stage > Console Output


==================== 4. JENKINS WEB (freestyle) ====================
# prereqs: Tomcat on port 8085, user admin / 1234 with roles manager-script,manager-gui; "Deploy to container" plugin
# create in this order: Deploy, Test, Build

# JOB 1: MavenWeb_Deploy
Freestyle > tick "Delete workspace before build starts"
Copy artifacts from another project > MavenWeb_Test > stable only > **/*
Post-build > Deploy WAR/EAR to a container
  WAR/EAR files: **/*.war
  Context path: Webpath
  Container: Tomcat 9.x Remote
  Credentials: Add > username admin, password 1234
  Tomcat URL: http://localhost:8085/
Save

# JOB 2: MavenWeb_Test
Freestyle > tick "Delete workspace before build starts"
Copy artifacts from another project > MavenWeb_Build > stable only > **/*
Maven goal: test
Post-build > Archive the artifacts > **/*
Post-build > Build other projects > MavenWeb_Deploy
Save

# JOB 3: MavenWeb_Build
Freestyle > Git > WEB_REPO_URL > Branch */main
Maven goals: clean, then install
Post-build > Archive the artifacts > **/*
Post-build > Build other projects > MavenWeb_Test
Save

# VIEW
"+" > MavenWeb_Pipeline > Build Pipeline View > Initial job: MavenWeb_Build > Run

# VERIFY (browser)
http://localhost:8085/   > Manager App > /Webpath
http://localhost:8085/Webpath/


==================== 5. JENKINS SCRIPT (Pipeline job) ====================
# New Item > Pipeline > Pipeline script > paste below > Save > Build Now
pipeline {
    agent any
    tools {
        maven 'YOUR_MAVEN_NAME'
    }
    stages {
        stage('git repo & clean') {
            steps {
                bat "if exist testrepo rmdir /s /q testrepo"
                bat "git clone https://github.com/zaynul2311/testrepo.git"
                bat "mvn clean -f testrepo"
            }
        }
        stage('install') {
            steps { bat "mvn install -f testrepo" }
        }
        stage('test') {
            steps { bat "mvn test -f testrepo" }
        }
        stage('package') {
            steps { bat "mvn package -f testrepo" }
        }
    }
}
# 6 PM daily trigger: Build Triggers > Build periodically > 0 18 * * *


==================== 6. KUBERNETES: SCALE NGINX ====================
minikube start --driver=docker
minikube status
kubectl create deployment mynginx --image=nginx
kubectl get deployments
kubectl get pods
kubectl describe pods
kubectl expose deployment mynginx --type=NodePort --port=80 --target-port=80
kubectl get service mynginx
kubectl scale deployment mynginx --replicas=4
kubectl get pods
kubectl port-forward svc/mynginx 8081:80
# open http://localhost:8081   (if it fails: minikube service mynginx --url)
# cleanup
kubectl delete deployment mynginx
kubectl delete service mynginx
minikube stop


==================== 7a. DOCKER SINGLE CONTAINER ====================
mkdir D:\Desktop\dockerlab
cd D:\Desktop\dockerlab
@"
FROM redis:latest
CMD ["redis-server"]
"@ | Set-Content -Path Dockerfile -Encoding ascii
docker build -t redisnew .
docker run --name myredisnew -d redisnew
docker ps
docker exec -it myredisnew redis-cli
# inside redis-cli:  SET name "Alice"  |  GET name  |  exit
docker stop myredisnew
docker login
docker commit myredisnew HUBUSER/redis1
docker images
docker push HUBUSER/redis1
docker rm myredisnew
docker rmi HUBUSER/redis1
docker ps -a
docker logout
docker pull HUBUSER/redis1
docker run --name myredis -d HUBUSER/redis1
docker ps
docker stop myredis
docker rm myredis
docker rmi HUBUSER/redis1


==================== 7b. DOCKER MULTI CONTAINER (COMPOSE) ====================
mkdir D:\Desktop\compose-lab
cd D:\Desktop\compose-lab
@"
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    networks:
      - app-net
    depends_on:
      - db
      - redis
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: demo
      POSTGRES_PASSWORD: demo
      POSTGRES_DB: demo_db
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-net
  redis:
    image: redis:alpine
    networks:
      - app-net
networks:
  app-net:
volumes:
  db-data:
"@ | Set-Content -Path docker-compose.yml -Encoding ascii
docker compose up -d
docker compose ps
# open http://localhost:8080
docker compose exec db psql -U demo -d demo_db -c "CREATE TABLE students(id int, name text);"
docker compose exec db psql -U demo -d demo_db -c "INSERT INTO students VALUES (1,'Alice');"
docker compose down
docker compose up -d
docker compose exec db psql -U demo -d demo_db -c "SELECT * FROM students;"
docker network ls
docker volume ls
docker compose down


==================== 8. AWS: EC2 + DOCKER + MAVEN WEB APP ====================
# CONSOLE
Sign in the way your class did > open lab > AWS console
Search EC2 > Launch instance
Name: Myserver | AMI: Ubuntu Server | Type: t2.micro or t3.micro
Key pair > Create new > SElab > download .pem
Network settings > tick SSH, HTTPS, HTTP | Auto-assign public IP: Enable
Storage 8 GiB > Launch instance
Wait for Running + 2/2 checks > Connect > SSH client > copy the ssh -i line
Instance > Security tab > security group > Edit inbound rules > Add rule: Custom TCP, 6060, 0.0.0.0/0 > Save

# LAPTOP (PowerShell, in folder with the .pem)
ssh -i "SElab.pem" ubuntu@PUBLIC_DNS

# ON THE VM
sudo apt update
sudo apt install -y docker.io git maven
git clone WEB_REPO_URL
cd WEB_REPO_NAME
mvn clean package
cat > Dockerfile <<'EOF'
FROM tomcat:9-jdk11
COPY target/*.war /usr/local/tomcat/webapps/
EOF
sudo docker build -t myimage .
sudo docker images
sudo docker run -d --name app-demo -p 6060:8080 myimage
sudo docker ps
# open http://PUBLIC_IP:6060/maven-web-app/

# CLEANUP: Instance state > Terminate, then End Lab