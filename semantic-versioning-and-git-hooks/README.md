# Semantic Versioning
---
## Description

- Purposes: 2 main purposes: 

    - `From waypoint 1-6`: For those who would like to write step by step a class Version has 3 attributes named `major`, `minor`, and `patch` . Demonstrate how to write as below steps:
      - WP1: Convert a Semantic Versioning Component Number String to a Tuple
      - WP2: Compare Versions
      - WP3: Write a Class `Version`
      - WP4: Compute "Official" String Representations
      - WP5: Compute "Informal" String Representation
      - WP6: Compare `Version` Instances

    - `Waypoint 7`: This code will be set up as something known as a git hook. This script is named "post-commit", it will occur after a commit. When changes are committed to the Git repository, the script automatically increments the patch number of a semantic versioning 3-component number (at least 1) stored in a file VERSION located at the root folder of a Git repository.

- _Note_ : _more details, please refer to initial_istruction.md file_
---
## How to use

### Prerequisites
- Python3 installation is required to get started (check by using python3 --version)

### Usage
- Clone this repo to your local machine using `https://github.com/intek-training-jsc/semantic-versioning-and-git-hooks-hoaithu1.git`
- Create a `post-commit` file to the .git/hooks folder within your own repository where you want to use this script. 

```shell
cd PATH/TO/YOUR/REPO/.git/hooks
touch post-commit
```
- Navigate to the repo from which you want to run this script and make the post-commit file executable. 

```shell
cd PATH/TO/YOUR/REPO/.git/hooks
chmod +x post-commit
```

- Open `post-commit` file and write below code:
```
#!/bin/bash
python3 post_commit.py 
```
- When changes are committed to the Git repository, the script automatically increments the patch number of a semantic versioning 3-component number stored in a file VERSION located at the root folder of a Git repository. Check file VERSION.

## Support

Reach out to me (author)at the following place!

- Email at hoai.le@f4.intek.edu.vn
---
