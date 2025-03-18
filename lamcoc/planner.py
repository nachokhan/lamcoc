from lamcoc.config import load_config
from lamcoc.file_selector import get_files_to_include, get_library_files
import os
import fnmatch


def generate_plan(project_root):
    """Generate a plan of files to be included in the ZIP, ensuring exclusions are respected."""
    
    # Load config
    include_patterns, exclude_patterns, libraries = load_config(project_root)

    # Get included files (excluding files based on exclusion patterns)
    files = get_files_to_include(project_root, include_patterns, exclude_patterns)

    # Get library files (placing them at ZIP root, but respecting exclusions)
    all_lib_files = get_library_files(project_root, libraries)

    # Apply exclusions to libraries as well
    lib_files = {abs_path: zip_root_path for abs_path, zip_root_path in all_lib_files.items()
                 if not any(fnmatch.fnmatch(zip_root_path, pat) for pat in exclude_patterns)}

    # Define output files
    plan_file = os.path.join(project_root, "plan_to_zip.txt")
    final_plan_file = os.path.join(project_root, "planned_zip.txt")

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

    print(f"✅ Plan generated: {plan_file}")
    print(f"✅ Final ZIP structure generated: {final_plan_file} (exclusions applied)")
