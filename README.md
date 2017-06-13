# pykick

## Quick start on Docker

### Run with example config and templates on http://localhost:8000/.
```
docker run --rm -p 8000:8000 amane/pykick
```

### Run with your own config or/and templates.
Firstly, copy [pykick/pykick/example](https://github.com/amane-katagiri/pykick/tree/master/pykick/example) to `/path/to/your/app`.

Replace all of config, template, static files with yours.
```
docker run --rm -p 8000:8000 -v /path/to/your/app:/app:ro amane/pykick
```

Or mount `config`, `templates` or `static` directory individually.
```
docker run --rm -p 8000:8000 -v /path/to/your/app/config:/app/config:ro \
    -v /path/to/your/app/templates:/app/templates:ro \
    -v /path/to/your/app/static:/app/static:ro amane/pykick
```

## Save count permanently

Use Redis binding to save count.

```
docker run --name pykick-redis -d redis
docker run -p 8000:8000 --link pykick-redis:redis -d amane/pykick --redis_address=redis:6379
```

## Options

Use `-h` to see all options.

```
docker run --rm amane/pykick --help
```
