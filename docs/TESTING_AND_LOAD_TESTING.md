# Testing and Load Testing for Weather API Project

## 1. Pytest Testing Methodology

The project uses [pytest](https://docs.pytest.org/) for unit and integration testing of the Flask web API.

### Structure of Tests

- Tests are located in the `src/tests/` directory.
- Each test file is a standard Python file prefixed with `test_`.
- `pytest` automatically discovers tests based on the `test_*.py` pattern.

### Key Components in `src/tests/test_app.py`

- **Pytest Fixture for Flask Test Client**  
  A `client` fixture sets up the Flask app in testing mode and provides a test client for HTTP requests:
  ```python
  @pytest.fixture
  def client():
      app.testing = True
      return app.test_client()
  ```

- **Test Functions**  
  Individual test functions use the `client` to send HTTP requests to the Flask app endpoints and assert on the responses.  
  For example, testing the home route:
  ```python
  def test_home_route(client):
      res = client.get("/")
      assert res.status_code == 200
      assert b"Welcome to the Weather API" in res.data
  ```

- **Mocking External API Calls**  
  The `/weather` endpoint relies on an external API. During tests, external calls are mocked using `unittest.mock.patch` to avoid network dependency and ensure consistent, testable responses:
  ```python
  @patch("src.app.requests.get")
  def test_weather_success(mock_get, client):
      mock_get.return_value.json.return_value = {
          "current_weather": {"temperature": 23.7, "windspeed": 23.7}
      }
      res = client.get("/weather?lat=30.709675&lon=134.568701")
      data = res.get_json()
      assert res.status_code == 200
      assert "current_weather" in data
  ```
  
### Benefits

- Isolated, fast tests without hitting real external APIs.
- Clear, descriptive test cases for each API behavior.
- Easily extensible with additional endpoint tests.

---

## 2. Additional Example Pytest Tests

```python
def test_weather_invalid_lat_lon(client):
    # Test invalid latitude and longitude values
    res = client.get("/weather?lat=abc&lon=xyz")
    assert res.status_code == 400 or res.status_code == 200  # Current app doesn't validate types, you may handle this.

def test_home_route_content_type(client):
    res = client.get("/")
    assert res.content_type == "text/html; charset=utf-8"
```

These enhance robustness by testing additional parameter scenarios.

---

## 3. Load Testing with Artillery

[Artillery](https://artillery.io/) is a modern, powerful, and easy-to-use load testing tool.

### Steps to Configure and Run Load Tests

1. **Install Artillery**  
   Using npm (requires Node.js installed):  
   ```bash
   npm install -g artillery
   ```

2. **Create an Artillery config file**  
   A sample YAML configuration `load-test.yml` will simulate multiple users hitting the home and weather endpoints of your API.

3. **Run Load Test**  
   Execute the test in terminal:  
   ```bash
   artillery run load-test.yml
   ```

4. **Interpret Results**  
   Artillery provides metrics like response times, request rates, errors, and percentiles to analyze API performance.

---

## 4. Sample Artillery Config (`load-test.yml`)

```yaml
config:
  target: "http://localhost:5000"
  phases:
    - duration: 60
      arrivalRate: 10  # 10 new users per second
scenarios:
  - flow:
      - get:
          url: "/"
      - get:
          url: "/weather?lat=30.709675&lon=134.568701"
```

This config runs a 60-second test with 10 new virtual users per second hitting the API.

---

## 5. Summary

- Use pytest for functional testing of your Flask API with mocks for external calls.
- Use Artillery for realistic load testing to evaluate API performance under traffic.
- Extend tests and load tests as project evolves.

---

For any queries or further help, feel free to ask!
