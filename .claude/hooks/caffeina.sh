#!/bin/sh
# Tiene sveglio il Mac mentre lavorano gli agenti: a ogni Agent/Workflow riparte un caffeinate di 2 ore.
pidfile="${TMPDIR:-/tmp}/reel-anim-caffeinate.pid"
[ -f "$pidfile" ] && kill "$(cat "$pidfile")" 2>/dev/null
nohup caffeinate -ims -t 7200 >/dev/null 2>&1 &
echo $! > "$pidfile"
