resource "local_file" "example" {
  filename = "${path.module}/hello.txt"
  content  = "Hello Terraform"
}
