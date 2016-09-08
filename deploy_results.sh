#!/bin/sh

mkdir -p benchmark_results
ls
git clone https://github.com/jayhorn/jayhorn.git  --branch gh-pages --single-branch benchmark_results
ls
cd benchmark_results
ls
echo $TRAVIS_BRANCH
mkdir -p ./$TRAVIS_BRANCH
cp -r view_results/* ./$TRAVIS_BRANCH/
echo "$PWD"
git add ./$TRAVIS_BRANCH
git -c user.name='lememta' -c user.email='lememta@gmail.com' commit -am "UPDATING Results from Benchmarks" --no-verify
git push -f -q https://lememta:$GITHUB_API_KEY@github.com/jayhorn/jayhorn gh-pages 
cd .. 
echo "DONE updating results"   
echo "$PWD"




