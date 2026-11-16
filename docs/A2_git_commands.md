# Part A2 — Git command table

| Command | Where the change happens | What exactly happens? |
|---|---|---|
| `git init` | Working folder → local repository | Creates the hidden `.git` repository metadata in the current folder. |
| `git add train.py` | Working folder → staging area | Marks the current version of `train.py` for the next commit. |
| `git commit -m "msg"` | Staging area → local repository | Records a snapshot and message in local Git history. |
| `git remote add origin URL` | Local repository configuration | Saves the remote repository URL under the name `origin`; it does not upload code. |
| `git push -u origin main` | Local repository → remote GitHub repository | Uploads local commits on `main` and sets its upstream tracking branch. |
| `git pull origin main` | Remote repository → local repository and working tree | Fetches remote commits and integrates them into the current branch (normally by merge). |

After `git commit`, a teammate cannot see the new commit on GitHub yet because it exists only in the local repository. It becomes visible on the remote after `git push`.
