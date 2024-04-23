FROM python:3.11.8

ARG USER_ID
ARG USER_NAME
ARG USER_GID
ARG USER_GNAME
ARG LLM_EVALUATOR_GID
ARG LLM_EVALUATOR_GNAME
ARG DOCKER_GID

ARG QUARTO_VERSION=1.4.549

# Install docker
RUN groupadd -g ${DOCKER_GID} docker
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

RUN echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list

RUN apt-get update && apt-get install -y docker-ce-cli


# Install necessary packages
RUN apt-get update && apt-get install -y \
    sudo git-lfs && \
    git lfs install && \
    rm -rf /var/lib/apt/lists/*

# Download and install Quarto
RUN mkdir -p /opt/quarto/${QUARTO_VERSION}
RUN curl -o quarto.tar.gz -L \
    "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.tar.gz"
RUN tar -zxvf quarto.tar.gz \
    -C "/opt/quarto/${QUARTO_VERSION}" \
    --strip-components=1
RUN rm quarto.tar.gz
RUN ln -s /opt/quarto/${QUARTO_VERSION}/bin/quarto /usr/local/bin/quarto

# Create user and group
RUN groupadd -g ${USER_GID} ${USER_GNAME}
RUN useradd ${USER_NAME} -u ${USER_ID} -g ${USER_GNAME} -m -s /bin/bash
# Add permission to sudo
RUN echo "${USER_NAME} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
# Create group
RUN groupadd -g ${LLM_EVALUATOR_GID} ${LLM_EVALUATOR_GNAME}
RUN usermod -aG ${LLM_EVALUATOR_GNAME} ${USER_NAME}
# Add user to docker group
RUN usermod -aG docker ${USER_NAME}

# INSTALL THE REST AS A USER
USER ${USER_NAME}

# set USERNAME for metaflow
ENV USERNAME ${USER_NAME}


# Global dev settings
RUN git config --global pull.rebase false
RUN git config --global core.editor "code --wait"