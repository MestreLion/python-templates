#!/bin/bash
#
# Allow editing the (usually very outdated) typeshed bundled with PyCharm CE
# https://askubuntu.com/a/1036611/11015
#
# Copyright (C) 2023 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
# License: GPLv3 or later, at your choice. See <http://www.gnu.org/licenses/gpl>
#------------------------------------------------------------------------------

override=/usr/local/share/pycharm/typeshed
snap=/snap/pycharm-community/current/plugins/python-ce/helpers/typeshed

#------------------------------------------------------------------------------
set -Eeuo pipefail  # exit on any error
trap '>&2 echo "error: line $LINENO, status $?: $BASH_COMMAND"' ERR
#------------------------------------------------------------------------------
# Copy the original content
if ! [[ -d "$override" ]]; then
	sudo rsync -av "$snap" "$(dirname "$override")"
fi

# Clone latest typeshed, just as a reference...
if ! [[ -d "$override"-git ]]; then
	sudo git clone https://github.com/python/typeshed.git "$override"-git
fi

# Manually doing it:
#	Start: sudo mount --bind -o nodev,ro "$override" "$snap"/
#	Stop:  sudo umount "$snap"

# NOTE: Since systemd v237 (2018-01), systemd forbids mount points containing symlinks,
# as is the case with /snap/pycharm-community/current. Se we add to /etc/fstab instead
# See https://github.com/systemd/systemd/pull/7940, https://github.com/coreos/bugs/issues/2407

# Create, enable and start a systemd auto-mount unit, so it persists across reboots
# Mount units must be named after mount point
# see https://www.freedesktop.org/software/systemd/man/systemd.mount.html
#name=$(systemd-escape --path "$snap")
#if ! [[ -f /etc/systemd/system/"$name".mount ]]; then
#	sudo tee /etc/systemd/system/"$name".mount <<-EOF
#	[Unit]
#	Description=Override bundled typeshed in pycharm-community snap package
#	After=snapd.service

#	[Mount]
#	What=${override}
#	Where=${snap}
#	Type=none
#	Options=bind,nodev,ro

#	[Install]
#	WantedBy=multi-user.target
#	EOF
#	sudo systemctl enable --now "$name".mount
#fi

# Add the mount point to /etc/fstab
if grep -q "$snap" /etc/fstab; then exit; fi
sudo cp -- /etc/fstab /etc/fstab."$(date +%Y%m%d%H%M%S)".bak
sudo tee -a /etc/fstab <<-EOF

# Override bundled typeshed in pycharm-community snap package
# See https://github.com/MestreLion/python-templates/tree/main/pycharm
# and https://askubuntu.com/a/1036611/11015
${override}  ${snap}  none  bind,nodev,ro,x-systemd.after=snapd.service,x-systemd.wanted-by=multi-user.target  0 0
EOF
