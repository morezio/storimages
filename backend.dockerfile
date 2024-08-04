FROM morezio/envs:u_dev

# create non-root user for deployment
RUN groupadd -r nonrootuser && useradd -r -g nonrootuser nonrootuser

# adds the inter-container shared path
RUN mkdir -p /storimages/data
WORKDIR /storimages
ADD backend/ backend/
RUN pip install -r backend/be_requirements.txt

# Switch to non-root for running the app
RUN chown -R nonrootuser:nonrootuser /storimages
USER nonrootuser


WORKDIR /storimages/backend
# I break down because it is easier to read and debug
# Also, used cmd because I find it tedious to split these --arg s if
# I was using entrypoint x cmd
# Not adding variables below to reduce the mental overhead for now
CMD gunicorn \
--workers=1 \
--log-level=info \
--proxy-allow-from '*' \
--forwarded-allow-ips '*' \
--log-file=- \
--access-logfile=- \
--error-logfile=- \
--bind=0.0.0.0:80 app:app