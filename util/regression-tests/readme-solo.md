how to run:
```
python -m SimpleHTTPServer 8080 &
cd /home/yuval/sources/owasp-modsecurity-crs/rules
reset; sudo /home/yuval/Projects/solo/envoy-gloo-ee/bazel-bin/envoy  -c ~/Projects/solo/envoy-examples/waf-listener.yaml -l debug --concurrency 1 2>&1 |tee /tmp/log.log
```

terminal2:
```
cd /home/yuval/sources/owasp-modsecurity-crs/util/regression-tests
py.test -v CRS_Tests.py --ruledir_recurse=tests/
```