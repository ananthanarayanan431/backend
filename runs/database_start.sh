#! /bin/bash

# Start the server
echo "Starting the database server..."
cd ../
source .venv/bin/activate

echo "Server started on http://localhost:8000"
uvicorn src.database_start.main:app --reload

# End of file