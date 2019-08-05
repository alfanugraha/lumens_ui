#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os.path
import io

class MenuFactory:
    
    APP_ADD_LAYER = "Application.add_layer"
    APP_DELETE_LAYER = "Application.delete_layer"
    APP_ZOOM_IN = "Application.zoom_in"
    APP_ZOOM_OUT = "Application.zoom_out"
    APP_ZOOM_FULL = "Application.zoom_full"
    APP_ZOOM_TO_SELECTED = "Application.zoom_to_selected"
    APP_ZOOM_TO_LAYER = "Application.zoom_to_layer"
    APP_ZOOM_LAST = "Application.zoom_last"
    APP_ZOOM_NEXT = "Application.zoom_next"
    APP_PAN = "Application.pan"
    APP_PAN_TO_SELECTED = "Application.pan_to_selected"
    APP_REFRESH = "Application.refresh"
    APP_ATTRIBUTE_TABLE = "Application.attribute_table"
    APP_ATTRIBUTE_TOTAL_FEATURES = "Application.attribute_total_features"
    APP_DELETE_SELECTED_FEATURE = "Application.delete_selected_feature"
    APP_LAYER_ATTRIBUTE_TABLE = "Application.layer_attribute_table"
    APP_ATTRIBUTE_EDITOR = "Application.attribute_editor" 
    APP_LAYER_ATTRIBUTE_EDITOR = "Application.layer_attribute_editor"
    
    APP_LAYER_PROP_STYLE = "Application.layer_properties_style"
    APP_LAYER_PROP_TRANSPARENCY = "Application.layer_properties_transparency"
    APP_LAYER_PROP_SINGLE = "Application.layer_properties_single"
    APP_LAYER_PROP_CATEGORIZED = "Application.layer_properties_categorized"
    APP_LAYER_PROP_GRADUATED = "Application.layer_properties_graduated"
    APP_LAYER_PROP_LAYER_TRANSPARENCY = "Application.layer_properties_layer_transparency"
    APP_LAYER_PROP_FILL_COLOR = "Application.layer_properties_fill_color"
    APP_LAYER_PROP_ATTRIBUTE = "Application.layer_properties_attribute"
    APP_LAYER_PROP_VALUE = "Application.layer_properties_value"
    APP_LAYER_PROP_LABEL = "Application.layer_properties_label"
    APP_LAYER_PROP_ADD = "Application.layer_properties_add"
    APP_LAYER_PROP_DELETE = "Application.layer_properties_delete"
    APP_LAYER_PROP_DELETE_ALL = "Application.layer_properties_delete_all"
    APP_LAYER_PROP_COLOR = "Application.layer_properties_color"
    APP_LAYER_PROP_LOWER_VALUE = "Application.layer_properties_lower_value"
    APP_LAYER_PROP_UPPER_VALUE = "Application.layer_properties_upper_value"
    APP_LAYER_PROP_RULE = "Application.layer_properties_rule"
    APP_LAYER_PROP_MIN_SCALE = "Application.layer_properties_min_scale"
    APP_LAYER_PROP_MAX_SCALE = "Application.layer_properties_max_scale"
    APP_LAYER_PROP_ENABLE = "Application.layer_properties_enable"
    APP_LAYER_PROP_LABEL_ATTRIBUTE = "Application.layer_properties_label_attribute"
    APP_LAYER_PROP_LABEL_SIZE = "Application.layer_properties_label_size"
    APP_LAYER_PROP_LABEL_COLOR = "Application.layer_properties_label_color"
    APP_LAYER_PROP_APPLY = "Application.layer_properties_apply"
    
    APP_SELECT_FEATURES_BY_EXPRESSION = "Application.select_features_by_expression"
    APP_LAYER_PROPERTIES = "Application.layer_properties"
    APP_TOGGLE_EDIT_LAYER = "Application.toggle_edit_layer"
    APP_SELECT = "Application.select"
    APP_INFO = "Application.info"
    APP_ACTIVE_PROJECT = "Application.active_project"
    APP_DASHBOARD = "Application.dashboard"
    APP_CLOSE_DASHBOARD = "Application.close_dashboard"
    APP_BROWSER = "Application.browser"
    APP_LAYERS = "Application.layers"
    APP_TABLE_EDITOR = "Application.table_editor"
    APP_EXPLORE = "Application.explore"
    APP_EXPLORE_NAME = "Application.explore_name"
    APP_PROJ = "Application.project"
    APP_PROJ_CREATE = "Application.project_create"
    APP_PROJ_DETAILS = "Application.project_details"
    APP_PROJ_NAME = "Application.project_name"
    APP_PROJ_OUTPUT_FOLDER = "Application.project_output_folder"
    APP_PROJ_BOUNDARY = "Application.project_boundary"
    APP_PROJ_BOUNDARY_ATTRIBUTE = "Application.project_boundary_attribute"
    APP_PROJ_DESCRIPTION = "Application.project_description"
    APP_PROJ_LOCATION = "Application.project_location"
    APP_PROJ_PROVINCE = "Application.project_province"
    APP_PROJ_COUNTRY = "Application.project_country"
    APP_PROJ_SPATIAL_RESOLUTION = "Application.project_spatial_resolution"
    APP_PROJ_DISSOLVED = "Application.project_dissolved"
    APP_PROJ_NEW = "Application.project_new"
    APP_PROJ_OPEN = "Application.project_open"
    APP_PROJ_CLOSE = "Application.project_close"
    APP_PROJ_EXPORT = "Application.project_export"
    APP_PROJ_ADD_DATA = "Application.project_add_data"
    APP_PROJ_REMOVE_DATA = "Application.project_remove_data"
    APP_ADD_DATA_DEFINE_PROPERTIES = "Application.add_data_define_properties"
    APP_ADD_DATA_ADD_ITEM = "Application.add_data_add_item"
    APP_ADD_DATA_LAND_USE_COVER = "Application.add_data_land_use_cover"
    APP_ADD_DATA_PLANNING_UNIT = "Application.add_data_planning_unit"
    APP_ADD_DATA_FACTOR = "Application.add_data_factor"
    APP_ADD_DATA_TABLE = "Application.add_data_table"
    APP_ADD_DATA_SELECT_FILE = "Application.add_data_select_file"
    APP_ADD_DATA_FILE = "Application.add_data_file"
    APP_PROPERTIES = "Application.properties"
    APP_ADD_DATA_PROPERTIES = "Application.add_data_properties"
    APP_ADD_DATA_RASTER = "Application.add_data_raster"
    APP_PROP_DESCRIPTION = "Application.properties_description"
    APP_PROP_YEAR = "Application.properties_year"
    APP_PROP_CLASS_DEFINITION_FILE = "Application.properties_class_definition_file"
    APP_PROP_LEGEND = "Application.properties_legend"
    APP_PROP_UNIDENTIFIED_LANDUSE = "Application.properties_unidentified_landuse"
    APP_PROP_CLASSIFIED = "Application.properties_classified"
    APP_PROP_FIRST_CLASS = "Application.properties_first_class"
    APP_PROP_SECOND_CLASS = "Application.properties_second_class"
    APP_PROP_THIRD_CLASS = "Application.properties_third_class"
    APP_PROP_FOURTH_CLASS = "Application.properties_fourth_class"
    APP_PROP_FIFTH_CLASS = "Application.properties_fifth_class"
    APP_PROP_SIXTH_CLASS = "Application.properties_sixth_class"
    APP_PROP_SEVENTH_CLASS = "Application.properties_seventh_class"
    APP_PROP_EIGHTH_CLASS = "Application.properties_eighth_class"
    APP_ADD_VECTOR_DATA = "Application.add_vector_data"
    APP_PROP_FIELD_ATTRIBUTE = "Application.properties_field_attribute"
    APP_PROP_DISSOLVE = "Application.properties_dissolve"
    APP_ADD_TABULAR_DATA = "Application.add_tabular_data"
    APP_ADD_DATA_PROPERTIES_SAVE = "Application.add_data_properties_save"
    APP_ADD_DATA_PROSES = "Application.add_data_proses"
    APP_PROJECT_DELETE_DATA = "Application.project_delete_data"
    APP_DELETE_DATA_DATA = "Application.delete_data_data"
    APP_DELETE_DATA_DESCRIPTION = "Application.delete_data_description"
    APP_DELETE_DATA_ACTION = "Application.delete_data_action"
    APP_DELETE_DATA_DELETE_ACTION = "Application.delete_data_delete_action"
    APP_PROJ_STATUS = "Application.project_status"
    APP_BROWSE = "Application.browse"
    APP_SELECT_LUMENS_DATABASE = "Application.select_lumens_database"
    APP_LUMENS_PROJ_FILE = "Application.lumens_project_file"
    APP_LUMENS_PROJ_ARCHIVE = "Application.lumens_project_archive"
    APP_SELECT_WORKING_DIRECTORY = "Application.select_working_directory"
    APP_LUMENS_HELP = "Application.lumens_help"
    APP_PRESS_F11 = "Application.press_f11"
    APP_VECTOR_RASTER_FILE = "Application.vector_raster_file"
    APP_DBF_FILE = "Application.dbf_file"
    APP_CSV_FILE = "Application.csv_file"
    APP_FEATURE_INFO = "Application.feature_info"
    APP_LUMENS_VIEWER = "Application.lumens_viewer"
    APP_TABLE_EDITOR = "Application.table_editor"
    APP_TABLE_EDITOR_LOOKUP_TABLE = "Application.table_editor_lookup_table"
    APP_TABLE_EDITOR_LOAD = "Application.table_editor_load"
    APP_TABLE_EDITOR_SAVE= "Application.table_editor_save"
    
    FILE_EXIT = "FileMenu.exit"
    VIEW_MENU_BAR = "ViewMenu.menu_bar"
    VIEW_DASHBOARD = "ViewMenu.dashboard"
    VIEW_TOP_TOOLBAR = "ViewMenu.top_toolbar"
    VIEW_MAP_TOOLBAR = "ViewMenu.map_toolbar"
    MODE_PAN = "ModeMenu.pan"
    MODE_SELECT = "ModeMenu.select"
    MODE_INFO = "ModeMenu.info"
    TOOLS_PIVOT_TABLE = "ToolsMenu.pivot_table"
    HELP_OPEN_HELP = "HelpMenu.open_help"
    HELP_ABOUT_LUMENS = "HelpMenu.about_lumens"
    
    PUR_TITLE = "PUR.title"
    PURBUILD_BUILD = "PURBuild.build"
    PURBUILD_SETUP_REFERENCE = "PURBuild.setup_reference"
    PURBUILD_REFERENCE_DATA = "PURBuild.reference_data"
    PURBUILD_LOAD_TABLE = "PURBuild.load_table"
    PURBUILD_REFERENCE_CLASS = "PURBuild.reference_class"
    PURBUILD_EDIT_CLASS = "PURBuild.edit_class"
    PURBUILD_EDIT_REFERENCE_CLASS = "PURBuild.edit_reference_class"
    PURBUILD_ADD_REFERENCE_CLASS = "PURBuild.add_reference_class"
    PURBUILD_CONSERVATION = "PURBuild.conservation"
    PURBUILD_PRODUCTION = "PURBuild.production"
    PURBUILD_OTHER = "PURBuild.other"
    PUBBUILD_RECONCILIATION = "PUBBuild.reconciliation"
    PUBBUILD_ADDITIONAL = "PUBBuild.additional"
    PUBBUILD_SAVE = "PUBBuild.save"
    PURBUILD_CANCEL = "PURBuild.cancel"
    PURBUILD_ATTRIBUTE_REFERENCE_MAPPING = "PURBuild.attribute_reference_mapping"
    PURBUILD_ATTRIBUTE_VALUE = "PURBuild.attribute_value"
    PURBUILD_SETUP_PLANNING_UNIT = "PURBuild.setup_planning_unit"
    PURBUILD_CLEAR_PLANNING_UNIT = "PURBuild.clear_planning_unit"
    PURBUILD_ADD_PLANNING_UNIT = "PURBuild.add_planning_unit"
    PURRECONCILE_RECONCILE = "PURReconcile.reconcile"
    PURRECONCILE_UNRESOLVED_CASES = "PURReconcile.unresolved_cases"
    PURRECONCILE_ACTION = "PURReconcile.reconcile_action"
    PURLOG_LOG = "PURLog.log"
    PURLOG_HISTORY_LOG = "PURLog.history_log"
    PUR_PROCESS = "PUR.process"
    
    QUES_TITLE = "QUES.title"
    QUES_LOG = "QUES.log"
    QUES_HISTORY_LOG = "QUES.history_log"
    PREQUES_TITLE = "PreQUES.title"
    PREQUES_PARAMETERIZATION = "PreQUES.parameterization"
    PREQUES_EARLIER_LAND_USE_COVER = "PreQUES.earlier_land_use_cover"
    PREQUES_LATER_LAND_USE_COVER = "PreQUES.later_land_use_cover"
    PREQUES_PLANNING_UNIT = "PreQUES.planning_unit"
    PREQUES_LAND_USE_COVER_LOOKUP_TABLE = "PreQUES.land_use_cover_lookup_table"
    PREQUES_ANALYSIS_OPTION = "PreQUES.analysis_option"
    PREQUES_ANALYSIS_OPTION_ONE = "PreQUES.analysis_option_one"
    PREQUES_ANALYSIS_OPTION_TWO = "PreQUES.analysis_option_two"
    PREQUES_ANALYSIS_OPTION_THREE = "PreQUES.analysis_option_three"
    PREQUES_ANALYSIS_OPTION_FOUR = "PreQUES.analysis_option_four"
    PREQUES_NO_DATA_VALUE = "PreQUES.no_data_value"
    PREQUES_PROCESS = "PreQUES.process"
    QUESC_TITLE = "QUESC.title"
    QUESC_FEATURES = "QUESC.features"
    QUESC_CARBON_ACCOUNTING = "QUESC.carbon_accounting"
    QUESC_EMISSION_FROM_LAND_USE_CHANGE = "QUESC.emission_from_land_use_change"
    QUESC_EARLIER_LAND_USE_COVER = "QUESC.earlier_land_use_cover"
    QUESC_LATER_LAND_USE_COVER = "QUESC.later_land_use_cover"
    QUESC_PLANNING_UNIT = "QUESC.planning_unit"
    QUESC_CARBON_STOCK_LOOKUP_TABLE = "QUESC.carbon_stock_lookup_table"
    QUESC_NO_DATA_VALUE = "QUESC.no_data_value"
    QUESC_INCLUDE_PEAT_EMISSION = "QUESC.include_peat_emission"
    QUESC_PEAT_EMISSION_LOOKUP_TABLE = "QUESC.peat_emission_lookup_table"
    QUESC_PEAT_MAP = "QUESC.peat_map"
    QUESC_LOAD = "QUESC.load"
    QUESC_SUMMARIZE_MULTIPLE_PERIOD = "QUESC.summarize_multiple_period"
    QUESC_CALCULATE_SUMMARIZE_MULTIPLE_PERIOD = "QUESC.calculate_summarize_multiple_period"
    QUESC_PROCESS = "QUESC.process"
    QUESB_TITLE = "QUESB.title"
    QUESB_PARAMETERIZATION = "QUESB.parameterization"
    QUESB_EARLIER_LAND_USE_COVER = "QUESB.earlier_land_use_cover"
    QUESB_LATER_LAND_USE_COVER = "QUESB.later_land_use_cover"
    QUESB_INTACT_FOCAL_AREA = "QUESB.intact_focal_area"
    QUESB_PLANNING_UNIT = "QUESB.planning_unit"
    QUESB_NO_DATA_VALUE = "QUESB.no_data_value"
    QUESB_EDGE_CONTRAST_WEIGHT = "QUESB.edge_contrast_weight"
    QUESB_FOCAL_AREA_CLASS = "QUESB.focal_area_class"
    QUESB_LOAD = "QUESB.load"
    QUESB_MOVING_WINDOW = "QUESB.moving_window"
    QUESB_SHAPE_SQUARE = "QUESB.shape_square"
    QUESB_SHAPE_CIRCLE = "QUESB.shape_circle"
    QUESB_SIZE = "QUESB.size"
    QUESB_ADJACENT_ONLY = "QUESB.adjacent_only"
    QUESB_TRUE = "QUESB.true"
    QUESB_FALSE = "QUESB.false"
    QUESB_SAMPLING_GRID_SIZE = "QUESB.sampling_grid_size"
    
    # QUESH to be coded soon
    
    TA_TITLE = "TA.title"
    TA_LOG = "TA.log"
    TA_HISTORY_LOG = "TA.history_log"
    TAOPCOST_TITLE = "TAOpcost.title"
    TAOPCOST_FEATURES = "TAOpcost.features"
    TAOPCOST_ABACUS_OPPORTUNITY_COST = "TAOpcost.abacus_opportunity_cost"
    TAOPCOST_OPPORTUNITY_COST_CURVE = "TAOpcost.opportunity_cost_curve"
    TAOPCOST_PARAMETERIZATION = "TAOpcost.parameterization"
    TAOPCOST_PROFITABILITY_LOOKUP_TABLE = "TAOpcost.profitability_lookup_table"
    TAOPCOST_QUESC_DATABASE = "TAOpcost.quesc_database"
    TAOPCOST_COST_THRESHOLD = "TAOpcost.cost_threshold"
    TAOPCOST_OPPORTUNITY_COST_MAP = "TAOpcost.opportunity_cost_map"
    TAOPCOST_EARLIER_LAND_USE_COVER = "TAOpcost.earlier_land_use_cover"
    TAOPCOST_LATER_LAND_USE_COVER = "TAOpcost.later_land_use_cover"
    TAOPCOST_PLANNING_UNIT = "TAOpcost.planning_unit"
    TAOPCOST_CARBON_STOCK_LOOKUP_TABLE = "TAOpcost.carbon_stock_lookup_table"
    TAOPCOST_NO_DATA_VALUE = "TAOpcost.no_data_value"
    TAREGECO_TITLE = "TARegeco.title"
    TAREGECO_FEATURES = "TARegeco.features"
    TAREGECO_DESCRIPTIVE_ANALYSIS_OF_RE = "TARegeco.descriptive_analysis_of_re"
    TAREGECO_RE_SCENARIO_IMPACT = "Regional Economic Scenario Impact"
    TAREGECO_LUC_IMPACT = "Land Use Change Impact"
    TAREGECO_DESCRIPTIVE_ANALYSIS = "TARegeco.descriptive_analysis"
    TAREGECO_INITIALIZE = "TARegeco.initialize"
    TAREGECO_PARAMETERIZATION = "TARegeco.parameterization"
    TAREGECO_INTERMEDIATE_CONSUMPTION_MATRIX = "TARegeco.intermediate_consumption_matrix"
    TAREGECO_VALUE_ADDED_MATIX = "TARegeco.value_added_matix"
    TAREGECO_FINAL_CONSUMPTION_MATRIX = "TARegeco.final_consumption_matrix"
    TAREGECO_LIST_OF_ECONOMIC_SECTOR = "TARegeco.list_of_economic_sector"
    TAREGECO_LABOUR_REQUIREMENT = "TARegeco.labour_requirement"
    TAREGECO_FINANCIAL_UNIT = "TARegeco.financial_unit"
    TAREGECO_AREA_NAME = "TARegeco.area_name"
    TAREGECO_YEAR = "TARegeco.year"
    TAREGECO_LAND_REQUIREMENT_ANALYSIS = "TARegeco.land_requirement_analysis"
    TAREGECO_CURRENT_LAND_COVER_MAP = "TARegeco.current_land_cover_map"
    TAREGECO_LAND_REQUIREMENT_LOOKUP_TABLE = "TARegeco.land_requirement_lookup_table"
    TAREGECO_DESCRIPTIVE_ANALYSIS_OUTPUT = "TARegeco.descriptive_analysis_output"
    TAREGECO_REGIONAL_ECONOMY_SCENARIO = "TARegeco.regional_economy_scenario"
    TAREGECO_PERIOD = "TARegeco.period"
    TAREGECO_MULTI_PERIOD = "TARegeco.multiple_period"
    TAREGECO_SCENARIO_TYPE = "TARegeco.scenario_type"
    TAREGECO_LAND_REQUIREMENT = "TARegeco.land_requirement"
    TAREGECO_FINAL_DEMAND_SCENARIO = "TARegeco.final_demand_scenario"
    TAREGECO_FINAL_DEMAND_LOOKUP_TABLE = "TARegeco.final_demand_lookup_table"
    TAREGECO_GDP_SCENARIO = "TARegeco.gdp_scenario"
    TAREGECO_GDP_LOOKUP = "TARegeco.gdp_lookup"
    TAREGECO_LAND_USE_SCENARIO = "TARegeco.land_use_scenario"
    TAREGECO_PROJECTED_LAND_COVER_MAP = "TARegeco.projected_land_cover_map"
    
    SCIENDO_TITLE = "SCIENDO.title"
    SCIENDO_FEATURES = "TAOpcost.features"
    SCIENDO_LOG = "SCIENDO.log"
    SCIENDO_HISTORY_LOG = "SCIENDO.history_log"
    SCIENDO_LED = "SCIENDO.led"
    SCIENDO_HISTORICAL_BASELINE_PROJECTION = "SCIENDO.historical_baseline_projection"
    SCIENDO_HISTORICAL_BASELINE_ANNUAL_PROJECTION = "SCIENDO.historical_baseline_annual_projection"
    SCIENDO_DRIVERS_ANALYSIS = "SCIENDO.drivers_analysis"
    SCIENDO_HISTORICAL_BASELINE_ANALYSIS = "SCIENDO.historical_baseline_analysis"
    SCIENDO_PERIODIC_PROJECTION_PARAMETER = "SCIENDO.periodic_projection_parameter"
    SCIENDO_CONDUCT_PERIODIC_PROJECTION = "SCIENDO.conduct_periodic_projection"
    SCIENDO_QUESC_DATABASE = "SCIENDO.quesc_database"
    SCIENDO_ITERATION = "SCIENDO.iteration"
    SCIENDO_ANNUAL_PROJECTION_PARAMETER = "SCIENDO.annual_projection_parameter"
    SCIENDO_CONDUCT_ANNUAL_PROJECTION = "SCIENDO.conduct_annual_projection"
    SCIENDO_DRIVERS_ANALYSIS_PARAMETER = "SCIENDO.drivers_analysis_parameter"
    SCIENDO_DRIVERS_OF_LAND_USE_CHANGE = "SCIENDO.drivers_of_land_use_change"
    SCIENDO_LAND_USE_TRAJECTORY = "SCIENDO.land_use_trajectory"
    SCIENDO_SCENARIO_BUILDER = "SCIENDO.scenario_builder"
    SCIENDO_BUILD_SCENARIO = "SCIENDO.build_scenario"
    SCIENDO_HISTORICAL_BASELINE_DATA = "SCIENDO.historical_baseline_data"
    SCIENDO_LUCM = "SCIENDO.lucm"
    SCIENDO_LAND_USE_SIMULATION = "SCIENDO.land_use_simulation"
    SCIENDO_CALCULATE_TRANSITION_MATRIX = "SCIENDO.calculate_transition_matrix"
    SCIENDO_SETUP_INITIAL_AND_FINAL_MAP = "SCIENDO.setup_initial_and_final_map"
    SCIENDO_EARLIER_LAND_USE_COVER = "SCIENDO.earlier_land_use_cover"
    SCIENDO_LATER_LAND_USE_COVER = "SCIENDO.later_land_use_cover"
    SCIENDO_PLANNING_UNIT = "SCIENDO.planning_unit"
    SCIENDO_CREATE_FACTOR_RASTER_CUBE = "SCIENDO.create_factor_raster_cube"
    SCIENDO_LIST_FACTORS = "SCIENDO.list_factors"
    SCIENDO_SIMULATION_DIRECTORY_INDEX = "SCIENDO.simulation_directory_index"
    SCIENDO_FACTOR_DIRECTORY = "SCIENDO.factor_directory"
    SCIENDO_CALCULATE_WEIGHT_OF_EVIDENCE = "SCIENDO.calculate_weight_of_evidence"
    SCIENDO_LAND_COVER_LOOKUP_TABLE = "SCIENDO.land_cover_lookup_table"
    SCIENDO_SIMULATE_LAND_USE = "SCIENDO.simulate_land_use"
    SCIENDO_SIMULATE_WITH_SCENARIO = "SCIENDO.simulate_with_scenario"
    SCIENDO_PARAMETERIZATION = "SCIENDO.parameterization"
    
    CONF_TITLE = "Configuration.title"
    CONF_LOADED_CONFIGURATION = "Configuraton.loaded_configuration"
    CONF_NONE = "Configuration.none"
    CONF_NAME = "Configuration.name"
    CONF_NO_FOUND = "Configuration.no_found"
    CONF_LOAD = "Configuration.load"
    CONF_SAVE = "Configuration.save"
    CONF_SAVE_AS = "Configuration.save_as"
    CONF_LOAD_EXISTING_CONFIGURATION = "Configuration.load_existing_configuration"
    CONF_TEMPLATE = "Configuration.template"
    CONF_TEMPLATE_NAME = "Configuration.template_name"
    CONF_NO_TEMPLATE_FOUND = "Configuration.no_template_found"
    CONF_LOAD_TEMPLATE = "Configuration.load_template"
    CONF_SAVE_TEMPLATE = "Configuration.save_template"
    CONF_SAVE_AS_TEMPATE = "Configuration.save_as_tempate"
    CONF_PROCESS = "Configuration.process"
    CONF_CONFIGURE = "Configuration.configure"
    
    MSG_ERROR = "Message.error"
    MSG_PROCESS_TEMPLATE = "Message.process_template"
    MSG_APP_SAVE_LAYER = "Message.app_save_layer"
    MSG_APP_DELETE_ALL_STYLE = "Message.app_delete_all_style"
    MSG_APP_DELETE_FEATURE = "Message.app_delete_feature"
    MSG_APP_INVALID_WORKING_DIRECTORY = "Message.app_invalid_working_directory"
    MSG_APP_INVALID_LUMENS_PROJECT = "Message.app_invalid_lumens_project"
    MSG_APP_HELP_NOT_FOUND = "Message.app_help_not_found"
    MSG_APP_GUIDE_NOT_FOUND = "Message.app_guide_not_found"
    MGS_APP_SELECT_DATA_MAPPING_FILE = "Message.app_select_data_mapping_file"
    MSG_APP_RESULT_SUCCESS = "Message.app_result_success" 
    MSG_APP_RESULT_ERROR = "Message.app_result_error"
    MSG_DB_SELECT_OUTPUT_FOLDER = "Message.db_select_output_folder"
    MSG_DB_SELECT_SHAPEFILE = "Message.db_select_shapefile"
    MSG_DB_INVALID_DISSOLVED_TABLE = "Message.db_invalid_dissolved_table"
    MSG_DB_SUCCESS_CREATED = "Message.db_success_created"
    MSG_DB_FAILED_CREATED = "Message.db_failed_created"
    MSG_DB_FAILED_OPENED = "Message.db_failed_opened"
    MSG_DB_HTML_REPORT = "Message.db_html_report"
    MSG_DB_CHOOSE_DATA_TO_BE_DELETED = "Message.db_choose_data_to_be_delete"
    MSG_DB_SUCCESS_ADDED = "Message.db_success_added"
    MSG_DB_FAILED_ADDED = "Message.db_failed_added"
    MSG_PUR_SETUP_RUN_SUCCESS = "Message.pur_setup_run_success"
    MSG_PUR_RECONCILE_RUN_SUCCESS = "Message.pur_reconcile_run_success"
    MSG_PUR_DUPLICATE_REFERENCE = "Message.pur_duplicate_reference" 
    MSG_PUR_EMPTY_REFERENCE = "Message.pur_empty_reference_title" 
    MSG_PUR_NON_NUMBER_REFERENCE = "Message.pur_non_number_reference_id" 
    MSG_PUR_NO_REFERENCE_FOUND = "Message.pur_no_reference_found"
    MSG_QUES_CHOOSE_QUESC_DB = "Message.ques_choose_quesc_db"
    MSG_QUES_SELECT_FOCAL_AREA = "Message.ques_select_focal_area"
    MSG_TA_SELECT_LAND_REQUIREMENT = "Message.ta_select_land_requirement"
    MSG_SCIENDO_NO_QUESC_DB = "Message.sciendo_no_quesc_db"
    MSG_SCIENDO_SELECT_LAND_USE_DRIVERS = "Message.sciendo_select_land_use_drivers"
    MSG_SCIENDO_SELECT_HISTORICAL_BASELINE_CAR = "Message.sciendo_select_historical_baseline_car"
    MSG_SCIENDO_SELECT_FACTORS_DIR = "Message.sciendo_select_factors_dir"
    MSG_SCIENDO_SELECT_LAND_USE_LOOKUP_TABLE = "Message.sciendo_select_land_use_lookup_table"
    MSG_SCIENDO_CHOOSE_QUESC_DB = "Message.sciendo_choose_quesc_db" 
    
    menuProperties = {}
    
    @staticmethod
    def setMenuProperties(filename, lang):
        if not os.path.isfile(filename):
            return
        
        if lang == 'vn':
            lines = io.open(filename, encoding='utf-16-le', errors='ignore')
        else:
            lines = open(filename)
        
        line = lines.readline().strip('\n')
        while line != '':
            tokens = line.split('=')
            MenuFactory.menuProperties[tokens[0]] = tokens[1]
            line = lines.readline().strip('\n')
        lines.close()
        
        
    @staticmethod    
    def getLabel(name):
        name = name + '_label'
        if name in MenuFactory.menuProperties.keys():
            return MenuFactory.menuProperties[name]
        else:
            return None
        
        
    @staticmethod    
    def getDescription(description):
        description = description + '_description'
        if description in MenuFactory.menuProperties.keys():
            return MenuFactory.menuProperties[description]
        else:
            return None
    
    
# class MenuProperty:
#     """The property of menu.
#     """
# 
#     def __init__(self, label, description=''):
#         self.label = label
#         self.description = description
        
