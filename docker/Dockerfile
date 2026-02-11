FROM frappe/erpnext:develop

USER root
# Install git if needed for pip
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
USER frappe

# Copy the local app directory into the container
COPY --chown=frappe:frappe . /home/frappe/frappe-bench/apps/erpnext_nextcloud_sso

# Install the app (editable mode)
RUN cd /home/frappe/frappe-bench && \
    ./env/bin/pip install -e apps/erpnext_nextcloud_sso && \
    echo "" >> sites/apps.txt && \
    echo "erpnext_nextcloud_sso" >> sites/apps.txt
