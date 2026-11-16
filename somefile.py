# SE Lab Internal-2: Complete Experiment Guide

Covers: Docker (single + multi-container), Jenkins (freestyle, pipeline script, webhooks, email), Kubernetes + Nagios, AWS VPC + EC2 deployment.
Built from your 8 lab manuals and the screenshots inside the AWS manual, with fixes where the manuals are wrong or incomplete.

## Read first

- **Do not paste commands from the Word files.** The AWS manual has `docker build –t`, `–d`, `–p` and the Compose manual has `docker-compose up –d` with typographic en-dashes. Docker rejects them. Type commands yourself.
- **Your AWS lab used AWS Academy Learner Lab**, not a normal free-tier account (screenshots show a Canvas course, "Used $0 of $50" and a ~4 hour timer).
- **Running each experiment once yourself before the exam is non-negotiable.** Whatever you have never run is what you will fumble under the clock.
- **Take a screenshot after every step.** Every manual ends with "upload the screenshots".

---

## PART 1: Experiments (16)

| # | Experiment | What you must show |
|---|---|---|
| 1 | Docker CLI with Redis | pull, run, exec, stop, start, rm, rmi |
| 2 | Dockerfile, build, commit, push to Docker Hub, pull, run | Image on Docker Hub, SET/GET works |
| 3 | Compose: Nginx + Postgres | Nginx page on :8080 |
| 4 | Compose: add Redis + depends_on | 3 services running |
| 5 | Compose: portability | Same stack runs on another machine/folder |
| 6 | Compose: network + volume | Data survives down/up |
| 7 | Compose: Flask app with build | Message changes after rebuild |
| 8 | Jenkins freestyle chain: Maven Java | Build then Test pipeline view, all green |
| 9 | Jenkins freestyle chain: Maven Web | Build, Test, Deploy to Tomcat, app opens |
| 10 | Jenkins pipeline script + build triggers | 4 stages green |
| 11 | GitHub webhook + ngrok | A `git push` auto-starts a build |
| 12 | Jenkins email notification (Gmail) | Email arrives |
| 13 | Minikube: deploy, expose, scale nginx | 4 pods, app opens |
| 14 | Nagios in Docker | Dashboard on :8888 |
| 15 | Custom VPC + subnets + IGW + route tables + EC2 | Working public instance, isolated private one |
| 16 | EC2 Ubuntu, Docker, deploy Maven web app | App opens on the public IP |

## PART 2: Accounts and tools to have ready

| Need | Used in | Have ready |
|---|---|---|
| **GitHub account** with Maven-Java and Maven-Web repos (each with `pom.xml`) | 8-12, 16 | HTTPS clone URLs and the real default branch (`main` or `master`) |
| **Docker Hub account** | 2 | Username + password. Run `docker login` once before the exam to confirm it works. |
| **Docker** (Desktop or Engine) + Git Bash or WSL | 1-7, 13, 14 | `docker version` works |
| **Jenkins** on `localhost:8080` | 8-12 | Admin login, JDK and Maven configured |
| **Jenkins plugins** | 8-12 | Git, GitHub, Maven Integration, Pipeline, Copy Artifact, Build Pipeline, Deploy to container, Email Extension |
| **Tomcat 9 on port 8085** | 9 | User `admin` / `1234` with roles `manager-script` and `manager-gui` in `tomcat-users.xml` |
| **ngrok account + executable** | 11 | Authtoken from the ngrok dashboard |
| **Google account with 2-Step Verification** | 12 | A 16-character app password |
| **minikube + kubectl** | 13 | `minikube version` and `kubectl version --client` work |
| **AWS access** | 15, 16 | AWS Academy Learner Lab via Canvas (or free-tier account), SSH client, key pair `.pem` |

Also do beforehand:
- **Pre-pull images** so you don't depend on exam Wi-Fi: `redis`, `nginx`, `postgres:15`, `redis:alpine`, `python:3.10-slim`, `tomcat:9-jdk11`, `jasonrivers/nagios`.
- **Match the Maven name exactly.** The freestyle manual says `MAVEN_HOME`, the pipeline manual says `MAVEN-HOME`. Use whatever name you saved in *Manage Jenkins > Tools*. A mismatch fails the job.

