import fnmatch
import os


def get_files_to_include(project_root, include_patterns, exclude_patterns):
    """Find files matching include patterns and remove those matching exclude patterns."""
    all_files = set()

    # Traverse project directory
    for root, _, files in os.walk(project_root):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, project_root)  # Make paths relative

            # Include only if it matches at least one include pattern
            if any(fnmatch.fnmatch(relative_path, pat) for pat in include_patterns):
                all_files.add(relative_path)

    # Apply exclusions
    excluded_files = {file for file in all_files if any(fnmatch.fnmatch(file, pat) for pat in exclude_patterns)}

    return sorted(all_files - excluded_files)


def get_library_files(project_root, libraries):
    """Get all files from library directories while preserving their relative paths."""
    lib_files = {}

    for lib_path in libraries:
        abs_lib_path = os.path.join(project_root, lib_path)
        if not os.path.exists(abs_lib_path):
            print(f"⚠️ Library path not found: {abs_lib_path}")
            continue

        for root, _, files in os.walk(abs_lib_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path_within_lib = os.path.relpath(full_path, abs_lib_path)
                lib_files[full_path] = rel_path_within_lib  # Preserve structure inside lib dir

    return lib_files
