#!/usr/bin/env python3
"""
Shader compilation script using sokol-shdc
This script compiles shaders after the sokol-tools-bin subproject is downloaded
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def get_shdc_path():
    """Get the path to sokol-shdc based on the platform"""
    # When run from build directory by Meson, we need to go up one level
    if Path.cwd().name == 'build':
        base_path = Path("../subprojects/sokol-tools-bin/bin")
    else:
        base_path = Path("../subprojects/sokol-tools-bin/bin")
    
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        shdc = base_path / "win32" / "sokol-shdc.exe"
    elif system == "darwin":  # macOS
        if "arm" in machine or "aarch64" in machine:
            shdc = base_path / "osx_arm64" / "sokol-shdc"
        else:
            shdc = base_path / "osx" / "sokol-shdc"
    else:  # Linux and others
        shdc = base_path / "linux" / "sokol-shdc"
    
    return shdc

def compile_shader(input_file, output_file):
    """Compile a shader file"""
    shdc = get_shdc_path()
    
    if not shdc.exists():
        print(f"Error: sokol-shdc not found at {shdc}")
        print("Make sure to run 'meson setup build' first to download tools")
        return False
    
    # Command for compiling shaders with modern shader languages
    # glsl410 - Desktop OpenGL 4.1 (max for macOS)
    # glsl300es - OpenGL ES 3.0 / WebGL2
    # hlsl5 - Direct3D 11
    # metal_macos - macOS Metal
    # wgsl - WebGPU
    cmd = [
        str(shdc),
        "--input", str(input_file),
        "--output", str(output_file),
        "--slang", "glsl410:glsl300es:hlsl5:metal_macos:wgsl",
        "--format", "sokol"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[OK] Compiled {input_file} -> {output_file}")
            return True
        else:
            print(f"[ERROR] Failed to compile {input_file}")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Error running shader compiler: {e}")
        return False

def main():
    """Main function - compiles all shaders in the shaders directory"""
    
    # Since this script is now IN the shaders directory, adjust paths
    # When run from build directory by Meson
    if Path.cwd().name == 'build':
        shader_dir = Path("../shaders")
        output_dir = Path("../shaders/compiled")
    else:
        # If run directly from shaders directory
        shader_dir = Path(".")
        output_dir = Path("compiled")
    
    # Create directories if they don't exist
    shader_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    # Check if shader compiler exists
    shdc = get_shdc_path()
    if not shdc.exists():
        print(f"Note: Shader compiler not found at {shdc}")
        print("Shaders will be compiled when sokol-shdc is available")
        # Still create stamp file for successful run
        stamp_file = Path('shaders_compiled.stamp')
        stamp_file.write_text(f"No shaders compiled - compiler not available")
        return 0
    
    print(f"[OK] Shader compiler found at: {shdc}")
    
    # Find all .glsl files in the shaders directory
    shader_files = list(shader_dir.glob("*.glsl"))
    
    if not shader_files:
        print(f"No shader files found in {shader_dir}")
    else:
        print(f"Found {len(shader_files)} shader file(s) to compile")
        
        compiled_count = 0
        for shader_file in shader_files:
            # Generate output filename (e.g., simple.glsl -> simple.h)
            output_file = output_dir / (shader_file.stem + ".h")
            
            print(f"Compiling: {shader_file.name} -> {output_file.name}")
            if compile_shader(shader_file, output_file):
                compiled_count += 1
        
        print(f"Successfully compiled {compiled_count}/{len(shader_files)} shader(s)")
    
    # Create stamp file for Meson (indicates script ran successfully)
    # When run by Meson, output directory is the current working directory
    stamp_file = Path('shaders_compiled.stamp')
    stamp_file.write_text(f"Compiled {len(shader_files)} shaders")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