### Account notes

**AWS login**
- Learner Lab: https://www.awsacademy.com/LMS_Login (from memory; if it fails, use the Canvas link from your college invite email or ask your lab faculty). Then course > Modules > AWS Academy Learner Lab > Launch > Start Lab.
- Normal free-tier account: https://console.aws.amazon.com (Root user) or https://aws.amazon.com to sign up.
- Learner Lab needs a student account provisioned by your college through an invite. You cannot self-sign-up. A personal AWS account also works for Exp 15 and 16 (needs a payment card; delete NAT Gateways and stop/terminate EC2 when done; check current free-tier terms). Ask your faculty which one the exam uses.
- Can't remember which email: search all inboxes for "AWS Academy", "Canvas" or "awsacademy". Otherwise ask faculty to re-send the invite.
- **AWS Builder ID is not your Learner Lab login and not a console account.** It is for Skill Builder, re:Post, CodeCatalyst. It supports optional MFA. Manage/reset at https://profile.aws.amazon.com > Security > Change password, or on the sign-in page "Trouble Signing In?" > "Forgot password?".

**Gmail app password (needed for Exp 12)**
- An app password is a 16-character password Google generates for one app (Jenkins). It replaces your real password for sending mail. It cannot log into the Gmail website. 2-Step Verification must be on first.
- Create: https://myaccount.google.com > Security > turn on 2-Step Verification > search "App passwords" (or https://myaccount.google.com/apppasswords) > name `Jenkins-Demo` > Create > copy the 16 characters and **remove spaces**. You cannot view it again, so save it on paper or a phone note.
- Use in Jenkins: username = full Gmail address, password = the app password.
- Exam-hall safety: generate it before the exam so you never need to log into Gmail on the exam PC. Check the inbox on your phone. Download Google backup codes (Security > 2-Step Verification > Backup codes). Don't change your Google password before the exam (that revokes app passwords). Ask whether phones are allowed. Fallback: screenshot of Jenkins "Email was successfully sent" plus the job's Editable Email Notification settings.

---

## PART 3: Step-by-step

### Exp 1: Docker CLI with Redis
```
docker pull redis
docker run --name my-redis -d redis
docker ps
docker exec -it my-redis redis-cli
    SET name "Alice"
    GET name            -> "Alice"
    exit
docker stop my-redis
docker start my-redis
docker stop my-redis     (stop before removing)
docker rm my-redis
docker rmi redis
```
Screenshot after each command.

### Exp 2: Dockerfile to Docker Hub
1. Make a folder (`mkdir Redis && cd Redis`) and create a file named exactly `Dockerfile`, no extension:
   ```
   FROM redis:latest
   CMD ["redis-server"]
   ```
2. Run in order:
   ```
   docker build -t redisnew .
   docker run --name myredisnew -d redisnew
   docker ps
   docker stop myredisnew
   docker login                                  (Docker Hub credentials)
   docker ps -a
   docker commit myredisnew <hubuser>/redis1
   docker images
   docker push <hubuser>/redis1
   docker rm myredisnew
   docker rmi <hubuser>/redis1
   docker ps -a
   docker logout
   docker pull <hubuser>/redis1
   docker run --name myredis -d <hubuser>/redis1
   docker exec -it myredis redis-cli
       SET name "Abcdef"
       GET name
       exit
   docker ps -a
   docker stop myredis
   docker rm myredis
   docker images
   docker rmi <hubuser>/redis1
   ```
- Replace `budarajumadhurika` with your own Docker Hub username. The manual's container IDs (`0e993d2009a1`, `50a6e4a9c326`) are the author's; use container names instead.
- Image name must be `<username>/<repo>` or the push is rejected.
- If `pull` says "access denied" after logout, the repo is private. Make it public on Docker Hub.
- `docker build` creates an image from a Dockerfile; `docker commit` snapshots a container into an image.

