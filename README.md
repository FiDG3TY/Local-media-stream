# Local-media-stream
# After configration



* Create file: directly by right-clicking on folder -- new.

* Check status: git status
  1) Clean repository: no changes.
  2) Modified files.
     a) Changes not staged for commit: changes not added yet on existing files. 
       - git add <file_name>
     b) Changes staged for commit: changes added but not commited yet on existing files.
       - git commit -m "some message"
  3) Untracked files: new file created but not added yet. 
     - git add <file_name>
  4) Ahead/behind remote branch: changes saved but yet to push.
     - git push
  5) Conflicts: shows files with merge conflicts.
  6) Other stages: To resolve move to staged state.
    a) Renamed files: Files renamed or moved.
      - git mv old_name new_name 
    b) Deleted files: Files removed from the repository.
      - git rm file
    c) Copied files: Files copied to a new location.
      - add <new_location>
    d) Type changes: Changes in file type.
     - git add <file>
    e) Permission changes: Changes in file permissions.
     - git add <file>
     

* Add: it is a command that stages changes in your working directory, preparing them to be committed
  - git add .


* Commit: it means saving your changes with a brief message explaining what you did.
  - git commit -m "Fixed login issue"


* Merge: it combines changes from one branch into another.
  ** Merge Process

  1. Checkout the target branch: Switch to the branch where you want to save changes.
     - git checkout <branch-name>
  2. Merge the source branch: Integrate changes from the source branch.
     - git merge <branch-name>
  3. Resolve conflicts (if any): Git highlights conflicts. Manually resolve them, then commit the resolved changes.
  4. Add and Commit the merge: add and commit, combining changes from both branches.

  
                
