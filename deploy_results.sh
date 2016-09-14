#!/bin/sh

echo $GITHUB_API_KEY
echo $TRAVIS_BRANCH
if [ -n "$GITHUB_API_KEY" ]; then 
  if [ -n "$TRAVIS_BRANCH" ]; then
      mkdir -p benchmark_results
      git clone https://github.com/jayhorn/jayhorn.git  --branch gh-pages --single-branch benchmark_results
      cd benchmark_results

      mkdir -p ./$TRAVIS_BRANCH
      cp -r ../view_results/* ./$TRAVIS_BRANCH/
      echo "$PWD"
      git add ./$TRAVIS_BRANCH
      git -c user.name='lememta' -c user.email='lememta@gmail.com' commit -am "UPDATING Results from Benchmarks" --no-verify
      git push -f -q https://lememta:$GITHUB_API_KEY@github.com/jayhorn/jayhorn gh-pages 
      cd .. 
      echo "DONE updating results"   
      echo "$PWD"
  fi
fi




