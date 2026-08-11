import importlib


def get_constants(survey_stage):
    module_name = f"constants.stage_{survey_stage}"
    return importlib.import_module(module_name)
