"""Run the global_invest carbon-storage pipeline over a chosen AOI."""
import os
import hazelbean as hb

from global_invest import ecosystem_services_tasks
from global_invest import ecosystem_services_functions


def build_task_tree(p):
    p.project_aoi_task = p.add_task(ecosystem_services_tasks.project_aoi)
    p.aoi_inputs_task = p.add_task(ecosystem_services_tasks.aoi_inputs)
    p.ecosystem_services_task = p.add_task(ecosystem_services_tasks.ecosystem_services)
    p.carbon_storage_simple_task = p.add_task(ecosystem_services_tasks.carbon_storage_simple, parent=p.ecosystem_services_task) # Just runs on the base year to prove its working
    p.carbon_storage_biophysical_task = p.add_task(ecosystem_services_tasks.carbon_storage_biophysical_invest, parent=p.ecosystem_services_task) # Requires a scenarios.csv becuase calcualtes differences
    # it was carbon_storage_biophysical, now changed to carbon_storage_biophysical_invest


def run_project(project_name='test_global_invest', append_timestamp=False,
                tasks_to_skip=None, execute=True):
    """Build and execute the global carbon-storage task tree.

    append_timestamp=True gives each run a fresh project dir (the spec preference is a
    stable, resumable dir with append_timestamp=False, which resumes in place and skips
    tasks whose outputs already exist). Returns p.
    """
    p = hb.ProjectFlow()

    # Set project-directories
    p.user_dir = os.path.expanduser('~')
    p.extra_dirs = ['Files', 'global_invest', 'projects']
    p.project_name = project_name
    if append_timestamp:
        p.project_name = p.project_name + '_' + hb.pretty_time()
    p.project_dir = os.path.join(p.user_dir, os.sep.join(p.extra_dirs), p.project_name)
    p.set_project_dir(p.project_dir)

    # Set base_data_dir. Will download required files here.
    p.base_data_dir = os.path.join(p.user_dir, 'Files', 'base_data')

    # Configure cloud bucket
    p.input_bucket_name = 'gtap_invest_seals_2023_04_21'
    p.cloud_bucket_name = 'gtap_invest_seals_2023_04_21'

    # Set model-paths
    p.aoi = 'RWA'
    p.base_year_lulc_path = p.get_path('lulc/esa/lulc_esa_2017.tif') # Defines the fine_resolution
    p.region_ids_coarse_path = p.get_path('cartographic/ee/eemarine_r566_ids_10sec.tif') # Defines the coarse_resolution

    # FOR COMPATIBILITY WITH SCENARIOS.CSV, CONSIDER renaming this regions_vector_path. TODOO
    p.global_regions_vector_path = p.get_path('cartographic/ee/eemarine_r566_correspondence.gpkg') # Will be used to create the aoi vector
    p.regions_vector_path = p.global_regions_vector_path  # Alias for compatibility
    p.regions_column_label = 'iso3_r250_label' # name of column from the correspondence file

    build_task_tree(p)
    p.skip_tasks(tasks_to_skip)

    p.L = hb.get_logger('global_carbon')
    hb.log('Created ProjectFlow object at ' + p.project_dir)

    if execute:
        p.execute()

    return p


if __name__ == '__main__':
    run_project(append_timestamp=True)
