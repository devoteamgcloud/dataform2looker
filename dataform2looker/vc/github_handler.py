# Module used to implement a GitHub handler capable of pushing files into a target repo
import logging
import os

from github import Auth, Github, InputGitAuthor
from github.GithubException import UnknownObjectException

CONSOLE_LOGGER = logging.getLogger()


class GithubClient:
    """
    Class used to implement authentication into a GitHub repo
    via a Personal Access Token
    """

    def __init__(self, token: str, repo: str, user_email: str = None) -> None:
        """
        Creates a Github object using the authentication token.
        :param str token: The Personal Access Token used to authenticate
        to the repository,
        needs read/write access on Contents and Pull requests.
        :param str repo: The repo to access in format {owner}/{repo},
        such as sindresorhus/awesome
        :param str user_email User email to commit with:
        """
        self.token = token
        self.repo = repo
        self.user_email = user_email
        # Create a GitHub API client using the access token
        auth = Auth.Token(token)
        g = Github(auth=auth)
        self.repo = g.get_repo(repo)
        self.user = g.get_user()

    def update_files(
        self,
        input_dir: str,
        output_dir: str,
        target_branch: str,
        base_branch: str = "main",
        file_creation_message: str = None,
        file_update_message: str = None,
    ) -> None:
        """
        Method used to read all files from an input directory, create one commit
        per file, and push them to the target branch.
        :param str input_dir: Input directory, used to read all the files to
        commit, "../../views"
        :param str output_dir: Output directory in the target branch,
        MUST EXIST.
        :param str target_branch: Target branch, will be created if it
        does not exist
        :param str base_branch: Base branch to create the target branch from
        :param str file_creation_message: Commit message to use when creating
        a file
        :param str file_update_message: Commit message to use when updating
        a file
        :return:
        """
        # Pass login as email, since it's required but not tested
        if not self.user_email:
            self.user_email = self.user.login
        author = InputGitAuthor(self.user.login, self.user_email)
        branches = self.repo.get_branches()

        if target_branch in [b.name for b in branches]:
            CONSOLE_LOGGER.info(f"Branch {target_branch} already exists")
            branch = self.repo.get_git_ref(f"heads/{target_branch}")
        else:
            base_ref = self.repo.get_branch(base_branch)
            self.repo.create_git_ref(
                f"refs/heads/{target_branch}", sha=base_ref.commit.sha
            )
            CONSOLE_LOGGER.info(
                f"New branch {target_branch} created in repo {self.repo.name}"
            )

        # Read input files from the local directory
        files = []
        for file_name in os.listdir(input_dir):
            file_path = os.path.join(input_dir, file_name)
            with open(file_path, "r") as f:
                file_content = f.read()
            files.append({"name": file_name, "content": file_content})

        has_changes = False
        # Compare base layer files
        for file in files:
            output_path = output_dir + "/" + file["name"]
            contents = self.repo.get_contents(output_dir, ref=target_branch)

            if file["name"] in [content_file.name for content_file in contents]:
                if file_update_message:
                    message = file_update_message
                else:
                    message = f"update {file['name']}"
                content_file = self.repo.get_contents(output_path, ref=target_branch)
                # Compare file contents
                if content_file.decoded_content.decode() == file["content"]:
                    CONSOLE_LOGGER.info(
                        f"File {file['name']} already exists and it is up to date"
                    )
                    continue
                has_changes = True
                self.repo.update_file(
                    path=output_path,
                    message=message,
                    content=file["content"],
                    sha=content_file.sha,
                    branch=target_branch,
                    author=author,
                )
                CONSOLE_LOGGER.info(f"File {file['name']} has been updated")
                continue

            else:
                has_changes = True
                if file_creation_message:
                    message = file_creation_message
                else:
                    message = f"create {file['name']}"
                self.repo.create_file(
                    path=output_path,
                    message=message,
                    content=file["content"],
                    branch=target_branch,
                    committer=author,
                    author=author,
                )
                CONSOLE_LOGGER.info(f"File {file['name']} has been created")

        # Return if there are no changes
        if not has_changes:
            CONSOLE_LOGGER.info(
                "No changes detected. No commits have been made to the repository"
            )
            return

    def create_pull_request(
        self, base_branch: str, target_branch: str, pr_title: str, pr_body: str
    ) -> None:
        # Create a pull request if it does not exist
        pulls = self.repo.get_pulls(state="open", sort="created", base=base_branch)
        if target_branch in [pull.head.ref for pull in pulls]:
            CONSOLE_LOGGER.info(
                f"Pull request already exists for branch {target_branch}"
            )
            return

        # Create a new pull request
        pull_request = self.repo.create_pull(
            title=pr_title,
            body=pr_body,
            base=base_branch,
            head=f"{target_branch}",
            draft=True,
        )
        CONSOLE_LOGGER.info(f"Pull request created: {pull_request.html_url}")

    def delete_branch(self, branch_name: str) -> None:
        try:
            ref = self.repo.get_git_ref(f"heads/{branch_name}")
            ref.delete()
            CONSOLE_LOGGER.info(f"Branch {branch_name} deleted")
        except UnknownObjectException:
            CONSOLE_LOGGER.warning(f"{branch_name} does not exist")
