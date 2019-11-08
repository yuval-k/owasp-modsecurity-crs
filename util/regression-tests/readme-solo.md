how to run:
```
CRS_HOME=/home/yuval/sources/owasp-modsecurity-crs
python -m SimpleHTTPServer 8080 &
reset; docker run -v $CRS_HOME:/owasp-modsecurity-crs:ro -w /owasp-modsecurity-crs/rules --net host quay.io/solo-io/envoy-gloo-ee:0.1.26 -c /owasp-modsecurity-crs/util/regression-tests/envoy.yaml -l debug --concurrency 1 2>&1 | tee /tmp/log.log
```

terminal2:
```
cd $CRS_HOME/util/regression-tests
py.test -v CRS_Tests.py --ruledir_recurse=tests/ --config envoy
```