provider "docker" {
  host = "unix:///var/run/docker.sock"
}
# Pulls the image
resource "docker_image" "alpine" {
  name = "alpine:latest"
}
# Create a container
resource "docker_container" "alpine-test" {
  image = docker_image.alpine.image_id
 name  = "alpine-test"
must_run = true
 command = [ "tail",
    "-f",
    "/dev/null"
 ]
}