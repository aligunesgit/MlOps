# Reference material for Week 3 — Module 3: Git Essentials for MLOps Practitioners

> Source: [dtu_mlops](https://github.com/SkafteNicki/dtu_mlops), `s2_organisation_and_version_control/git.md`
> (DTU course 02476, Apache 2.0 licensed). Copied in full as raw source material for building this
> week's lesson content — rewrite/adapt before publishing to students, and note that DTU-specific
> references (their own repo URL, their course project setup, image paths under `../figures/`) will
> need to be swapped for this course's own repo/project once we build the real module page.

---

# Git

!!! info "Core Module"

Proper collaboration with other people will require that you can work on the same codebase in an organized manner.
This is the reason that **version control** exists. Simply stated, it is a way to keep track of:

* Who made changes to the code
* When did the change happen
* What changes were made

For a full explanation, please see this [page](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F).

Secondly, it is important to note that GitHub is not git! GitHub is the dominating player when it comes to
hosting repositories, but that does not mean that they are the only ones providing free repository hosting
(see [bitbucket](https://bitbucket.org/product/) or [gitlab](https://about.gitlab.com/) for some other examples).

That said, we will be using git and GitHub throughout this course. It is a requirement for passing this course that
you create a public repository with your code and use git to upload any code changes. How much you choose to integrate
this into your own projects depends, but you are at least expected to be familiar with git+GitHub.

<figure markdown>
![Image](../figures/git.png){ width="400" }
<figcaption> <a href="https://xkcd.com/1597/"> Image credit </a> </figcaption>
</figure>

## Initial config

!!! quote "What does Git stand for?"

    The name "git" was given by Linus Torvalds when he wrote the very first version. He described the tool as
    "the stupid content tracker" and the name as (depending on your mood):

    * Random three-letter combination that is pronounceable, and not actually used by any common UNIX command. The fact
        that it is a mispronunciation of "get" may or may not be relevant.
    * Stupid. Contemptible and Despicable. Simple. Take your pick from the dictionary of slang.
    * "Global information tracker": you're in a good mood, and it actually works for you.
        Angels sing, and a light suddenly fills the room.
    * "Goddamn idiotic truckload of sh*t": when it breaks

1. [Install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) on your computer and make sure
    that your installation is working by writing `git help` in a terminal and it should show you the help message for
    git.

2. Create a [GitHub](https://github.com/) account if you do not already have one.

3. To make sure that we do not have to type in our GitHub username every time that we want to make some changes,
    we can once and for all set it on our local machine.

    ```bash
    # type in a terminal
    git config credential.helper store
    git config --global user.email <email>
    ```

## Git overview

The most simple way to think of version control is that it is just nodes with lines connecting them.

Each node, which we call a *commit*, is uniquely identified by a hash string. Each node stores what our code
looked like at that point in time (when we made the commit) and using the hash codes we can easily
revert to a specific point in time.

The commits are made up of local changes that we make to our code. A basic workflow for
adding commits can be seen below:

Assuming that we have made some changes to our local *working directory* and that we
want to get these updates to be online in the *remote repository* we have to do the following steps:

* First we run the command `git add`. This will move our changes to the *staging area*. While changes are in the
    staging area we can very easily revert them (using `git restore`). There has therefore not been assigned a unique
    hash to the code yet, and so we can still overwrite it.

* To take our code from the *staging area* and make it into a commit, we simply run `git commit` which will locally
    add a node to the graph. Note again that we have not pushed the commit to the online *repository* yet.

* Finally, we want others to be able to use the changes that we made. We do a simple `git push` and our
    commit goes online.

Of course, the real power of version control is the ability to make branches.

Each branch can contain code that is not present on other branches. This is useful when you are many developers
working together on the same project.

### Exercises

1. In your GitHub account create a repository, where the intention is that you upload the code from a previous
    exercise.

    1. After creating the repository, clone it to your computer.

        ```bash
        git clone https://github.com/my_user_name/my_repository_name.git
        ```

    2. Move/copy the relevant files into the repository (and any others that you made).

    3. Add the files to a commit by using the `git add` command.

    4. Commit the files using the `git commit` command where you use the `-m` argument to provide a commit message.
        Writing a good commit message is a skill in and of itself. A commit message should be short but informative
        about the work you are trying to commit.

    5. Finally push the files to your repository using `git push`. Make sure to check online that the files have been
        updated in your repository. Be aware that you either need to generate a token to remote push from your local
        [terminal](https://github.com/settings/tokens) or install the
        [GitHub CLI](https://docs.github.com/en/github-cli/github-cli/quickstart).

    6. You can always use the command `git status` to check where you are in the process of making a commit.

    7. Also checkout the `git log` command, which will show you the history of commits that you have made.

2. Make sure that you understand how to make branches, as this will allow you to try out code changes without
    messing with your working code. Creating a new branch can be done using:

    ```bash
    # create a new branch
    git checkout -b <my_branch_name>
    ```

    Afterwards, you can use `git checkout` to change between branches (remember to commit your work!).
    Try adding something (a file, a new line of code, etc.) to the newly created branch, commit it and
    try changing back to main afterwards. You should hopefully see whatever you added on the branch
    is not present on the main branch. The `git checkout` command is used for a lot of different things in git. It can
    be used to change branches, to revert changes and to create new branches. An alternative is using `git switch` and
    `git restore` which are more modern commands.

3. Make sure to make a `git pull` on your local copy regularly whenever the course/team repository is updated.

4. Git may seem like a waste of time when solutions like Dropbox, Google Drive, etc. exist, and it is
    not completely untrue when you are only one or two working on a project. However, these file management
    systems fall short when hundreds to thousands of people work together. For this exercise you will
    go through the steps of sending an open-source contribution:

    1. Go online and find a project you do not own, where you can improve the code. You can either look at this
        [page](https://goodfirstissue.dev/) of good issues to get started with. Now fork the project by
        clicking the *fork* button.

        This will create a local copy of the repository which you have complete writing access to. Note that
        code updates to the original repository do not update code in your local repository.

    2. Clone your local fork of the project using `git clone`.

    3. As default your local repository will be on the `main branch` (HINT: you can check this with the
        `git status` command). It is good practice to make a new branch when working on some changes. Use
        the `git branch` command followed by the `git checkout` command to create a new branch.

    4. You are now ready to make changes to the repository. Try to find something to improve (any spelling mistakes?).
        When you have made the changes, do the standard git cycle: `add -> commit -> push`.

    5. Go online to the original repository and go to the `Pull requests` tab. Find the `compare` button and
        choose the button to compare the `master branch` of the original repo with the branch that you just created
        in your own repository. Check the diff on the page to make sure that it contains the changes you have made.

    6. Write a bit about the changes you have made and click `Create pull request` :).

5. Forking a repository has the consequence that your fork and the repository that you forked can diverge. To
    mitigate this we can set what is called a *remote upstream*. Take a look at this
    [page](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/configuring-a-remote-repository-for-a-fork),
    and set a remote upstream for the repository you just forked.

    ??? success "Solution"

        ```bash
        git remote add upstream <url-to-original-repo>
        ```

6. After setting the upstream branch, we need to pull and merge any updates.

    ??? success "Solution"

        ```bash
        git fetch upstream
        git checkout main
        git merge upstream/main
        ```

7. As a final exercise we want to simulate a *merge conflict*, which happens when two users try to commit changes
    to exactly the same lines of code in the codebase, and git is not able to resolve how the different commits should be
    integrated.

    1. In your browser, open your favorite repository (it could be the one you just worked on), go to any file of
        your choosing and click the edit button and make some change to the file. For example, if
        you choose a Python file you can just import some random packages at the top of the file. Commit the change.

    2. Make sure not to pull the change you just made to your local computer. Locally make changes to the same
        file in the same lines and commit them afterwards.

    3. Now try to `git pull` the online changes. What should (hopefully) happen is that git will tell you that it found
        a merge conflict that needs to be resolved. Open the file and you should see something like this:

        ```txt
        <<<<<<< HEAD
        this is some content to mess with
        content to append
        =======
        totally different content to merge later
        >>>>>>> master
        ```

        this should be interpreted as: everything that's between `<<<<<<<` and `=======` are the changes made by your
        local commit and everything between `=======` and `>>>>>>>` are the changes you are trying to pull. To fix
        the merge conflict you simply have to make the code in the two "cells" work together. When you are done,
        remove the identifiers `<<<<<<<`, `=======` and `>>>>>>>`.

        !!! note "Merge, rebase or fast-forward?"

            On a `git pull` you can get messages like this the first time you try to pull after a merge conflict:

            ```txt
            hint: You have divergent branches and need to specify how to reconcile them.
            hint: You can do so by running one of the following commands sometime before
            hint: your next pull:
            hint:
            hint:   git config pull.rebase false  # merge
            hint:   git config pull.rebase true   # rebase
            hint:   git config pull.ff only       # fast-forward only
            ```

            In general we recommend setting `git config pull.rebase false` to merge the changes. This is the default
            behavior of git and is the most common way to resolve merge conflicts. However, if you are working on a
            project with many people and you want to keep the commit history clean, you can use
            `git config pull.rebase true` to rebase the changes.

    4. Finally, commit the merge and try to push.

8. (Optional) The above exercises have focused on how to use git from the terminal, which we highly recommend learning.
    However, if you are using a proper editor they also have built-in support for version control. We recommend getting
    familiar with these features (here is a tutorial for
    [VS Code](https://code.visualstudio.com/docs/editor/versioncontrol)).

## Knowledge check

1. How do you know if a certain directory is a git repository?

    ??? success "Solution"

        You can check if there is a ".git" directory. Alternatively you can use the `git status` command.

2. Explain what the file `gitignore` is used for?

    ??? success "Solution"

        The file `gitignore` is used to tell git which files to ignore when doing a `git add .` command. This is
        useful for files that are not part of the codebase, but are needed for the code to run (e.g. data files)
        or files that contain sensitive information (e.g. `.env` files that contain API keys and passwords).

3. You have two branches - *main* and *devel*. What sequence of commands would you need to execute to make sure that
    *devel* is in sync with *main*?

    ??? success "Solution"

        ```bash
        git checkout main
        git pull
        git checkout devel
        git merge main
        ```

4. What best practices are you familiar with regarding version control?

    ??? success "Solution"

        * Use a descriptive commit message
        * Make each commit a logical unit
        * Incorporate others' changes frequently
        * Share your changes frequently
        * Coordinate with your co-workers
        * Don't commit generated files

## Standard Git branching strategies (from Module 3's own topic list)

The course's own module list additionally calls for teaching standard branching strategies used in
industry MLOps/DevOps teams. DTU's material above doesn't cover this in depth (it focuses on the
mechanics of git), so this part needs to be written from scratch for this course:

* **Development branch** — long-lived integration branch, ahead of `main`
* **Feature branches** — one per feature/story, branched from `development`, merged back via PR
* **Bugfix branches** — short-lived, branched from `development` or `main` (hotfix), fixes a specific bug
* **Release branches** — stabilization branch cut from `development` before a release
* **UAT (User Acceptance Testing) branches** — deployed to a staging environment for stakeholder sign-off before
  merging to `main`/production

## AI-Assisted Code Exploration (bonus, from DTU material)

As AI tools like ChatGPT, Claude, and Gemini become increasingly popular for code understanding and development,
having your entire repository in a format that's easy to share with Large Language Models (LLMs) can be very helpful.

[Repomix](https://github.com/yamadashy/repomix) is a powerful tool that packs your entire repository into a single
AI-friendly file with support for multiple output formats and token counting.

```bash
# Quick usage without installation (packs current directory)
npx repomix

# Pack a remote repository directly
npx repomix --remote https://github.com/username/repository
```

For a quick browser-based alternative, [uithub.com](https://uithub.com) lets you view any public GitHub repository
as raw text with token counts.

---

## Still to source for this module (not covered by the DTU git.md page above)

* Standard branching strategy diagrams/exercises (development/feature/bug/release/UAT) — write from scratch, see stub above
* GitHub Actions overview and working — see `week4_cicd_strategies.md` (this course groups GitHub Actions under Module 4, CI/CD)
* GitHub Remote Repository — partially covered above (clone/push/pull/remote); could use a dedicated short section on remotes (`git remote -v`, multiple remotes, SSH vs HTTPS)
* Project: "Mastering Git: Commands, Branching, and Collaboration" — build as this week's hands-on project, combining the git.md exercises above with a small team-branching simulation exercise
