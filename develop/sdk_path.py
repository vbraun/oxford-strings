
from .git_interface import GitInterface, GitError


GIT_CONFIG_HELP = """
Google Appengine SDK path not configured. Run something like

    git config googleappengine.path /home/vbraun/opt/google_appengine

in the project directory to set it up.
""".strip()


def get_sdk_path():
    git = GitInterface()
    try:
        return git.config('googleappengine.path').strip()
    except GitError:
        print(GIT_CONFIG_HELP)
        import sys
        sys.exit(1)
