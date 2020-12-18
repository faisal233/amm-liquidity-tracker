from swagger_tester import swagger_test

authorize_error = {
    "put": {"/api/tokens": [400, 404], "/api/tokens/{token_id}": [400, 404]},
    "post": {"/api/tokens": [400, 404], "/api/tokens/{token_id}": [400, 404]},
    "get": {"/api/tokens": [400, 404, 500], "/api/tokens/{token_id}": [400, 404, 500]},
    "delete": {"/api/tokens": [400, 404, 500], "/api/tokens/{token_id}": [400, 404, 500]},
}


def test_swagger():
    swagger_test("liquidity-tracker/swagger.yml",
                 authorize_error=authorize_error)
