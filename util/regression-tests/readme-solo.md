How to run:

In terminal 1:

MAKE sure to set the correct time zone below, or tests will fail!


```
python -m SimpleHTTPServer 8080 &
CRS_HOME=/home/yuval/sources/owasp-modsecurity-crs
reset; docker run --name envoy-crs -d -v /tmp/envoy:/tmp/envoy -v $CRS_HOME:/owasp-modsecurity-crs:ro -w /owasp-modsecurity-crs/rules --net host quay.io/solo-io/envoy-gloo-ee:0.1.26 -c /owasp-modsecurity-crs/util/regression-tests/envoy.yaml -l debug --disable-hot-restart --concurrency 1 --log-path /tmp/envoy/envoy.log --file-flush-interval-msec 1

# to see what's going on:
tail -f /tmp/envoy/envoy.log
```

In terminal 2:
```
CRS_HOME=/home/yuval/sources/owasp-modsecurity-crs
cd $CRS_HOME/util/regression-tests
py.test -v CRS_Tests.py --config envoy --ruledir_recurse=tests/
```

to run a specific test:
In terminal 2:
```
CRS_HOME=/home/yuval/sources/owasp-modsecurity-crs
cd $CRS_HOME/util/regression-tests
py.test -v CRS_Tests.py --config envoy --rule tests/REQUEST-920-PROTOCOL-ENFORCEMENT/920440.yaml
```

to clean up:

```
docker rm -f envoy-crs
```