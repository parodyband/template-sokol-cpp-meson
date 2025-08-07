project('sokol', 'c')

# Platform-specific dependencies
sokol_deps = []

if host_machine.system() == 'darwin'
    # macOS requires these frameworks for Sokol
    sokol_deps += dependency('appleframeworks', modules: [
        'Cocoa',
        'QuartzCore',
        'Metal',
        'MetalKit',
        'OpenGL',
        'CoreGraphics',
        'CoreFoundation',
        'AppKit',
        'Foundation'
    ])
elif host_machine.system() == 'windows'
    # Windows dependencies
    # Add Windows-specific dependencies if needed
elif host_machine.system() == 'linux'
    # Linux dependencies
    # Add Linux-specific dependencies if needed (e.g., X11, GL)
endif

sokol_dep = declare_dependency(
    include_directories: include_directories('.'),
    dependencies: sokol_deps
)

meson.override_dependency('sokol', sokol_dep)
