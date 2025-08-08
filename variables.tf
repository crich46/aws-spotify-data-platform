# declare all input vars ex: spotify client IDs

variable "spotify_client_id" {
  description = "Spotify API Client ID"
  type = string
  sensitive = true
}

variable "spotify_client_secret" {
  description = "Spotify API Client Secret"
  type = string
  sensitive = true
}

variable "region" {
  description = "AWS region that resources will be created in"
  type = string
  sensitive = false
}
