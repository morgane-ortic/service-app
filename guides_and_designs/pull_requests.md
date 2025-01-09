# **Workflow for Feature Branches and Pull Requests**

## Step 1: Create a Feature Branch
1. Make sure your local repository is up-to-date:
   ```bash
   git fetch origin
   git checkout dev
   git pull origin dev
   ```
2. Create a new feature branch from dev:
   ```bash
   git checkout -b <feature-branch-name>
   ```
## Step 2: Commit and Push Your Changes
1. Add and commit your changes:
   ```bash
   git add .
   git commit -m "Brief description of the feature"
   ```
2. Push your feature branch to the remote repository:
   ```bash
   git push origin <feature-branch-name>
   ```
## Step 3: Open a Pull Request
1. Go to your GitHub
2. Navigate to the repository and look for the option to create a Pull Request.
3. Select your feature branch as the source branch and dev as the target branch.
## Step 4: Write a Clear Description
* Title: Summarize the feature (e.g., Add therapist app with registration feature).
* Description: Include:

    * What the feature does.
    * Key changes in the branch.
    * Dependencies (e.g., migrations, libraries).
    * Testing instructions (if applicable).
## Step 5: Assign Reviewer and Labels
* Assign [Reviewer’s Name] (person responsible for reviewing the dev branch) as the reviewer.
* Add appropriate labels (e.g., enhancement, bug, etc.).
## Step 6: Submit the Pull Request
Click Create Pull Request and wait for feedback or approval.
## Step 7: Update Your Feature Branch (If Necessary)
If updates are required in your branch after the pull request:
1. Pull the latest changes from dev:
   ```bash
   git fetch origin
   git checkout dev
   git pull origin dev
   ```
2. Merge dev into your feature branch to resolve conflicts:
   ```bash
   git checkout <feature-branch-name>
   git merge dev
   ```
3. Push the updated branch:
   ```bash
   git push origin <feature-branch-name>
   ```
4. Inform the reviewer that the branch has been updated.
## Step 8: Complete the Pull Request
Once the pull request is approved:
1. Merge the feature branch into dev.
2. Delete the feature branch from the remote repository:
   ```bash
   git push origin --delete <feature-branch-name>
   ```