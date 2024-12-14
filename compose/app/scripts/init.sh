#!/bin/bash
./compose/app/scripts/run_migrations.sh &&
./compose/app/scripts/create_superuser.sh &&
./compose/app/scripts/run_server.sh