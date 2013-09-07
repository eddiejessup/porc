#!/bin/bash

if [ $TRAVIS_BRANCH != "master" ]; then
    echo "Skipping deploy of non-master branch..."
    exit 0
fi

cat > "s3cfg" << EOF
[default]
access_key=$AWS_ACCESS_KEY
secret_key=$AWS_SECRET_KEY
EOF

s3cmd -c s3cfg put apidocs-$TRAVIS_BUILD_NUMBER.tar.bz2 s3://io.orchestrate.deploy/
