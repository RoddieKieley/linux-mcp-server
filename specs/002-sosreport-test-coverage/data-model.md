# Data Model: Sosreport Test Coverage

## Entity: GenerationScenario

- **Purpose**: Represents one deterministic `generate_sosreport` behavior under test.
- **Fields**:
  - `name` (string): scenario identifier.
  - `inputs` (object): host and generation options supplied to the tool.
  - `mock_command_results` (ordered list): simulated command outcomes for version/generate/fallback/stat calls.
  - `expected_result` (object): expected structured content values on success.
  - `expected_error` (string, optional): expected error fragment on failure.
  - `fr_ids` (list[string]): mapped functional requirement identifiers.
  - `sc_ids` (list[string]): mapped success criteria identifiers.
- **Validation Rules**:
  - `mock_command_results` order must align with expected command call sequence.
  - Success scenarios require `expected_result`; failure scenarios require `expected_error`.

## Entity: RetrievalScenario

- **Purpose**: Represents one deterministic `fetch_sosreport` behavior under test.
- **Fields**:
  - `name` (string): scenario identifier.
  - `fetch_reference` (string): archive reference input.
  - `mock_read_result` (bytes/tuple/error): simulated privileged read outcome.
  - `expected_archive_path` (string, optional): local path expectation for success.
  - `expected_size_bytes` (int, optional): expected byte count for success.
  - `expected_sha256` (string, optional): expected checksum for success.
  - `expected_error` (string, optional): expected error fragment for failure.
  - `fr_ids` (list[string]): mapped functional requirement identifiers.
  - `sc_ids` (list[string]): mapped success criteria identifiers.
- **Validation Rules**:
  - Success scenarios require both `expected_size_bytes` and `expected_sha256`.
  - Failure scenarios require deterministic `expected_error`.

## Entity: OptionValidationCase

- **Purpose**: Captures valid and invalid option/input contracts.
- **Fields**:
  - `name` (string): case identifier.
  - `tool` (enum): `generate_sosreport` or `fetch_sosreport`.
  - `arguments` (object): input payload being validated.
  - `expected_valid` (bool): pass/fail expectation.
  - `expected_message` (string, optional): validation error fragment when invalid.
  - `fr_ids` (list[string]): mapped functional requirement identifiers.
- **Validation Rules**:
  - Invalid cases must assert no downstream command execution.
  - Valid cases must preserve effective option values in returned structured output.

## Relationships

- One `GenerationScenario` may include multiple `OptionValidationCase` rows.
- One `RetrievalScenario` may include one integrity assertion set (`size`, `sha256`) for success.
- All scenario entities include FR/SC linkage for coverage traceability.
