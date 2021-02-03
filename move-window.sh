xdotool search nparse | xargs -L 1 -I % sh -c 'echo -n "% "; xdotool getwindowname %' | grep Maps | awk '{print $1}' | xargs -I % ^Cotool windowmove % 500 500
