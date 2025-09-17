set quiet

# Run the p2p simulation
[no-exit-message]
run *peer_number:
  just generate_configs {{peer_number}}
  just download_dataset
  just remove_venv
  just clean
  docker compose -f docker/docker-compose.generated.yml build
  docker compose -f docker/docker-compose.generated.yml up
  just test_models {{peer_number}}

# Generate config files
[no-exit-message]
generate_configs *peer_number:
  uv --project src run src/util/generate_configs.py {{peer_number}}

# Download the imdb dataset
[no-exit-message]
download_dataset:
  uv --project src run src/util/download_dataset.py -q

# Remove local .venv file
[no-exit-message]
remove_venv:
  ./src/util/remove_venv.sh

# Clean docker images
[no-exit-message]
clean:
  docker compose -f docker/docker-compose.generated.yml down
  docker image prune -af

# Test peer models against local model
[no-exit-message]
test_models *peer_number:
  uv --project src run src/util/test_models.py {{peer_number}}

# Add python module to project dependencies
[no-exit-message]
add *modules:
  uv --project src add {{modules}}

# Remove python module from project dependencies
[no-exit-message]
remove *modules:
  uv --project src remove {{modules}}

# Build the final report
[no-exit-message]
build-doc:
  ./doc/bin/build_report.sh

# Build and open the final report
[no-exit-message]
doc:
  ./doc/bin/build_report.sh
  open ./doc/build/finalReport.pdf &

# Run debug testing facility
[no-exit-message]
test:
  uv --project src run src/main/test.py

# List available recipies
default:
  just --list --unsorted --list-heading $'Available commands:\n'

