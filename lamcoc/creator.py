import zipfile
import os
import logging
from lamcoc.config import load_config
from lamcoc.file_selector import get_files_to_include, get_library_files

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def create_zip(project_root):
    """Create a ZIP file containing selected files, placing libraries at ZIP root if specified."""

    logging.info("Starting to create the Lambda ZIP package...")

    try:
        include_patterns, exclude_patterns, libraries = load_config(project_root)

        files = get_files_to_include(project_root, include_patterns, exclude_patterns)
        lib_files = {}

        # Process libraries only if they are specified
        if libraries:
            logging.info("Including libraries in the ZIP package...")
            lib_files = get_library_files(project_root, libraries)
        else:
            logging.info("No libraries specified, skipping library inclusion.")

        output_zip = os.path.join(project_root, "lambda.zip")

        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add regular files (preserve structure)
            for file in files:
                zipf.write(os.path.join(project_root, file), file)

            # Add library files (move to ZIP root)
            for abs_path, zip_root_path in lib_files.items():
                zipf.write(abs_path, zip_root_path)

        logging.info(f"✅ Lambda package created: {output_zip}")

    except FileNotFoundError as e:
        logging.error(f"❌ File not found: {e}", exc_info=True)
    except Exception as e:
        logging.error(f"❌ Error creating ZIP: {e}", exc_info=True)
