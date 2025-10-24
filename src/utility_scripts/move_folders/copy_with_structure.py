import os
import shutil


def copy_files_with_structure(source_root, dest_root, files_to_copy):
    """
    Copies specific files from source_root to dest_root, preserving folder structure.

    :param source_root: Path to the main source folder.
    :param dest_root: Path to the destination folder.
    :param files_to_copy: List of file paths (absolute or relative to source_root).
    """
    source_root = os.path.abspath(source_root)
    dest_root = os.path.abspath(dest_root)

    for file_path in files_to_copy:
        # Make sure we use absolute paths
        abs_file_path = (
            file_path if os.path.isabs(file_path)
            else os.path.join(source_root, file_path)
        )

        if not os.path.exists(abs_file_path):
            print(f"⚠️ File not found: {abs_file_path}")
            continue

        # Calculate relative path (to preserve structure)
        rel_path = os.path.relpath(abs_file_path, source_root)
        dest_path = os.path.join(dest_root, rel_path)

        # Create destination subfolders if needed
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        # Copy the file
        shutil.copy2(abs_file_path, dest_path)
        print(f"✅ Copied: {rel_path}")


if __name__ == "__main__":
    # Example usage
    SOURCE_DIR = r"C:\Projects\ParentFolder"
    DEST_DIR = r"C:\Backup\SelectedFiles"

    # List of files you want to copy (relative to SOURCE_DIR)
    FILES_TO_COPY = [
        "data/info.json",
        "images/cars/car1.png",
        "scripts/utils/helpers.py",
    ]

    copy_files_with_structure(SOURCE_DIR, DEST_DIR, FILES_TO_COPY)
