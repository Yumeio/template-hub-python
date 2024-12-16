import subprocess, logging, os
from typing import Optional, Union
from pathlib import Path
from .folder_progress import FolderProgress

from httpx import DecodingError

logger = logging.getLogger(__name__)

class Repository():
    def __init__(
        self,
        local_dir: str,
        clone_url: Optional[str] = None,
        repo_type: Optional[str] = None,
        token: Union[str, None] = None,
        status_lfs: Optional[bool] = False,
        git_user: Optional[str] = None,
        git_email: Optional[str] = None
    ): 
        
        os.makedirs(local_dir, exist_ok=True)
        self.local_dir = Path(local_dir)
        
        self.check_git_version()
        self.configure_git_profile(git_user, git_email)
        
        if clone_url is not None:
            pass
        else:
            pass
        
        self.token = token
        self.repo_type = repo_type
        self.status_lfs = status_lfs
        
            
    def check_git_version(self):
        try:
            git_versions = subprocess.check_output(['git', '--version'], encoding='utf-8', stderr=subprocess.STDOUT, shell=True).strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Git is not installed: {e}")
            git_versions = 'Not installed'
        
        if(self.status_lfs):
            try:
                git_lfs_version = subprocess.check_output(['git', 'lfs', '--version'], encoding='utf-8', stderr=subprocess.STDOUT, shell=True).strip()
            except subprocess.CalledProcessError as e:
                logger.error(f"Git LFS is not installed: {e}")
                git_lfs_version = 'Not installed'

        logger.info(f"Git version: {git_versions}")
        if(self.status_lfs):
            logger.info(f"Git LFS version: {git_lfs_version}")
        else:
            logger.info("Git LFS is not enabled")
            
    def configure_git_profile(self, git_name: Optional[str] = None, git_email: Optional[str] = None):
        if git_name is None:
            git_name = subprocess.check_output(['git', 'config', '--global', 'user.name'], encoding='utf-8', stderr=subprocess.STDOUT, shell=True).strip()
        if git_email is None:
            git_email = subprocess.check_output(['git', 'config', '--global', 'user.email'], encoding='utf-8', stderr=subprocess.STDOUT, shell=True).strip()
        
        subprocess.run(['git', 'config', '--global', 'user.name', git_name],cwd= self.local_dir, check=True, shell=True)
        subprocess.run(['git', 'config', '--global', 'user.email', git_email], cwd= self.local_dir, check=True, shell=True)
    
    def init_repo(self):
        try:
            subprocess.run(['git', 'init'], cwd= self.local_dir, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error: {e}")
    
    def clone_repo(self, repo_url: str, token: Union[str, None] = None):
        if isinstance(token, str):
            api_token = token
        elif token:
            api_token = FolderProgress.get_token()
        else:
            api_token = None
            
        if(api_token is not None):
            repo_url = repo_url.replace("https://", f"https://user:{api_token}@")
        
        try:
            # init git lfs 
            subprocess.run(['git', 'lfs', 'install'], check=True, shell=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error: {e}")
        
        if(len(os.listdir(self.local_dir)) == 0):
            subprocess.run(['git', 'clone', repo_url, '.'], cwd= self.local_dir, check=True, shell=True)
        else:
            logger.warning("Directory is not empty, let's try to pull")
            self.init_repo()
            self.add_remote(repo_url)
            self.git_fetch()
            self.git_pull()
            self.git_reset_origin(branch="master")
            
            
    def check_remote(self):
        try:
            remotes = subprocess.run(['git', 'remote', '-v'], cwd= self.local_dir, check=True, shell=True)
            logger.debug("Your repository has remotes")
            logger.debug(f"Remote: {remotes}")
        except subprocess.CalledProcessError as e:
            logger.error("Your repository has no remotes")
            logger.error("You need to add a remote to your repository")
            logger.error(f"Error: {e}")
            
    def add_remote(self, remote_url: str): 
        try:
            subprocess.run(['git', 'remote', 'add', 'origin', remote_url], cwd= self.local_dir, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error: {e}")          
    
    def git_add(self, command: str = "."):
        subprocess.run(['git', 'add', command], cwd= self.local_dir, check=True, shell=True)
    
    def git_commit(self, message: str):
        subprocess.run(['git', 'commit', '-m', message], cwd= self.local_dir, check=True, shell=True)
    
    def git_push(self):
        subprocess.run(['git', 'push'], cwd= self.local_dir, check=True, shell=True)
    
    def git_pull(self, rebased: Optional[bool] = False):
        if rebased:
            subprocess.run(['git', 'pull', '--rebase'], cwd= self.local_dir, check=True, shell=True)
        else:
            subprocess.run(['git', 'pull'], cwd= self.local_dir, check=True, shell=True)
    
    def git_fetch(self):
        subprocess.run(['git', 'fetch'], cwd= self.local_dir, check=True, shell=True)
        
    def git_status(self):
        subprocess.run(['git', 'status'], cwd= self.local_dir, check=True, shell=True)
        
    def git_log(self):
        subprocess.run(['git', 'log'], cwd= self.local_dir, check=True, shell=True)

    def git_reset_origin(self, branch: str = "master"):
        subprocess.run(['git', 'reset', '--hard', f'origin/{branch}'], cwd= self.local_dir, check=True, shell=True)
        
    def enable_lfs(self):
        self.status_lfs = True
    
    def enable_lfs_large_files(self, file: str):
        pass
    
    def lfs_track(self, file: str):
        pass
    
    def lfs_untrack(self, file: str):
        pass
    
    def lfs_push(self):
        pass
    
    def push_to_hub(self, message: str = "Push to Hub"):
        self.git_add()
        self.git_commit(message)
        self.git_push()