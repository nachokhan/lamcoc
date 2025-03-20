import logging
import os
import fnmatch
from lamcoc.config import load_config
from lamcoc.file_selector import get_files_to_include, get_library_files

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def generate_plan(project_dir, output_dir, config_dir, config_file, zip_file, **kwargs):
    """Generate a plan of files to be included in the ZIP, ensuring exclusions are respected."""

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

        # Get included files (excluding based on patterns)
        files = get_files_to_include(project_dir, include_patterns, exclude_patterns)

        # Process libraries if specified
        lib_files = {}
        if libraries:
            logging.info("Processing libraries for inclusion in ZIP...")
            all_lib_files = get_library_files(project_dir, libraries)

            # Apply exclusions to libraries as well
            lib_files = {
                abs_path: zip_root_path
                for abs_path, zip_root_path in all_lib_files.items()
                if not any(fnmatch.fnmatch(zip_root_path, pat) for pat in exclude_patterns)
            }
        else:
            logging.info("No libraries specified, skipping library inclusion.")

        # Define output files
        plan_file = os.path.join(output_dir, "plan_to_zip.txt")
        final_plan_file = os.path.join(output_dir, "planned_zip.txt")

        # Save plan_to_zip.txt (original paths before modification)
        with open(plan_file, "w") as f:
            for file in files:
                f.write(file + "\n")

        # Save planned_zip.txt (final structure inside ZIP, with exclusions applied)
        with open(final_plan_file, "w") as f:
            for file in files:
                f.write(file + "\n")  # Regular files maintain their paths
            for _, zip_root_path in lib_files.items():
                f.write(zip_root_path + "\n")  # Libraries go to ZIP root

        logging.info(f"✅ Plan generated: {plan_file}")
        logging.info(f"✅ Final ZIP structure saved: {final_plan_file}")

    except Exception as e:
        logging.error(f"❌ Error generating plan: {e}", exc_info=True)
