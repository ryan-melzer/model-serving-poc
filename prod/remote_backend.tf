terraform {
  backend "remote" {
    organization = "upwork"
    hostname     = "tfe.upwork-internal.com"

    ## The workspace name is the name of the workspace in Terraform Cloud
    # workspaces {
    #   name = ""
    # }
  }
}
