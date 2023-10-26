FROM python:3.8

LABEL maintainer="Gina Oba"

USER root

WORKDIR /opt/app
COPY requirements.txt ./

# Consolidate RUN commands to reduce image layers and improve build speed
RUN python -m pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt


# Copy your Dash application files
COPY *.py .
COPY Clover ./Clover
COPY assets ./assets
COPY resources ./resources

EXPOSE 8050

# Run the Dash app on container startup
CMD ["python", "index.py", "--port", "8050"]