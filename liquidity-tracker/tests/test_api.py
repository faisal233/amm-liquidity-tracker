from swagger_tester import swagger_test

authorize_error = {
    "put": {"/api/tokens": [400, 404], "/api/tokens/{token_id}": [400, 404]},
    "post": {"/api/tokens": [400, 404], "/api/tokens/{token_id}": [400, 404]},
    "get": {"/api/tokens": [400, 404], "/api/tokens/{token_id}": [400, 404]},
    "delete": {"/api/tokens": [400, 404], "/api/tokens/{token_id}": [400, 404]},
}


def test_swagger():
    swagger_test("swagger.yml", authorize_error=authorize_error)
