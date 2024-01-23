#!/bin/sh
set -x

RIC_OCTET=5
XAPP_IP_BASE="10.0.$RIC_OCTET"
XAPP_NEW_NAME="xapp-ric$RIC_OCTET"
XAPP_NEW_IMAGE_NAME="ef-ric$RIC_OCTET"
EF_XAPP_DIR="$(dirname "$PWD")"
WORKSPACE_DIR="$(dirname "$EF_XAPP_DIR")"
XAPP_NEW_DIR=${WORKSPACE_DIR}/${XAPP_NEW_NAME}
XAPP_NEW_SETUP_DIR=${XAPP_NEW_DIR}/setup
XAPP_NEW_SM_CONNECTOR_DIR=${XAPP_NEW_SETUP_DIR}/xapp-sm-connector


# Check if xapp exist - if yes, we do nothing
if [ -d "$XAPP_NEW_DIR" ]; then
    echo "Directory exists."
    cd $WORKSPACE_DIR
    rm -rf $XAPP_NEW_NAME
    exit
else
    echo "Directory do not exist."
    echo "Coping directory to $XAPP_NEW_DIR"
    cd $WORKSPACE_DIR
    # create new dir
    mkdir $XAPP_NEW_NAME
    cp -r ${EF_XAPP_DIR}/.vscode ${XAPP_NEW_DIR}
    # change the remote path directory to the new directory
    sed -i "s#${EF_XAPP_DIR}#${XAPP_NEW_DIR}#g" ${XAPP_NEW_DIR}/.vscode/sftp.json
    # copy xapp-sm-connector
    cd $XAPP_NEW_DIR
    mkdir setup
    # cd setup
    cp -r ${EF_XAPP_DIR}/setup/xapp-sm-connector ${XAPP_NEW_SETUP_DIR}
    cp -r ${EF_XAPP_DIR}/setup/xapp ${XAPP_NEW_SETUP_DIR}

    # copy setup-scripts
    mkdir setup-scripts
    cd ${EF_XAPP_DIR}/setup-scripts
    cp $(ls  --ignore=create-new-xapp.sh) ${XAPP_NEW_DIR}/setup-scripts

    cd ${XAPP_NEW_DIR}/setup-scripts
    # change the name
    sed -i "s#IMAGE_NAME=xapp#IMAGE_NAME=${XAPP_NEW_IMAGE_NAME}#g" ${XAPP_NEW_DIR}/setup-scripts/setup-xapp.sh
    sed -i "s#ric #ric${RIC_OCTET} #g" ${XAPP_NEW_DIR}/setup-scripts/setup-xapp.sh
    sed -i "s#10.0.2#${XAPP_IP_BASE}#g" ${XAPP_NEW_DIR}/setup-scripts/setup-lib.sh
    sed -i "s#36422#$(($(($RIC_OCTET-2))*10000+36422))#g" ${XAPP_NEW_DIR}/setup-scripts/setup-lib.sh
    sed -i "s#xapp-#${XAPP_NEW_IMAGE_NAME}-#g" ${XAPP_NEW_DIR}/setup-scripts/start-xapp-ns-o-ran.sh
    # change init files
    sed -i "s#10.0.2#${XAPP_IP_BASE}#g" ${XAPP_NEW_DIR}/setup/xapp-sm-connector/init/routes.txt
    sed -i "s#10.0.2#${XAPP_IP_BASE}#g" ${XAPP_NEW_DIR}/setup/xapp-sm-connector/src/xapp_env.sh
    # CHANGE ip in the Dockerfile
    sed -i "s#10.0.2#${XAPP_IP_BASE}#g" ${XAPP_NEW_DIR}/setup/xapp/Dockerfile
fi

echo "Moving to the new created directory"

cd ${XAPP_NEW_DIR}
git init  -b main
# git config --global init.defaultBranch "main"
git config --local user.name "fgjeci" 
git config --local user.email "franci.gjeci@gmail.com"
cp ${EF_XAPP_DIR}/.git/info/exclude ${XAPP_NEW_DIR}/.git/info/exclude
git add .
git commit -m "Xapp creation"

# create github account
# GitHub CLI api
# https://cli.github.com/manual/gh_api

gh repo create ${XAPP_NEW_IMAGE_NAME} --private --source=. --remote=origin --push
git push --set-upstream origin main


# gh repo delete fgjeci/${XAPP_NEW_IMAGE_NAME}



