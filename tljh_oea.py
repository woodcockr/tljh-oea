from tljh.hooks import hookimpl

@hookimpl
def tljh_extra_apt_packages():
    return [
        'postgresql',
        'postgresql-contrib',
        'postgis',
        'gawk',
        'g++',
        'gcc',
        'bzip2',
        'sed',
        'less',
        'wget',
        'curl',
        'vim',
        'tmux',
        'htop',
        'fish',
        'tig',
        'git',
        'xz-utils',
        'openssh-client',
        'graphviz',
        'sudo',
        'iproute2',
        'iputils-ping',
        'net-tools',
        'simpleproxy',
        'rsync',
        'hdf5-tools',
        'netcdf-bin',
        'unzip',
        'zip',
        'python3-dev',
        'python3-pip',
        'python3-venv'
    ]