### Exp 3-7: Docker Compose
Make a folder `compose-lab` with `docker-compose.yml` in it. The manual's plain-text export lost YAML indentation; use the indentation below, it matters. The manual starts with `version: "3.9"`. Compose treats the top-level `version` element as obsolete, so you only get a harmless warning. Keep it if you want to match the manual.

**Exp 3: Nginx + Postgres**
```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: demo
      POSTGRES_PASSWORD: demo
      POSTGRES_DB: demo_db
```
`docker compose up -d`, then open `http://localhost:8080` for the Nginx welcome page. Also `docker compose ps`.

**Exp 4: add Redis + depends_on**
Add the service:
```yaml
  redis:
    image: redis:alpine
```
Under `web:` add:
```yaml
    depends_on:
      - redis
```
`docker compose up -d` and `docker compose ps`: 3 services. `depends_on` controls start order only, it does not wait for readiness.

**Exp 5: portability**
1. `docker compose down`, zip the `compose-lab` folder.
2. Copy to another machine with Docker, unzip, `docker compose up -d`.
3. Check Nginx on :8080 and `docker compose ps`.
Only one machine? Copy the folder to a different directory and run from there; say so in your write-up.

**Exp 6: network + volume**
```yaml
networks:
  app-net:
volumes:
  db-data:
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    networks:
      - app-net
    depends_on:
      - db
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
```
```
docker compose up -d
docker compose exec db psql -U demo -d demo_db -c "CREATE TABLE students(id int, name text);"
docker compose exec db psql -U demo -d demo_db -c "INSERT INTO students VALUES (1,'Alice');"
docker compose down
docker compose up -d
docker compose exec db psql -U demo -d demo_db -c "SELECT * FROM students;"     <- row is still there
docker network ls        (shows compose-lab_app-net)
docker volume ls         (shows compose-lab_db-data)
```
`docker compose down -v` deletes the volume, so don't use `-v` here or the data is gone.

**Exp 7: Flask with build**
`app.py`:
```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Flask + Docker!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```
`Dockerfile`:
```
FROM python:3.10-slim
WORKDIR /app
COPY app.py /app/
RUN pip install flask
CMD ["python", "app.py"]
```
`docker-compose.yml`:
```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: demo
      POSTGRES_PASSWORD: demo
      POSTGRES_DB: demo_db
```
```
docker compose up --build        -> open http://localhost:5000
```
Edit the return text in `app.py`, run `docker compose up --build` again, refresh. The code is copied at build time, which is why you must rebuild. If you see an "orphan containers" warning from earlier tasks, add `--remove-orphans`.

### Exp 8: Jenkins freestyle chain, Maven Java
Create `MavenJava_Test` first, because the Build job's "Build other projects" field rejects a project that does not exist yet.

**Job A: `MavenJava_Test`**
1. Dashboard > New Item > name `MavenJava_Test` > Freestyle project > OK.
2. Description: "Test demo".
3. Build Environment: tick **Delete workspace before build starts**.
4. Build Steps > Add build step > **Copy artifacts from another project**: Project name `MavenJava_Build`, tick **Stable build only**, Artifacts to copy `**/*`.
5. Add build step > **Invoke top-level Maven targets**: Maven Version = your Maven name, Goals = `test`.
6. Post-build Actions > **Archive the artifacts**, Files = `**/*`.
7. Save.

**Job B: `MavenJava_Build`**
1. New Item > `MavenJava_Build` > Freestyle > OK. Description: "Java Build demo".
2. Source Code Management > **Git**: Repository URL = your Maven-Java repo, Branch = `*/main` (or `*/master`, match your repo).
3. Build Steps > Invoke top-level Maven targets > Goals = `clean`. Add a second step with Goals = `install`.
4. Post-build Actions > **Archive the artifacts**, Files = `**/*`.
5. Post-build Actions > **Build other projects**, Projects = `MavenJava_Test`, trigger **only if build is stable**.
6. Save.

**Pipeline view**
1. Dashboard: click **+** next to "All", name `MavenJava_Pipeline`, choose **Build Pipeline View**, Create.
2. Layout: "Based on upstream/downstream relationship", Initial job = `MavenJava_Build`. Apply, OK.
3. Click **Run**. Click the small black box on a stage to open its console.
4. Both boxes turn green, and the Test job starts by itself. Screenshot the configs, the green view and the console ("Finished: SUCCESS").

