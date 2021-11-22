from tljh.hooks import hookimpl
import sh

@hookimpl
def tljh_extra_user_pip_packages():
    return [
        'Cython',
        'numpy',
        'rasterio',
        '--extra-index-url=https://packages.dea.ga.gov.au',
        'datacube[performance,s3]==1.8.6',
        'eodatasets3',
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
        # '--no-binary=Cython,rasterio,Shapely,pygeos,netCDF4,pyproj,fc,hdstats,lmdb,lxml,numexpr,pyzmq,msgpack,ruamel.yaml.clib,zstandard'
    ]

# def tljh_config_post_install(config):
#     """
#     Post install script to be executed after installation
#     and after all the other hooks.
#     This can be arbitrary Python code.
#     """


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
        'less',
        'wget',
        'curl',
        'vim',
        'htop',
        'unzip',
        'zip',
        'python3-dev',
        'libpq-dev',
    ]
