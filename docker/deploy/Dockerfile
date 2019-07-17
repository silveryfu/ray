# The deploy Docker image build a self-contained Ray instance suitable
# for end users.

FROM silveryfu/base-deps

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ADD ray.tar /ray
ADD git-rev /ray/git-rev
RUN /ray/ci/travis/install-bazel.sh
ENV PATH=$PATH:/root/bin
WORKDIR /ray/python
RUN pip install -e .
WORKDIR /ray
