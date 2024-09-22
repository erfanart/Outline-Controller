if [ ! -d "/app/data" ]; then
  cp -r /app/data-default/*  /app/data/
fi

if [ ! -d "/app/config" ]; then
  cp -r /app/config-default/* /app/config/
fi

apachectl start &
exec "$@"