#!/bin/sh

(cd maraudersmap && alembic upgrade head)

uvicorn maraudersmap.main:app --host 0.0.0.0 --port 8080