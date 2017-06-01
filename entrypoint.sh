#!/bin/sh
set -e

case ${1} in
    app:create_db)
        echo 'Creating database'
        python db_create.py
        ;;
    app:upgrade_db)
        echo 'Apply database migrations'
        python db_upgrade.py
        ;;
    app:downgrade_db)
        echo 'Rollback database migrations'
        python db_downgrade.py
        ;;
    app:start)
        echo 'Apply database migrations'
        python db_upgrade.py
        echo 'Starting server'
        gunicorn -b 0.0.0.0:8000 --access-logfile=/dev/stdout app:app
        ;;
    app:shell)
        echo 'Entering shell'
        sh
esac
