import os

def create_directory_structure(base_dir="meeting_data"):
    # List of subdirectories to be created in each WP# folder
    subdirectories = ["raw_data", "transcripts", "whisper_summary", "key_terms"]

    # Create the base directory if it doesn't already exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Loop through numbers 1 to 10 to create WP# folders
    for i in range(1, 11):
        wp_folder = os.path.join(base_dir, f"WP{i}")
        os.makedirs(wp_folder, exist_ok=True)  # Create WP# folder

        # Create each of the specified subdirectories inside the current WP# folder
        for subdirectory in subdirectories:
            os.makedirs(os.path.join(wp_folder, subdirectory), exist_ok=True)

    print(f"Directory structure created under '{base_dir}'.")

if __name__ == "__main__":
    create_directory_structure()
