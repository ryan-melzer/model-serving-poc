locals {
  # Do not remove these basic tags.  
  # You may add additioanl tags here if relevant to the entire workspace
  default_tags = {
    "eo:ops:creator"      = "terraform"
    "eo:ops:environment"  = var.environment
    "terraform:git-repo"  = var.tf_workspace_repo
    "terraform:workspace" = var.TFC_WORKSPACE_NAME
  }
}
