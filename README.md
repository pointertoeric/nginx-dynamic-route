# Http dynamic route based on nginx
Sometimes we need to dynamically route API requests to backend servers based on some http headers returned by some other service. e.g. a typical use case is,  in a big organization, there are multiple data centers, all API requests for US1 organzation should be handled by backend servers in data center US1, all API requests for US2 organzations should be handled by backend servers in data center US2. The API request looks like ```http://localhost:8000/data_query?orgId=1``` or ```http://localhost:8000/data_query?orgId=2```, but to know which datacenter the organization resides have to call another service e.g. ```http://localhost:8000/get-dc?orgId=1``` which will set http header as ```"x-route": "us1"```, we assuming org 1 in US1, org 2 in US2, then front API gateway can use this header information to dispatch API request to correct backend.

Of course there are some API gateways you can use, e.g. envoy, zuul, etc. But you have to write code to support it, but as mentioned in this article you can actually use Nginx module and only nginx configurations to achieve this purpose without any code change.

# How it works
In nginx code base, there is a module called ngx_http_auth_request_module, original purpose is implements client authorization based on the result of a subrequest. If the subrequest returns a 2xx response code, the access is allowed. If it returns 401 or 403, the access is denied with the corresponding error code. Any other response code returned by the subrequest is considered an error, also as I side effect it can also set some variable during processing. So if we use this module, replace the authorization with our own service which will set the route header then we are done, sounds pretty simple and cool?

1. this module is not enabled by default, you have to enable it by recompile nginx.
```--with-http_auth_request_module```
2. route API request to organizaion service first
```
location ~ ^/data_query {
			    auth_request /get_dc;
          # set $dynamic to route header value
			    auth_request_set $dynamic $upstream_http_x_route;
          # then dispatch API call to backend
          # Note $upstream will evaluate from a map config whcch map $dynamic to $upstream, see below
          # so if route header is us1, it will map to upstream us1
			    proxy_pass http://$upstream;
		  }
      
	map $dynamic $upstream {
		  us1		us1;
		  us2		us2;
	}

	upstream us1 {
		  server backend_us1_service:8080;
	}

	upstream us2 {
		  server backend_us2_service:8080;
	}

  upstream get_dc {
		  server org_service:8080;
	}
```
# Try it:
In the repo, I provide the POC code and config, you can try it by yourself.
```
docker-compose -f docker-compose.yaml build
docker-compose -f docker-compose.yaml up
curl http://localhost:8000/data_query?orgId=1
curl http://localhost:8000/data_query?orgId=2
```

# Conclusion:
Wow, we just use nginx module and configuration change to support dynamic route, also you may consider to use nginx cache module to cache the upstream response, still without code change!!!

