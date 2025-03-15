import os
import sys
from tqdm import tqdm
import time
from datetime import datetime

# Accept directory paths as Command Line Arguments
target_directory = sys.argv[1]
source_directory = sys.argv[2]

start_time = time.time()
file_count = 0

# Initialize log file
time_at_start = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
log_filename = f"logs\\CFN\\CFN_{time_at_start}.log"
if not os.path.exists("logs\\CFN\\"):
    os.makedirs("logs\\CFN\\")

with open(log_filename, 'w') as log_file:
    log_file.write(f"Log for Copy File Names - {time_at_start}\n")
    log_file.write(f"Target folder: {target_directory}\n")
    log_file.write(f"Source folder: {source_directory}\n\n")


def copy_file_names(target_dir, source_dir):
    global log_file, file_count
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    for filename in tqdm(os.listdir(source_dir), desc="Copying Names",
                         colour="blue"):
        source_file = os.path.join(source_dir, filename)

        # Ensure not a folder and is a file
        if os.path.isfile(source_file):
            # Create file at target directory with source file name
            target_file = os.path.join(target_dir, filename)
            open(target_file, 'w').close()
            file_count += 1
            with open(log_filename, 'a') as log_file:
                log_file.write(f"Copied file name: {filename} to target\n")


copy_file_names(target_directory, source_directory)

end_time = time.time()

# Summary to console
print(f"{file_count} file(s)' name copied")
print(f"Time to run: {end_time - start_time:.3f}")

# Summary to log file
with open(log_filename, 'a') as log_file:
    log_file.write(f"\nTotal file's names copied: {file_count}\n")
    log_file.write(f"Time to run: {end_time - start_time:.3f} seconds")
