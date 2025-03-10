import os
import subprocess
import json
import tarfile
from datetime import datetime

class DevOpsAutomation:
    def __init__(self, project_name):
        self.project_name = project_name
        self.env = "production"
        self.db_credentials = {}
        self.git_repo_url = ""
        self.deploy_dir = f"/var/www/{self.project_name}"
    
    def configure_environment(self):
        print(f"[INFO] Configuring environment for {self.project_name}")
        os.makedirs(self.deploy_dir, exist_ok=True)

    def set_database_credentials(self, host, user, password, db_name):
        self.db_credentials = {
            "host": host,
            "user": user,
            "password": password,
            "db_name": db_name
        }
        print("[INFO] Database credentials set")

    def clone_repository(self, repo_url):
        self.git_repo_url = repo_url
        print(f"[INFO] Cloning repository from {self.git_repo_url}")
        subprocess.run(["git", "clone", self.git_repo_url, self.deploy_dir], check=True)
    
    def build_application(self):
        print("[INFO] Building the application")
        subprocess.run(["npm", "install"], cwd=self.deploy_dir, check=True)
        subprocess.run(["npm", "run", "build"], cwd=self.deploy_dir, check=True)

    def run_tests(self):
        print("[INFO] Running tests")
        result = subprocess.run(["npm", "test"], cwd=self.deploy_dir, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            raise Exception("[ERROR] Tests failed")

    def deploy_application(self):
        print(f"[INFO] Deploying application to {self.deploy_dir}")
        subprocess.run(["npm", "start"], cwd=self.deploy_dir, check=True)

    def create_backup(self):
        backup_file = f"{self.project_name}_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.tar.gz"
        print(f"[INFO] Creating backup: {backup_file}")
        with tarfile.open(backup_file, "w:gz") as tar:
            tar.add(self.deploy_dir, arcname=os.path.basename(self.deploy_dir))
        print("[INFO] Backup completed")

    def update_application(self):
        print("[INFO] Updating application")
        subprocess.run(["git", "pull"], cwd=self.deploy_dir, check=True)
        self.build_application()
    
    def send_notification(self, message):
        print(f"[NOTIFICATION] {message}")

    def run(self):
        self.configure_environment()
        self.clone_repository(self.git_repo_url)
        self.build_application()
        self.run_tests()
        self.deploy_application()
        self.create_backup()
        self.send_notification(f"{self.project_name} deployed successfully")

if __name__ == "__main__":
    project_name = "my_app"
    automation = DevOpsAutomation(project_name)
    automation.set_database_credentials("localhost", "user", "password", "my_db")
    automation.git_repo_url = "https://github.com/user/my_app.git"
    automation.run()