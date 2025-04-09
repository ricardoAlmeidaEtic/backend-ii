import os
import shutil
import threading
import logging

def copy_file(source, destination):
    logging.info("Copying file: %s to %s", source, destination)
    shutil.copy(source, destination)
    logging.info("Finished copying file: %s", source)

def synchronize_folders(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    if not os.path.exists(source_folder):
        os.makedirs(source_folder)

    threads = []
    for file_name in os.listdir(source_folder):
        source_file = os.path.join(source_folder, file_name)
        destination_file = os.path.join(destination_folder, file_name)

        if os.path.isfile(source_file):
            thread = threading.Thread(target=copy_file, args=(source_file, destination_file))
            print(f"Thread {thread.name} created for copying {source_file} to {destination_file}")
            threads.append(thread)
            thread.start()

    for thread in threads:
        logging.info("Waiting for thread %s to finish", thread.name)
        thread.join()
        logging.info("Thread %s finished", thread.name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    source_folder = "./source_folder"
    destination_folder = "./destination_folder"

    logging.info("Starting folder synchronization...")
    synchronize_folders(source_folder, destination_folder)
    logging.info("Folder synchronization completed!")