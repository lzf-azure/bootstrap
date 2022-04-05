# test the PAT
curl -i -u $GH_USERNAME:$GH_PAT https://api.github.com/user

# manually run a workspace
cat << EOF > data.json
{
  "data": {
    "attributes": {
      "message": "Just a test run"
    },
    "type":"runs",
    "relationships": {
      "workspace": {
        "data": {
          "type": "workspaces",
          "id": "ws-md6DDdEqDpJQ4c12"
        }
      }
    }
  }
}
EOF

curl -vk \
  --header "Authorization: Bearer $TFE_USER_TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  --request POST \
  --data @./data.json \
  https://app.terraform.io/api/v2/runs
