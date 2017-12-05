#!/bin/bash

###################
# Author: Domenic Denicola
# Modifications by: Prasad Talasila
# Date: 19-March-2017
###################


set -e # Exit with nonzero exit code if anything fails

SOURCE_BRANCH="dev"
TARGET_BRANCH="gh-pages"
ENCRYPTION_LABEL="fafbdc041e4b"
COMMIT_AUTHOR_EMAIL="tsrkp@goa.bits-pilani.ac.in"

function createDocs {
  cd docs &&  make html
  cd .. &&  cp -r docs/build/html/* out/ 
}

# Pull requests and commits to other branches shouldn't try to deploy, just build to verify
if [ "$TRAVIS_PULL_REQUEST" != "false" -o "$TRAVIS_BRANCH" != "$SOURCE_BRANCH" ]; then
    echo "Skipping deploy; just doing a build."
    exit 0
fi

# Save some useful information
REPO=`git config remote.origin.url`
SSH_REPO=${REPO/https:\/\/github.com\//git@github.com:}
SHA=`git rev-parse --verify HEAD`

# Clone the existing gh-pages for this repo into out/
# Create a new empty branch if gh-pages doesn't exist yet (should only happen on first deply)
git clone $REPO out
cd out
git checkout $TARGET_BRANCH || git checkout --orphan $TARGET_BRANCH
cd ..

# Clean out existing contents
rm -rf out/**/* || exit 0

# create the sphinx documents
createDocs

# Now let's go have some fun with the cloned repo
cd out
git config user.name "Travis CI"
git config user.email "$COMMIT_AUTHOR_EMAIL"

# Commit the "changes", i.e. the new version.
# The delta will show diffs between new and old versions.
git add .
git commit -m "[Travis Commit] Automated Deploy to gh-pages | Caused by ${SHA}
refer auto_commit_script: https://github.com/prasadtalasila/IRCLogParser/blob/$SOURCE_BRANCH/script/doc_auto_deploy.sh
" || exit 0	#if there is nothing to commit, exit now

#go to parent directory and perform SSH configuration
cd ..
# Get the deploy key by using Travis's stored variables to decrypt deploy_key.enc
ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
ENCRYPTED_KEY=${!ENCRYPTED_KEY_VAR}
ENCRYPTED_IV=${!ENCRYPTED_IV_VAR}
openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in config/deploy_key.enc -out config/deploy_key -d
chmod 600 config/deploy_key
eval `ssh-agent -s`
ssh-add config/deploy_key

#go to out/ directory and commit the gh-pages/ update
cd out/
#check the git repo context
pwd
echo repo=$SSH_REPO
echo branch=$TARGET_BRANCH
echo "===show local gh-pages commit logs==="
git log --oneline -n 5
echo "===show remote gh-pages commit logs==="
git log --oneline -n 5 origin/$TARGET_BRANCH
echo "===show remote commits above the current local commit==="
git log HEAD..origin/$TARGET_BRANCH
echo "===show status of local branch==="
git status

# Now that we're all set up, we can push.
git push $SSH_REPO $TARGET_BRANCH


##References
#https://gist.github.com/domenic/ec8b0fc8ab45f39403dd
#https://github.com/travis-ci/travis.rb