### Exp 9: Jenkins freestyle chain, Maven Web
Three jobs: Build > Test > Deploy. Create them in reverse order (Deploy first) so the "Build other projects" names exist.

**`MavenWeb_Deploy`**
1. New Item, freestyle. Description: "Web Code Deployment".
2. Tick **Delete workspace before build starts**.
3. Build step *Copy artifacts from another project*: project `MavenWeb_Test`, Stable build only, `**/*`.
4. Post-build > **Deploy WAR/EAR to a container**:
   - WAR/EAR files: `**/*.war`
   - Context path: `Webpath`
   - Add container > **Tomcat 9.x Remote**
   - Credentials > Add > Jenkins > username `admin`, password `1234`
   - Tomcat URL: `http://localhost:8085/`
5. Save.

**`MavenWeb_Test`**
1. Description: "Test demo". Tick Delete workspace.
2. Copy artifacts from `MavenWeb_Build` (stable only, `**/*`).
3. Maven goal `test`.
4. Post-build: Archive `**/*`, then Build other projects > `MavenWeb_Deploy`.

**`MavenWeb_Build`**
1. SCM Git > your Maven-Web repo.
2. Maven goals `clean`, then `install`.
3. Post-build: Archive `**/*`, then Build other projects > `MavenWeb_Test` (only if stable).

**View and verify**
1. Create the view `MavenWeb_Pipeline` (Build Pipeline View, initial job `MavenWeb_Build`) and click Run.
2. When all three are green, open `http://localhost:8085/` > **Manager App** (log in with the Tomcat credentials).
3. Click `/Webpath` in the application list to see the output. You can also open `http://localhost:8085/Webpath/` directly.

Watch out:
- The manual writes `https://localhost:8085/`. Stock Tomcat serves plain http; use https only if you configured TLS.
- Deploy fails with 401/403 when the Tomcat user lacks the `manager-script` role.

### Exp 10: Pipeline script + build triggers
**Part 1: the pipeline**
1. New Item > name > **Pipeline** (not Freestyle) > OK. Add a description.
2. Scroll to **Pipeline > Definition: Pipeline script**, paste the script below, Apply and Save.
3. **Build Now**, then open Console Output.

```groovy
pipeline {
    agent any
    tools {
        maven 'MAVEN-HOME'          // must match your Tools name exactly
    }
    stages {
        stage('git repo & clean') {
            steps {
                bat "if exist mavenjava rmdir /s /q mavenjava"
                bat "git clone https://github.com/<user>/mavenjava.git"
                bat "mvn clean -f mavenjava"
            }
        }
        stage('install') {
            steps { bat "mvn install -f mavenjava" }
        }
        stage('test') {
            steps { bat "mvn test -f mavenjava" }
        }
        stage('package') {
            steps { bat "mvn package -f mavenjava" }
        }
    }
}
```
- The `if exist ... rmdir` line is added by me. Without it the second build fails with "destination path already exists", because the workspace keeps the cloned folder. The manual leaves that line commented out, which is a trap.
- The folder name must equal your repo name; `-f mavenjava` points at the cloned folder.
- On Linux replace `bat` with `sh`.

**Your manual calls this "scripted", but the code above is declarative** (`pipeline { agent any ... }`). A true scripted pipeline starts with `node`. If the examiner asks for scripted syntax:
```groovy
node {
    def mvnHome = tool 'MAVEN-HOME'
    withEnv(["PATH+MAVEN=${mvnHome}\\bin"]) {
        stage('git repo & clean') {
            bat "if exist mavenjava rmdir /s /q mavenjava"
            bat "git clone https://github.com/<user>/mavenjava.git"
            bat "mvn clean -f mavenjava"
        }
        stage('install') { bat "mvn install -f mavenjava" }
        stage('test')    { bat "mvn test -f mavenjava" }
        stage('package') { bat "mvn package -f mavenjava" }
    }
}
```

