import os
import difflib
import sys
import time
from datetime import datetime
from tqdm import tqdm  # For a progress bar
from concurrent.futures import ThreadPoolExecutor, as_completed

'''
This script is meant to look for files with similar names and change the 
input file to match the file names of the "source" file with a similar name, 
created for the use of large amount of files needing to be renamed to match 
another folder with a very large amount of files.

- Dragphan 2024
'''

# TODO: Make code more encapsulated for integration with a larger script
#  which utilizes multiple file tools such as this one

# TODO: Add emergency break

# Define the file inputs
rename_path = sys.argv[1]
source_path = sys.argv[2]

start_time = time.time()

# Initialize count variables for statistics
count_renamed = 0
count_no_matches = 0
count_conflicts = 0

# Log file initialization
time_at_start = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
log_filename = f"logs\\MFR\\MFR_{time_at_start}.log"
if not os.path.exists("logs\\MFR\\"):
    os.makedirs("logs\\MFR\\")

with open(log_filename, 'w') as log_file:
    log_file.write(f"Log for Match File Rename - {time_at_start}\n")
    log_file.write(f"Rename folder: {rename_path}\n")
    log_file.write(f"Source folder: {source_path}\n\n")

rename_files = os.listdir(rename_path)  # File(s) to be renamed
source_files = os.listdir(source_path)  # File(s) to match name

# Create a list without extensions (e.x .zip) so that extension isn't overridden
source_files_name = [os.path.splitext(file)[0] for file in source_files]


def rename_file(file):
    global count_renamed, count_no_matches, count_conflicts, log_file
    rename_name, rename_ext = os.path.splitext(file)
    closest_match = difflib.get_close_matches(rename_name,
                                              source_files_name, 1, 0.45)
    if closest_match:
        try:
            # Get path of file to be renamed
            old_file_path = os.path.join(rename_path, file)

            # Path new file with correct extension
            new_file_name = closest_match[0] + rename_ext
            new_file_path = os.path.join(rename_path, new_file_name)

            os.rename(old_file_path, new_file_path)

        # TODO: Can improve on this by checking for which file would be a better
        #  match for the rename
        except FileExistsError:
            with open(log_filename, 'a') as log_file:
                log_file.write(f"Conflict: Already exists! {file} -> "
                               f"{closest_match}\n")
            count_conflicts += 1
        else:
            with open(log_filename, 'a') as log_file:
                log_file.write(f"Renamed: {file} -> {new_file_name}\n")
            count_renamed += 1

    else:
        with open(log_filename, 'a') as log_file:
            log_file.write(f"No match: {file}\n")
        count_no_matches += 1


# Use ThreadPoolExecutor to parallelize
with ThreadPoolExecutor() as executor:
    # Submit tasks for parallel execution
    futures = {executor.submit(rename_file, file): file for file in
               tqdm(rename_files, desc="Queuing files", colour="blue")}
    # # Progress bar and wait for completion
    for future in tqdm(as_completed(futures), total=len(rename_files),
                       desc="Processing files", colour="blue"):
        future.result()  # Ensure any exceptions are raised here

end_time = time.time()

# Summary to log
with open(log_filename, 'a') as log_file:
    log_file.write(f"\nSummary:\n")
    log_file.write(f"Renamed {count_renamed} files\n")
    log_file.write(f"No matches for: {count_no_matches} file(s)\n")
    log_file.write(f"{count_conflicts} naming conflicts\n")
    log_file.write(f"Time to run: {end_time - start_time:.3f} seconds")

# Summary to console
print(f"Renamed {count_renamed} file(s), no match(es) for {count_no_matches} "
      f"file(s), {count_conflicts} name conflict(s)")
print(f"Time to run: {end_time - start_time:.3f} seconds")
print(f"Log created at script_directory\\logs\\MFR\\{log_filename}")
