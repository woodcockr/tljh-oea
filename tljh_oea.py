from tljh.hooks import hookimpl
import sh

@hookimpl
def tljh_extra_user_conda_packages():
    return ['gdal==3.3.2']

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
        # 'gdal==3.3.2',
        'folium',
        'scipy',
        'pandas==1.3.4',
        'xarray',
        'matplotlib==3.4.3',
        'geopandas',
        'scikit-image',
        'tqdm',
        'click<8.0.0',
        'python-dateutil==2.7.5',
        # '--no-binary=Cython,rasterio,Shapely,pygeos,netCDF4,pyproj,fc,hdstats,lmdb,lxml,numexpr,pyzmq,msgpack,ruamel.yaml.clib,zstandard'
    ]

@hookimpl
def tljh_post_install():
    """
    Post install script to be executed after installation
    and after all the other hooks.
    This can be arbitrary Python code.
    """
    postgres_password = 'superPassword'
    sh.service("postgresql", "start")

    # TODO There is no doubt a simpler python way to achieve this outcome but as I am debugging this line by line
    # TODO and its making its way to completion and I am lazy I will leave the refactor until later

    # Some guards in case running the install script repeatedly in same container. This will remove the database
    sh.su("-", "postgres", "-c", "psql -c 'DROP DATABASE IF EXISTS datacube;'")
    sh.su("-", "postgres", "-c", "psql -c 'DROP EXTENSION IF EXISTS postgis;'")
    sh.su("-", "postgres", "-c", "psql -c 'CREATE EXTENSION postgis;'")
    sh.su("-", "postgres", "-c", "psql -c 'CREATE DATABASE datacube;'")
    # annoyingly the datacube system commands will require a postgres super user password
    # and also the specification to use localhost for the database hostname
    sh.su("-", "postgres", "-c", f"psql -c \"ALTER USER postgres PASSWORD \'{postgres_password}\';\"")
    sh.su("-", "postgres", "-c", f"source /opt/tljh/user/bin/activate && DB_HOSTNAME=localhost DB_USERNAME=postgres DB_PASSWORD={postgres_password} DB_DATABASE=datacube datacube -v system init")

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
        'postgresql',
        'postgresql-contrib',
        'postgis',
    ]
