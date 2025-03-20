import zipfile
import os
import logging
from lamcoc.config import load_config
from lamcoc.file_selector import get_files_to_include, get_library_files

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def create_zip(project_dir, output_dir, config_dir, config_file, zip_file, **kwargs):
    """Create a ZIP file containing selected files, placing libraries at ZIP root if specified."""

    logging.info(f"📂 Project directory: {project_dir}")
    logging.info(f"📂 Output directory: {output_dir}")
    logging.info(f"📂 Config file: {os.path.join(config_dir, config_file)}")
    logging.info(f"📦 ZIP file name: {zip_file}")

    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Load config from the specified directory and file
        config_path = os.path.join(config_dir, config_file)
        include_patterns, exclude_patterns, libraries = load_config(config_path)

        files = get_files_to_include(project_dir, include_patterns, exclude_patterns)
        lib_files = {}

        # Process libraries only if they are specified
        if libraries:
            logging.info("Including libraries in the ZIP package...")
            lib_files = get_library_files(project_dir, libraries)
        else:
            logging.info("No libraries specified, skipping library inclusion.")

        output_zip = os.path.join(output_dir, zip_file)

        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add regular files (preserve structure)
            for file in files:
                zipf.write(os.path.join(project_dir, file), file)

            # Add library files (move to ZIP root)
            for abs_path, zip_root_path in lib_files.items():
                zipf.write(abs_path, zip_root_path)

        logging.info(f"✅ Lambda package created: {output_zip}")

    except FileNotFoundError as e:
        logging.error(f"❌ File not found: {e}", exc_info=True)
    except Exception as e:
        logging.error(f"❌ Error creating ZIP: {e}", exc_info=True)