**Part 2: build triggers.** Job > Configure > **Build Triggers**, pick one:

| Trigger | Value |
|---|---|
| Build periodically | `0 18 * * *` (every day 6 PM; Jenkins suggests `H` but accepts this) |
| Poll SCM | `H/5 * * * *` (checks GitHub about every 5 minutes) |
| GitHub hook trigger for GITScm polling | Tick it (Exp 11) |
| Build after other projects are built | Upstream project name (the freestyle chain) |

Inside a declarative script you can also write `triggers { cron('0 18 * * *') }`.

### Exp 11: GitHub webhook + ngrok
1. **ngrok setup.** Sign up, download ngrok, then:
   ```
   ngrok config add-authtoken <your_token>
   ngrok http 8080
   ```
   Copy the HTTPS `Forwarding` URL and keep that terminal open. The free URL changes every restart, so update the webhook each time.
2. **GitHub:** repo > Settings > Webhooks > Add webhook.
   - Payload URL: `https://<ngrok-url>/github-webhook/` (keep the trailing slash; the manual shows a stray space before `/github-webhook/`, don't type it).
   - Content type: `application/json`.
   - Events: **Just the push event**. Add webhook.
   - Check *Recent Deliveries* for a green tick (HTTP 200).
3. **Jenkins:** job > Configure > Build Triggers > tick **GitHub hook trigger for GITScm polling** > Save. Works for freestyle and pipeline jobs. The job's SCM must point to the same repo and branch.
4. **Test:**
   ```
   git add .
   git commit -m "webhook test"
   git push
   ```
   A build should start in Jenkins within seconds with no manual click.

### Exp 12: Email notification (Gmail)
1. **Create the app password** (see Account notes above). Requires 2-Step Verification.
2. **Install the plugin.** Manage Jenkins > Plugins (older: Manage Plugins) > Available > **Email Extension Plugin**.
3. **Global settings.** Manage Jenkins > System (older: Configure System):
   - **Jenkins Location > System Admin e-mail address:** set to your Gmail address (Gmail may reject mail if it doesn't match the SMTP user).
   - **E-mail Notification** section: SMTP server `smtp.gmail.com`. Under Advanced: tick **Use SMTP Authentication** (your Gmail + the app password) and **Use SSL**, port `465`. Gmail accepts 465 with SSL or 587 with STARTTLS. Tick **Test configuration by sending test e-mail**, enter an address, click Test. You want "Email was successfully sent".
   - **Extended E-mail Notification** section: SMTP `smtp.gmail.com`, port `465`, Use SSL, Credentials > Add (Gmail + app password), Default content type `text/html`.
4. **Job:** Configure > Post-build Actions > **Editable Email Notification**:
   - Project Recipient List: your email address.
   - Advanced Settings > **Triggers > Add** > *Failure* and/or *Success*. **With no trigger added, no email is ever sent.**
5. **Test.** Run a build and check your inbox. To see the Failure email, break the build on purpose (for example a wrong Maven goal).

### Exp 13: Minikube, deploy / expose / scale
Docker Desktop must be running first.
```
minikube start --driver=docker
minikube status
kubectl get nodes
kubectl create deployment mynginx --image=nginx
kubectl get deployments
kubectl get pods
kubectl describe pods
kubectl expose deployment mynginx --type=NodePort --port=80 --target-port=80
kubectl get service mynginx
kubectl scale deployment mynginx --replicas=4
kubectl get pods                                  -> 4 pods
kubectl port-forward svc/mynginx 8081:80          -> http://localhost:8081 (keep terminal open)
minikube dashboard
```
Cleanup:
```
kubectl delete deployment mynginx
kubectl delete service mynginx
minikube stop
minikube delete      (optional)
```
- The manual's `kubectl get service myngnix` is a typo. Use `mynginx`.
- If `port-forward` errors, use `minikube service mynginx --url` and keep that terminal open. The manual suggests `minikube tunnel`, but that is aimed at LoadBalancer services, not your NodePort service. If unsure which works on the exam machine, try both.
- Update an existing deployment: `kubectl set image deployment/mynginx nginx=nginx:latest`.

### Exp 14: Nagios in Docker
```
docker pull jasonrivers/nagios:latest
docker run --name nagiosdemo -p 8888:80 jasonrivers/nagios:latest
```
That `run` blocks the terminal; use a second terminal or add `-d`.
1. Open `http://localhost:8888`. Login `nagiosadmin`, password `nagios` (web UI is on container port 80).
2. Explore **Hosts**, **Services** (CPU load, ping etc.) and the alerts/problems pages.
3. Click a host to see its status (UP/DOWN), metrics, and the actions: reschedule check, disable notifications, schedule downtime.
4. Cleanup:
   ```
   docker stop nagiosdemo
   docker rm nagiosdemo
   docker rmi jasonrivers/nagios:latest
   ```
Real-time logs: `docker logs -f nagiosdemo`.

### Exp 15: Custom VPC (AWS console)
In Learner Lab stay in the region the lab gives you (your screenshots use us-east-1).
1. **VPC.** VPC > Create VPC > VPC only. Name `Custom-VPC`, IPv4 CIDR `10.0.0.0/16` > Create.
2. **Subnets.** Subnets > Create subnet > pick Custom-VPC. Create `Public-Subnet` `10.0.1.0/24` and `Private-Subnet` `10.0.2.0/24`, both in the same AZ as in the manual.
   - The manual says same-AZ subnets give high availability. That is wrong: high availability means subnets in *different* AZs. Expect a viva question on it.
3. **Internet gateway.** Internet gateways > Create `Custom-IGW` > Actions > **Attach to VPC** > Custom-VPC.
4. **Route tables.**
   - Create `Public-RT` on Custom-VPC. Edit routes > add `0.0.0.0/0` > target Internet Gateway `Custom-IGW`. Subnet associations > `Public-Subnet`.
   - Create `Private-RT` on Custom-VPC, keep only the local route. Associate with `Private-Subnet`.
5. **Public IP.** Select `Public-Subnet` > Actions > **Edit subnet settings** > tick **Enable auto-assign public IPv4 address**.
6. **Security groups** (EC2 > Security Groups, VPC = Custom-VPC):
   - `Web-SG`: inbound HTTP 80 and HTTPS 443 from `0.0.0.0/0`, SSH 22 from **My IP**.
   - `Private-SG`: SSH 22 from source `Web-SG`.
7. **Launch two EC2 instances.**
   - Public: Custom-VPC, `Public-Subnet`, auto-assign public IP **on**, `Web-SG`.
   - Private: `Private-Subnet`, public IP **off**, `Private-SG`.
8. **Test.**
   - SSH into the public instance and run `ping 8.8.8.8` (replies expected).
   - The private instance has no public IP, so nothing from the internet can reach it. Reach it from the public instance: `ssh -i key.pem ubuntu@10.0.2.x`.
   - The manual's "Private EC2 > Internet via NAT" has **no step that creates a NAT**. To make it true, create a NAT Gateway in `Public-Subnet` with an Elastic IP, then add `0.0.0.0/0 > nat-xxxx` to `Private-RT`. NAT Gateways bill by the hour, so delete it after your screenshots.

### Exp 16: EC2 Ubuntu, Docker, deploy Maven web app
**A. Start AWS (Learner Lab)**
1. Canvas > AWS Academy Learner Lab > **Start Lab**. Wait for the dot next to "AWS" to turn green, then click **AWS** to open the console. The timer in your screenshot is about 4 hours, and EC2 instances can stop or change IP when a session ends.

**B. Launch the instance** (EC2 > Launch instance)
1. Name: `Myserver`.
2. AMI: **Ubuntu Server** (free-tier eligible), 64-bit x86.
3. Instance type: `t2.micro` (your screenshot shows `t3.micro`; use whichever is free-tier eligible).
4. Key pair: **Create new** (for example `SElab`), downloads a `.pem`. Store it in your AWS folder.
5. Network settings: Create security group, tick **SSH, HTTPS and HTTP**, auto-assign public IP **Enable**.
6. Storage 8 GiB. Number of instances 1. **Launch instance.**
7. Wait for *Running* and status checks 2/2 (your screenshot caught it at 0/2 right after launch).

**C. Connect**
1. Select the instance > **Connect > SSH client**, copy the two commands. Run from the folder holding the `.pem`:
   ```
   chmod 400 "SElab.pem"
   ssh -i "SElab.pem" ubuntu@ec2-xx-xx-xx-xx.compute-1.amazonaws.com
   ```
2. In WSL under `/mnt/c/...`, `chmod` doesn't stick and you get "UNPROTECTED PRIVATE KEY FILE". Copy the `.pem` into `~` and `chmod 400` it there.
3. Fallback: the **EC2 Instance Connect** web-browser tab.

**D. Install, clone, write the Dockerfile** (on the VM)
```
sudo apt update
sudo apt-get install -y docker.io
sudo apt install -y git nano
git clone <your-maven-web-java-repo-url>
cd <repo-folder>
nano Dockerfile
```
Dockerfile (from your screenshot):
```
FROM tomcat:9-jdk11
COPY **/*.war /usr/local/tomcat/webapps/
```
The two commented lines in your screenshot (`EXPOSE 8080`, `CMD catalina.sh run`) are optional; the Tomcat base image already provides them. Save in nano: Ctrl+O, Enter, Ctrl+X.

Your repo must contain the built `.war` (for example `target/yourapp.war`), because this flow never runs Maven on the VM. If not, `COPY` fails. Either commit the `.war`, or `sudo apt install maven -y` and run `mvn package` before building. If the `**` glob misbehaves, use `COPY target/*.war /usr/local/tomcat/webapps/`.

**E. Build and run**
```
sudo docker build -t myimage .
sudo docker images
sudo docker run -d --name app-demo -p 6060:8080 myimage
sudo docker ps
```
- Use `sudo` on every `docker` command (the manual omits it; you'll get "permission denied" otherwise). Or run `sudo usermod -aG docker ubuntu && newgrp docker` once.
- Match the port to your image. Your Dockerfile screenshot uses Tomcat, so `6060:8080`. Your build screenshot shows an nginx static site with `6060:80`. Use the container port your image actually listens on.

**F. Open it publicly**
1. Console: instance > **Security** tab > click the security group > **Edit inbound rules > Add rule**: Custom TCP, port `6060`, source `0.0.0.0/0` > Save.
2. Browse to `http://<public-ip>:6060/<war-name-without-.war>/`. Type `http://` explicitly; Chrome sometimes upgrades to https.
3. Shortcut that skips the rule edit: run with `-p 80:8080` (HTTP 80 is already open), then browse to `http://<public-ip>/<war-name>/`.
4. Cleanup: instance state > Stop or Terminate, then End Lab.

**G. Account signup, only if asked** (the manual's list):
1. Go to aws.amazon.com > Create AWS account.
2. Enter email and name, then the emailed verification code.
3. Enter contact details and accept the terms.
4. Enter billing details. A small charge is credited back after verification.
5. Verify your phone with an SMS code.
6. Choose the Basic plan > Complete sign-up > open the Management Console.
7. Set role Academic/Researcher and interest DevOps, then sign in as Root user.

---

## Sources

- Docker Hub: jasonrivers/nagios, https://hub.docker.com/r/jasonrivers/nagios
- Docker docs, Compose version element, https://docs.docker.com/reference/compose-file/version-and-name/
- ngrok docs, GitHub to Jenkins webhook, https://ngrok.com/docs/gateway/webhooks-to-on-prem/github-to-jenkins.md
- Nodemailer, Gmail app passwords, https://nodemailer.com/guides/using-gmail
- Gmail SMTP settings, https://hothawk.ai/resources/gmail-smtp-settings
- AWS Builder ID MFA, https://docs.aws.amazon.com/signin/latest/userguide/mfa-builder-id.md
- AWS Builder ID password change, https://docs.aws.amazon.com/signin/latest/userguide/change-password-aws_builder_id.html

Everything else comes from your 8 lab manuals and their screenshots.
#   t e s t r e p o  
 