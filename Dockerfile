FROM python:2

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends \
        libgtk-3-dev \
        libcanberra-gtk3-module \
        libgl1-mesa-dev \
        libglu1-mesa-dev \
        libnotify-dev \
    \
    && pip install -U --no-cache-dir \
        -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/debian-8 \
        -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "./clusteris/clusteris.py"]
