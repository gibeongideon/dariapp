#!/usr/bin/env bash
celery -A dariapp beat -l DEBUG
#celery -A dariapp beat -l INFO

#celery -A dariapp beat -l INFO