from tljh.hooks import hookimpl


@hookimpl
def tljh_extra_user_pip_packages():
    return [
        '--extra-index-url=https://packages.dea.ga.gov.au',
        'datacube[performance,s3]>=1.8.4.dev0',
        'eodatasets3>=0.15.1',
        'odc_algo[hdstats]',
        'odc_ui',
        'odc_index',
        'odc_aws',
        'odc_geom',
        'odc_io',
        'odc_aio',
        'odc_dscache',
        'odc_dtools',
        'odc-apps-dc-tools',
        'odc-apps-cloud',
        'odc_ppt',
        'datacube-stats',
        '--no-binary=rasterio,Shapely,pygeos,netCDF4,pyproj,fc,hdstats,lmdb,lxml,numexpr,pyzmq,msgpack,ruamel.yaml.clib,zstandard'
    ]

# def   tljh_post_install():
#     """
#     Post install script to be executed after installation
#     and after all the other hooks.
#     This can be arbitrary Python code.
#     """
#     return [
#     ]


@hookimpl
def tljh_config_post_install(config):
    """
    Set JupyterLab to be default
    """
    user_environment = config.get('user_environment', {})
    user_environment['default_app'] = user_environment.get(
        'default_app', 'jupyterlab')

    config['user_environment'] = user_environment


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
        # 'git',
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
        # 'python3-pip',
        # 'python3-venv'
        'sqlite3',
        'libjpeg-dev',
        'libexpat-dev',
        'libxerces-c-dev',
        'libwebp-dev',
        'libzstd-dev',
        'libtiff5-dev',
        'libpng-dev',
        'libgif-dev',
        'libdeflate-dev',
        'libnetcdf-dev',
        'libhdf4-alt-dev',
        'libhdf5-serial-dev',
        'libopenjp2-7-dev',
        'libkml-dev',
        'libatlas-base-dev',
        'gfortran',
        'libspatialindex-dev',
        'libsfcgal-dev',
        'libudunits2-dev',
        'libgeos-dev',
        'libgeos++-dev',
        'libpq-dev'
    ]
