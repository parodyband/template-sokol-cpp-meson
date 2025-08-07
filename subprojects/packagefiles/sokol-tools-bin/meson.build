project('sokol-tools-bin', 'c')

# This is just a tools repository, not a library dependency
# The tools will be available at: subprojects/sokol-tools-bin/bin/

# Export the tools directory path for use in the main project if needed
meson.override_find_program('sokol-shdc', 
    find_program('bin/sokol-shdc', 
                 'bin/win32/sokol-shdc.exe',
                 'bin/linux/sokol-shdc',
                 'bin/osx/sokol-shdc',
                 'bin/osx_arm64/sokol-shdc',
                 required: false))

# No dependency exported - this is just for tools
