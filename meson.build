project('sokol_meson', 'cpp',
        version: '1.0.0',
        default_options: [
                'cpp_std=c++20',
                'default_library=static',
                'werror=false'
        ]
)

fmt_dep = dependency('fmt', fallback: ['fmt', 'fmt_dep'])
sokol_dep = dependency('sokol', fallback: ['sokol', 'sokol_dep'])

# Download shader compilation tools (not a dependency, just tools)
sokol_tools = subproject('sokol-tools-bin', required: false)
if sokol_tools.found()
    message('Sokol shader tools available in subprojects/sokol-tools-bin/bin/')
endif

# Find Python for shader compilation
python = import('python').find_installation('python3', required: false)

# Shader compilation setup
compile_shaders_enabled = python.found() and get_option('compile_shaders')

if compile_shaders_enabled
    shader_compile = custom_target('compile_shaders',
        output: 'shaders_compiled.stamp',
        command: [python, files('shaders/compile_shaders.py')],
        build_by_default: true,
        build_always_stale: true  # Always check if shaders need recompiling
    )
    # Add shader compilation as a source dependency to ensure it runs first
    shader_sources = shader_compile
else
    if not python.found()
        message('Python not found, shader compilation disabled')
    else
        message('Shader compilation disabled (use -Dcompile_shaders=true to enable)')
    endif
    shader_sources = []
endif

# Main executable with shader dependencies
sokol_meson_sources = ['main.cpp']
if compile_shaders_enabled
    # This ensures shaders are compiled before the executable
    sokol_meson_sources += shader_sources
endif

# Platform-specific compiler arguments
cpp_args = ['-Wno-unknown-pragmas']

# On macOS, we need to compile as Objective-C++ because Sokol includes Cocoa headers
if host_machine.system() == 'darwin'
    cpp_args += ['-x', 'objective-c++']
endif

sokol_meson = executable(
        'sokol_meson',
        sokol_meson_sources,
        dependencies: [fmt_dep, sokol_dep],
        cpp_args: cpp_args,
        include_directories: include_directories('shaders/compiled', is_system: false)
)

test('test', sokol_meson)