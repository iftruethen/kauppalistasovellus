#!/bin/bash
rm db.db
touch db.db
sqlite3 db.db < schema.sql