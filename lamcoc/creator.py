import zipfile
import os
from lamcoc.config import load_config
from lamcoc.file_selector import get_files_to_include, get_library_files


def create_zip(project_root):
    """Create a ZIP file containing the selected files, placing libraries at ZIP root."""
    include_patterns, exclude_patterns, libraries = load_config(project_root)
    files = get_files_to_include(project_root, include_patterns, exclude_patterns)
    lib_files = get_library_files(project_root, libraries)

    output_zip = os.path.join(project_root, "lambda.zip")

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Add regular files (preserve structure)
        for file in files:
            zipf.write(os.path.join(project_root, file), file)

        # Add library files (move to ZIP root)
        for abs_path, zip_root_path in lib_files.items():
            zipf.write(abs_path, zip_root_path)

    print(f"✅ Lambda package created: {output_zip}")
