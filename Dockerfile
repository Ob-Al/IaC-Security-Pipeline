FROM python:3.12-slim

ARG TERRAFORM_VERSION=1.9.8
ARG TFSEC_VERSION=v1.28.13
ARG CHECKOV_VERSION=3.3.30

RUN apt-get update && apt-get install -y --no-install-recommends curl unzip git \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSLo /tmp/tf.zip "https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" \
    && unzip /tmp/tf.zip -d /usr/local/bin && rm /tmp/tf.zip \
    && curl -sSLo /usr/local/bin/tfsec "https://github.com/aquasecurity/tfsec/releases/download/${TFSEC_VERSION}/tfsec-linux-amd64" \
    && chmod +x /usr/local/bin/tfsec \
    && pip install --no-cache-dir "checkov==${CHECKOV_VERSION}"

WORKDIR /repo
ENTRYPOINT ["./scripts/scan.sh"]
CMD ["terraform"]
