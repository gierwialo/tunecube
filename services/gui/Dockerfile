FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
      chromium \
      xterm \
      chromium-l10n \
      fonts-liberation \
      fonts-roboto \
      hicolor-icon-theme \
      libcanberra-gtk-module \
      libexif-dev \
      libgl1-mesa-dri \
      libgl1-mesa-glx \
      libpangox-1.0-0 \
      libv4l-0 \
      libsdl2-dev \
      pulseaudio \
      fonts-symbola \
      --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /etc/chromium.d/ \
    && /bin/echo -e 'export GOOGLE_API_KEY="AIzaSyCkfPOPZXDKNn8hhgu3JrA62wIgC93d44k"\nexport GOOGLE_DEFAULT_CLIENT_ID="811574891467.apps.googleusercontent.com"\nexport GOOGLE_DEFAULT_CLIENT_SECRET="kdloedMFGdGla2P1zacGjAQh"' > /etc/chromium.d/googleapikeys
RUN adduser root pulse-access
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN groupadd -r chromium && useradd -r -g chromium -u 1004 -G audio,video,sudo,pulse-access chromium \
    && mkdir -p /home/chromium/Downloads && chown -R chromium:chromium /home/chromium

USER chromium

COPY --chown=chromium:chromium services/gui/start.sh /home/chromium/start.sh

ENTRYPOINT ["/bin/bash"]
CMD ["/home/chromium/start.sh" ]
