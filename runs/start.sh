#! /bin/bash

# Start the server
echo "Starting the server..."
cd ../
source .venv/bin/activate

echo "Server started on http://localhost:8000"
uvicorn src.start.main:app --reload

# End of file