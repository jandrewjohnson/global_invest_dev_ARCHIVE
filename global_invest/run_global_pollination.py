import os, sys
import hazelbean as hb
import pandas as pd

import ecosystem_services_tasks
import ecosystem_services_functions

# Create the project flow object
p = hb.ProjectFlow()

# Configure cloud bucket
p.input_bucket_name = 'gtap_invest_seals_2023_04_21'

# Set project-directories
p.user_dir = os.path.expanduser('~')        
p.extra_dirs = ['Files', 'global_invest', 'projects']
p.project_name = 'test_global_pollination'
p.project_name = p.project_name + '_' + hb.pretty_time()
p.project_dir = os.path.join(p.user_dir, os.sep.join(p.extra_dirs), p.project_name)
p.set_project_dir(p.project_dir) 

# Set base_data_dir
p.base_data_dir = os.path.join(p.user_dir, 'Files', 'base_data')
    
# Set model-paths
p.aoi = 'RWA'
p.base_year_lulc_path = p.get_path('lulc/esa/lulc_esa_2017.tif')
p.region_ids_coarse_path = p.get_path('cartographic/ee/eemarine_r566_ids_10sec.tif')
p.global_regions_vector_path = p.get_path('cartographic/ee/eemarine_r566_correspondence.gpkg')

# Add these for compatibility:
p.regions_vector_path = p.global_regions_vector_path
p.regions_column_label = 'iso3_r250_label'

# Create scenarios DataFrame for pollination task
# This defines what years/scenarios to run
scenarios_data = {
    'scenario_label': ['baseline_2017'],
    'scenario_type': ['baseline'],
    'lulc_src_label': ['esa'],
    'lulc_simplification_label': ['seals7'],
    'model_label': ['test'],
    'base_years': [[2017]],  # List format
    'years': [[]],  # Empty for baseline
    'baseline_reference_label': ['']
}
p.scenarios_df = pd.DataFrame(scenarios_data)

# Set key years
p.key_base_year = 2017
p.base_years = [2017]

# Directory for stitched LULC outputs (will be created by aoi_inputs task)
p.stitched_lulc_simplified_scenarios_dir = os.path.join(p.cur_dir, 'lulc_scenarios')


def build_task_tree(p):
    # Setup tasks (same as carbon)
    p.project_aoi_task = p.add_task(ecosystem_services_tasks.project_aoi)    
    p.aoi_inputs_task = p.add_task(ecosystem_services_tasks.aoi_inputs)    
    p.ecosystem_services_task = p.add_task(ecosystem_services_tasks.ecosystem_services)
    
    # Pollination tasks
    p.pollination_biophysical_task = p.add_task(
        ecosystem_services_tasks.pollination_biophysical, 
        parent=p.ecosystem_services_task
    )
    
    # Optional: Add economic task later once biophysical works
    # p.pollination_economic_task = p.add_task(
    #     ecosystem_services_tasks.pollination_economic,
    #     parent=p.ecosystem_services_task
    # )


# Build the task tree and execute it!
build_task_tree(p)
p.execute()