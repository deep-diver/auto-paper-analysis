#!/bin/bash

# Set start and end dates (format YYYY-MM-DD)
start_date=$1
end_date=$2
hf_repo_id=$3

# Convert dates into seconds since epoch (for easier calculations)
start_seconds=$(date -j -f "%Y-%m-%d" "$start_date" "+%s")
end_seconds=$(date -j -f "%Y-%m-%d" "$end_date" "+%s")

# Iterate through dates
current_seconds=$start_seconds
while [[ $current_seconds -le $end_seconds ]]; do
  current_date=$(date -j -r $current_seconds "+%Y-%m-%d")

  # Replace with your actual program execution
  echo "Running program for date: $current_date"
  python app.py --target-date $current_date \
    --gemini-api $GEMINI_API_KEY \
    --hf-token $HF_ACCESS_TOKEN \
    --hf-repo-id $hf_repo_id \
    --hf-daily-papers
  
  current_seconds=$((current_seconds + 86400))  # Add 1 day (86400 seconds)
done

