FROM python:3.11.2-slim-buster
# prevent __pycache__ folder and files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN set -ex \
  && apt-get update \
  && apt-get install -qq -y --no-install-recommends \
  make \
  curl openssh-server bash \
  gcc \
  git \
  jq \
  gettext \
  procps \
  python3-dev \
  libffi-dev \
  vim \
  postgresql-client \
  libcairo2 libpango-1.0 libpangocairo-1.0 libgdk-pixbuf2.0 fontconfig ttf-dejavu \
  && pip install pipenv \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --dev --verbose
ADD . ./
# Used by heroku to create SSH tunnel to the
# docker container via heroku CLI
ADD heroku-exec.sh /app/.profile.d
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

ADD docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod 775 /app/docker-entrypoint.sh

## if faced any issues with permission in mac or windows comment these lines
RUN adduser --disabled-password --gecos '' admin
RUN adduser admin sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER admin
#----------

ENTRYPOINT ["/app/docker-entrypoint.sh"]