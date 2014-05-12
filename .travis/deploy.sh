#!/bin/bash

if [ $TRAVIS_PULL_REQUEST != "false" ]; then
	export BUILD_ID="$TRAVIS_BUILD_NUMBER-pr-$TRAVIS_PULL_REQUEST"
elif [ $TRAVIS_BRANCH == "master" ]; then
	export BUILD_ID=$TRAVIS_BUILD_NUMBER
else
    echo "Skipping deploy of non-master branch..."
    exit 0
fi

mv build "apidocs-$BUILD_ID"
tar -cjvf "apidocs-$BUILD_ID.tar.bz2" "apidocs-$BUILD_ID"

cat > "s3cfg" << EOF
[default]
access_key=$AWS_ACCESS_KEY
secret_key=$AWS_SECRET_KEY
EOF

s3cmd -c s3cfg put "apidocs-$BUILD_ID.tar.bz2" s3://io.orchestrate.deploy/
