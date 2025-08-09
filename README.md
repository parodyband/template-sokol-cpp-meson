# Sokol Meson Project

A Sokol graphics application with automatic shader compilation using the Meson build system.

## Prerequisites

- C++ compiler (GCC, Clang, or MSVC)
- [Meson](https://mesonbuild.com/) build system
- [Ninja](https://ninja-build.org/) (recommended)
- Python 3.7+ (for Meson and shader compilation)

## Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd sokol_meson

# Setup build directory (Meson will auto-download all dependencies)
meson setup buildDir

# Compile (this also compiles shaders automatically)
meson compile -C buildDir

# Run the triangle demo
./buildDir/sokol_meson.exe  # Windows
./buildDir/sokol_meson      # Linux/macOS
```

## Features

- **Automatic Shader Compilation**: All `.glsl` files in `shaders/` are automatically compiled to C headers
- **Cross-platform**: Generates shaders for OpenGL, Direct3D, Metal, and WebGPU
- **Header-only Libraries**: Uses Sokol's single-file libraries
- **Dependency Management**: All dependencies auto-download via Meson wraps

## Project Structure

```
sokol_meson/
├── main.cpp                    # Application entry point (triangle demo)
├── meson.build                 # Build configuration
├── shaders/                    # Shader files
│   ├── compile_shaders.py      # Shader compilation script
│   ├── *.glsl                  # GLSL shader sources
│   └── compiled/               # Generated shader headers (git-ignored)
│       └── *.h
├── subprojects/                # Dependencies (auto-downloaded)
│   ├── *.wrap                  # Dependency definitions (committed)
│   ├── sokol/                  # Sokol headers (git-ignored)
│   ├── sokol-tools-bin/        # Shader compiler (git-ignored)
│   └── fmt-*/                  # fmt library (git-ignored)
└── buildDir/                   # Build output (git-ignored)
```

## Dependencies

All dependencies are automatically managed by Meson through wrap files:

- **[Sokol](https://github.com/floooh/sokol)** - Graphics, application framework, and utilities
- **[fmt](https://github.com/fmtlib/fmt)** - Modern C++ formatting library
- **[sokol-tools-bin](https://github.com/floooh/sokol-tools-bin)** - Shader cross-compiler

These are downloaded automatically when you run `meson setup buildDir`.

## Shader System

### Writing Shaders

Create `.glsl` files in the `shaders/` directory using Sokol's shader format:

```glsl
@vs vertex_shader
in vec4 position;
void main() {
    gl_Position = position;
}
@end

@fs fragment_shader
out vec4 FragColor;
void main() {
    FragColor = vec4(1.0, 0.5, 0.2, 1.0);
}
@end

@program my_shader vertex_shader fragment_shader
```

### Using Compiled Shaders

Shaders are automatically compiled to `shaders/compiled/*.h` and can be included:

```cpp
#include "sokol_gfx.h"
#include "my_shader.h"  // Your compiled shader

// In your init function:
sg_shader shd = sg_make_shader(my_shader_shader_desc(sg_query_backend()));
```

### Manual Shader Compilation

If needed, you can manually compile shaders:

```bash
cd shaders
python compile_shaders.py
```

## IDE/Linter Support

To get proper code completion and error checking in your IDE:

```bash
# Generate compile_commands.json for IDE/linter
cd buildDir && ninja -t compdb > ../compile_commands.json && cd ..
```

This file is git-ignored but essential for IDE features like:
- Header file discovery
- Code completion
- Error checking

### Supported IDEs

- **VS Code**: Uses compile_commands.json automatically
- **CLion**: Auto-detects compile_commands.json
- **Vim/Neovim (with clangd)**: Uses .clangd config

## Building Options

```bash
# Standard build
meson compile -C buildDir

# Clean rebuild
meson setup buildDir --wipe
meson compile -C buildDir

# Release build
meson setup buildDirRelease --buildtype=release
meson compile -C buildDirRelease
```

## Controls

- **ESC** - Quit the application

## Troubleshooting

### Shader Compilation Errors
- Ensure Python is installed and in PATH
- Check that sokol-tools-bin downloaded correctly in `subprojects/`

### Missing Headers in IDE
- Regenerate compile_commands.json (see IDE/Linter Support section)
- Reload your IDE window

### Build Errors
- Run `meson setup buildDir --wipe` for a clean configuration
- Ensure all subprojects downloaded: `meson subprojects download`