FROM lsiobase/alpine.python

WORKDIR /app

COPY  -r ../manager /app/
COPY  -r ../config  /app/
COPY ../config.yaml /app/
COPY ../requirements.txt /app/
COPY ../main.py /app/
COPY entrypoint.sh /app/
RUN mkdir /app/data
RUN cp -r /app/config /app/config-default
RUN cp -r /app/data /app/data-default
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT [ "entrypoint.sh" ]
CMD [ "python","main.py" ]