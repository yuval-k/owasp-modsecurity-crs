How to run:

In terminal 1:

```
CRS_HOME=/home/yuval/sources/owasp-modsecurity-crs
python -m SimpleHTTPServer 8080 &
reset; docker run --name envoy-crs -d -v $CRS_HOME:/owasp-modsecurity-crs:ro -w /owasp-modsecurity-crs/rules --net host quay.io/solo-io/envoy-gloo-ee:0.1.26 -c /owasp-modsecurity-crs/util/regression-tests/envoy.yaml -l debug --concurrency 1 

docker logs envoy-crs -f 2>&1 | tee /tmp/log.log
```


In terminal 2:
```
CRS_HOME=/home/yuval/sources/owasp-modsecurity-crs
cd $CRS_HOME/util/regression-tests
py.test -v CRS_Tests.py --ruledir_recurse=tests/ --config envoy
```