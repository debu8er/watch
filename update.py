import os
import git

# Set your personal access token
access_token = "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"

def update_project(branch_name):
    try:
        # Get the current working directory, which is the project directory
        local_dir = os.getcwd()

        # Construct the authenticated URL with your access token
        repo_url = f"https://{access_token}@github.com/debu8er/watch.git"

        repo = git.Repo(local_dir)

        # Set the remote URL to the authenticated URL
        origin = repo.remote()
        origin.set_url(repo_url)

        # Fetch the latest changes from the remote repository
        origin.fetch()

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
