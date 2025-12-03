# app/services/validator.py
# --------------------------------------------------------------------
# Validates PipelineSchema config.
# --------------------------------------------------------------------

def validate_pipeline_config(cfg: dict):
    if cfg.get("scaling") not in [None, "standard", "minmax"]:
        raise ValueError("Invalid scaling method")
    return True
