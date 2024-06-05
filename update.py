import os
import git

def update_project(branch_name):
    try:
        # Get the current working directory, which is the project directory
        local_dir = os.getcwd()

        # Access token should be set as an environment variable for security reasons
        access_token = os.getenv("GITHUB_ACCESS_TOKEN")
        if not access_token:
            raise EnvironmentError("GITHUB_ACCESS_TOKEN is not set in the environment variables.")

        # Assuming 'debu8er' and 'watch' are placeholders for user and repo, consider making them parameters or environment variables
        repo_url = f"https://{access_token}@github.com/debu8er/watch.git"

        repo = git.Repo(local_dir)

        # Set the remote URL to the authenticated URL
        origin = repo.remote()
        origin.set_url(repo_url)

        # Fetch the latest changes from the remote repository
        origin.fetch()

        # Check if the branch exists
        if branch_name not in repo.branches:
            raise ValueError(f"The branch '{branch_name}' does not exist.")

        # Check out the branch you want to update
        repo.git.checkout(branch_name)

        # Pull the latest changes from the branch
        repo.git.pull(origin, branch_name)

        print("Project has been updated successfully using GitPython.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    branch_name = "main"  # Change this to the branch you want to update from
    update_project(branch_name)
