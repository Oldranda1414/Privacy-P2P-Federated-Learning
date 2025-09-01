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

