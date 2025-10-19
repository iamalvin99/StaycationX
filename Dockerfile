FROM python:3.12

ENV TZ="Asia/Singapore"
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /
RUN mkdir -p staycation/app
COPY app /staycation/app
RUN mkdir -p staycation/tests
COPY tests /staycation/app/tests
COPY requirements.txt /staycation

WORKDIR /staycation
RUN pip3 install -r requirements.txt --no-cache-dir
RUN pip3 install gunicorn --no-cache-dir && \
    pip3 install Werkzeug==2.2.2 --no-cache-dir

COPY geckodriver /opt/geckodriver

RUN apt update && \
    apt install sudo -y && \
    install -d -m 0755 /etc/apt/keyrings && \
    wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null && \
    echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null && \
    printf "Package: *\nPin: origin packages.mozilla.org\nPin-Priority: 1000\n" > /etc/apt/preferences.d/mozilla && \
    apt update && \
    apt install firefox -y && \
    chmod a+x /opt/geckodriver

WORKDIR /staycation
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "5", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info", "app:create_app()"]