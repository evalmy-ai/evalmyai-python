if ! grep -q "# DEVCONTAINER EVALMYAI-CLIENT INIT" ~/.bashrc; then
    echo "Initializing..."
    echo "# DEVCONTAINER EVALMYAI-CLIENT INIT #" >> ~/.bashrc;
    echo "export USER_NAME=$(id -un)" >> ~/.bashrc;
    echo "export USER_ID=$(id -u)" >> ~/.bashrc;
    echo "export USER_GID=$(id -g)" >> ~/.bashrc;
    echo "export USER_GNAME=$(id -gn)" >> ~/.bashrc;

    GROUP_NAME=$(stat -c %G /data/evalmyai-client)
    GROUP_ID=$(getent group "$GROUP_NAME" | awk -F: '{print $3}')
    echo "export LLM_EVALUATOR_GID=$GROUP_ID" >> ~/.bashrc
    echo "export LLM_EVALUATOR_GNAME=\"$GROUP_NAME\"" >> ~/.bashrc

    echo "export DOCKER_GID=$(getent group docker | cut -d: -f3)" >> ~/.bashrc;
fi

mkdir -p ~/.aws && chmod 700 ~/.aws
touch ~/.aws/credentials

echo "Initialization complete..."
