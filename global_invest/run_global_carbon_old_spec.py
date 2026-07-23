import os, sys
import hazelbean as hb
import pandas as pd

import ecosystem_services_tasks
import ecosystem_services_functions

# Create the project flow object
p = hb.ProjectFlow()

# Set project-directories
p.user_dir = os.path.expanduser('~')        
p.extra_dirs = ['Files', 'global_invest', 'projects']
p.project_name = 'test_global_invest'
p.project_name = p.project_name + '_' + hb.pretty_time() # Comment this line out if you want it to use an existing project. Will skip recreation of files that already exist.
p.project_dir = os.path.join(p.user_dir, os.sep.join(p.extra_dirs), p.project_name)
p.set_project_dir(p.project_dir) 

# Set basa_data_dir. Will download required files here.
p.base_data_dir = os.path.join(p.user_dir, 'Files', 'base_data')

# ADD THESE TWO LINES - Configure cloud bucket:
p.input_bucket_name = 'gtap_invest_seals_2023_04_21'
p.cloud_bucket_name = 'gtap_invest_seals_2023_04_21'
    
# Set model-paths
p.aoi = 'RWA'
p.base_year_lulc_path = p.get_path('lulc/esa/lulc_esa_2017.tif') # Defines the fine_resolution
p.region_ids_coarse_path = p.get_path('cartographic/ee/eemarine_r566_ids_10sec.tif') # Defines the coarse_resolution

# FOR COMPATIBILITY WITH SCENARIOS.CSV, CONSIDER renaming this regions_vector_path. TODOO
p.global_regions_vector_path = p.get_path('cartographic/ee/eemarine_r566_correspondence.gpkg') # Will be used to create the aoi vector
# ADD THIS LINE:
p.regions_vector_path = p.global_regions_vector_path  # Alias for compatibility
p.regions_column_label = 'iso3_r250_label' # name of column from the correspondence file

def build_task_tree(p):
    p.project_aoi_task = p.add_task(ecosystem_services_tasks.project_aoi)    
    p.aoi_inputs_task = p.add_task(ecosystem_services_tasks.aoi_inputs)    
    p.ecosystem_services_task = p.add_task(ecosystem_services_tasks.ecosystem_services)
    p.carbon_storage_simple_task = p.add_task(ecosystem_services_tasks.carbon_storage_simple, parent=p.ecosystem_services_task) # Just runs on the base year to prove its working
    p.carbon_storage_biophysical_task = p.add_task(ecosystem_services_tasks.carbon_storage_biophysical_invest, parent=p.ecosystem_services_task) # Requires a scenarios.csv becuase calcualtes differences
    # it was carbon_storage_biophysical, now changed to carbon_storage_biophysical_invest

# Build the task tree and excute it!
build_task_tree(p)
p.execute()
    
