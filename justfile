set quiet

# List available recipies
default:
  just --list --list-heading $'Available commands:\n'

# Build the final report
[no-exit-message]
build-doc:
    ./doc/bin/build_report.sh

# Build and open the final report
[no-exit-message]
doc:
    ./doc/bin/build_report.sh
    open ./doc/build/finalReport.pdf &

# Run the p2p simulation
[no-exit-message]
run: download_dataset remove_venv clean
    docker compose -f docker/docker-compose.yml build
    docker compose -f docker/docker-compose.yml up

# Clean docker images
[no-exit-message]
clean:
    docker compose -f docker/docker-compose.yml down
    docker image prune -af

# Add python module to project dependencies
[no-exit-message]
add *modules:
    uv --project src add {{modules}}

# Remove python module from project dependencies
[no-exit-message]
remove *modules:
    uv --project src remove {{modules}}

# Run debug testing facility
[no-exit-message]
test:
    uv --project src run src/main/test.py

# Download the imdb dataset
[no-exit-message]
download_dataset:
    uv --project src run src/util/download_dataset.py -q

# Remove local .venv file
[no-exit-message]
remove_venv:
    ./src/util/remove_venv.sh
