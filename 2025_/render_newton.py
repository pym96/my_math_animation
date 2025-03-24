#!/usr/bin/env python
"""
Helper script for rendering Newton's Method animation.
This script handles common errors and makes rendering more robust.
"""

import os
import sys
import subprocess
import importlib
import importlib.util
import types
import logging

# Get the directory of this script
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ANIMATION_FILE = os.path.join(THIS_DIR, "newton_method.py")

def patch_manim_file_handling():
    """
    Patch Manim's file handling to avoid errors with cache files.
    This applies monkey patches to prevent errors when cleaning up files.
    """
    try:
        # Import manim modules that handle file operations
        from manim.scene.scene_file_writer import SceneFileWriter
        from manim import config
        
        # Store the original clean_cache method
        original_clean_cache = SceneFileWriter.clean_cache
        
        # Define our patched version that gracefully handles file errors
        def safe_clean_cache(self):
            try:
                # Try the original method
                original_clean_cache(self)
            except FileNotFoundError:
                print("Ignoring file not found error during cache cleaning")
            except PermissionError:
                print("Ignoring permission error during cache cleaning")
            except Exception as e:
                print(f"Ignoring error during cache cleaning: {e}")
                
        # Apply the patch
        SceneFileWriter.clean_cache = safe_clean_cache
        
        # Also patch the unlink method for all files in the cache directory
        original_unlink = os.unlink
        
        def safe_unlink(path, *args, **kwargs):
            try:
                return original_unlink(path, *args, **kwargs)
            except (FileNotFoundError, PermissionError) as e:
                print(f"Ignoring error when removing file {path}: {e}")
                return None
                
        # Apply the patch to os.unlink
        os.unlink = safe_unlink
        
        # Also disable caching and file cleanup in the config
        config.disable_caching = True
        config.flush_cache = False
        config.max_files_cached = 0
        
        print("Successfully patched Manim's file handling")
        return True
    except Exception as e:
        print(f"Failed to patch Manim's file handling: {e}")
        return False

def main():
    print("Starting Newton's Method animation rendering...")
    
    # Make sure the animation file exists
    if not os.path.exists(ANIMATION_FILE):
        print(f"Error: Animation file not found: {ANIMATION_FILE}")
        return 1
    
    # Patch Manim's file handling
    patch_manim_file_handling()
        
    cmd = [
        "manim", 
        "--no_latex_cleanup",   # Prevent latex cleanup errors
        "--disable_caching",    # Prevent cache-related errors
        "-pqh",                 # preview, medium quality, 1080p
        ANIMATION_FILE,
        "NewtonMethodAnimation"
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        # Set up environment variables to further control Manim behavior
        env = os.environ.copy()
        env["PYTHONPATH"] = os.pathsep.join([env.get("PYTHONPATH", ""), os.path.dirname(THIS_DIR)])
        
        # Run the command with the modified environment
        result = subprocess.run(cmd, text=True, capture_output=True, env=env)
        
        # Print the command output
        print(result.stdout)
        
        if result.stderr:
            print("Errors/Warnings:")
            print(result.stderr)
            
        # Check if successful
        if result.returncode == 0:
            print("Animation rendered successfully!")
            return 0
        else:
            print(f"Animation rendering failed with exit code: {result.returncode}")
            # Try to clean up any temp files that might be left
            try:
                os.system(f"find /Volumes/WD_BLACK/自媒体/manim_animation/my_math_animation/media -name '._*' -type f -delete")
            except:
                pass
            return result.returncode
            
    except Exception as e:
        print(f"Error running animation: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
if __name__ == "__main__":
    sys.exit(main()) 