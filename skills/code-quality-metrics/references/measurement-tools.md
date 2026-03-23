# Code Quality Measurement Tools

## TypeScript / JavaScript

### ESLint Complexity Rules

Configuration in `.eslintrc.json`:
```json
{
  "rules": {
    "complexity": ["error", { "max": 10 }],
    "max-depth": ["error", { "max": 4 }],
    "max-lines": ["error", { "max": 300 }],
    "max-lines-per-function": ["error", { "max": 50 }],
    "max-params": ["error", { "max": 4 }],
    "max-nested-callbacks": ["error", { "max": 3 }],
    "max-statements": ["error", { "max": 15 }]
  }
}
```

### SonarQube / SonarCloud

`sonar-project.properties`:
```properties
sonar.projectKey=my-project
sonar.sources=src
sonar.exclusions=**/node_modules/**,**/*.test.ts

# Thresholds
sonar.javascript.lcov.reportPaths=coverage/lcov.info
sonar.coverage.exclusions=**/*.test.ts,**/*.spec.ts
```

Run analysis:
```bash
npx sonar-scanner
```

### Code Climate

`.codeclimate.yml`:
```yaml
version: "2"
checks:
  method-complexity:
    config:
      threshold: 10
  method-lines:
    config:
      threshold: 30
  file-lines:
    config:
      threshold: 300

plugins:
  eslint:
    enabled: true
  duplication:
    enabled: true
    config:
      languages:
        javascript:
          mass_threshold: 40
```

---

## Java

### Checkstyle

`checkstyle.xml`:
```xml
<?xml version="1.0"?>
<!DOCTYPE module PUBLIC "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
  "https://checkstyle.org/dtds/configuration_1_3.dtd">
<module name="Checker">
  <module name="TreeWalker">
    <module name="CyclomaticComplexity">
      <property name="max" value="10"/>
    </module>
    <module name="MethodLength">
      <property name="max" value="50"/>
    </module>
    <module name="ParameterNumber">
      <property name="max" value="4"/>
    </module>
    <module name="NestedIfDepth">
      <property name="max" value="3"/>
    </module>
    <module name="ClassFanOutComplexity">
      <property name="max" value="20"/>
    </module>
  </module>
  <module name="FileLength">
    <property name="max" value="500"/>
  </module>
</module>
```

### SpotBugs + FindSecBugs

`pom.xml`:
```xml
<plugin>
  <groupId>com.github.spotbugs</groupId>
  <artifactId>spotbugs-maven-plugin</artifactId>
  <version>4.7.3.0</version>
  <configuration>
    <effort>Max</effort>
    <threshold>Low</threshold>
    <plugins>
      <plugin>
        <groupId>com.h3xstream.findsecbugs</groupId>
        <artifactId>findsecbugs-plugin</artifactId>
        <version>1.12.0</version>
      </plugin>
    </plugins>
  </configuration>
</plugin>
```

Run:
```bash
mvn spotbugs:check
```

---

## Python

### Radon

Install and run:
```bash
pip install radon

# Cyclomatic complexity
radon cc src/ -a -s

# Maintainability index
radon mi src/ -s

# Raw metrics (LOC, comments, etc.)
radon raw src/ -s

# Halstead metrics
radon hal src/
```

Output example:
```
src/module.py
    F 10:0 function_name - C (11)  # Cyclomatic = 11, Grade C
    C 25:0 ClassName - B (8)       # Cyclomatic = 8, Grade B
```

### Pylint

`.pylintrc`:
```ini
[DESIGN]
max-args=5
max-locals=15
max-returns=6
max-branches=12
max-statements=50
max-parents=7
max-attributes=7
max-public-methods=20

[FORMAT]
max-line-length=120
max-module-lines=1000
```

### Flake8 + Cognitive Complexity

```bash
pip install flake8 flake8-cognitive-complexity

# .flake8
[flake8]
max-cognitive-complexity = 15
max-complexity = 10
max-line-length = 120
```

---

## Go

### gocyclo

```bash
go install github.com/fzipp/gocyclo/cmd/gocyclo@latest
gocyclo -over 10 .
```

### golangci-lint

`.golangci.yml`:
```yaml
linters:
  enable:
    - gocyclo
    - gocognit
    - funlen
    - dupl

linters-settings:
  gocyclo:
    min-complexity: 10
  gocognit:
    min-complexity: 15
  funlen:
    lines: 60
    statements: 40
  dupl:
    threshold: 100
```

Run:
```bash
golangci-lint run
```

---

## PHP

### PHP_CodeSniffer + PHPStan

```bash
composer require --dev squizlabs/php_codesniffer phpstan/phpstan

# phpcs.xml
<?xml version="1.0"?>
<ruleset>
  <rule ref="Generic.Metrics.CyclomaticComplexity">
    <properties>
      <property name="complexity" value="10"/>
      <property name="absoluteComplexity" value="20"/>
    </properties>
  </rule>
  <rule ref="Generic.Metrics.NestingLevel">
    <properties>
      <property name="nestingLevel" value="4"/>
      <property name="absoluteNestingLevel" value="6"/>
    </properties>
  </rule>
  <rule ref="Generic.Files.LineLength">
    <properties>
      <property name="lineLimit" value="120"/>
    </properties>
  </rule>
</ruleset>
```

### PHPMD (Mess Detector)

```xml
<!-- phpmd.xml -->
<ruleset>
  <rule ref="rulesets/codesize.xml">
    <exclude name="TooManyPublicMethods"/>
  </rule>
  <rule ref="rulesets/codesize.xml/CyclomaticComplexity">
    <properties>
      <property name="reportLevel" value="10"/>
    </properties>
  </rule>
</ruleset>
```

---

## Lua

### luacheck

`.luacheckrc`:
```lua
max_line_length = 120
max_cyclomatic_complexity = 10

stds.lua51 = {
   read_globals = {"table", "string", "math", "io", "os"}
}
```

### luacov (Coverage)

```bash
lua -lluacov script.lua
luacov
```

---

## Universal Tools

### SonarQube

Supports all listed languages. Self-hosted or SonarCloud.

```bash
# Docker setup
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest
```

### Codacy

Cloud-based analysis supporting multiple languages. Configure via `.codacy.yml`:

```yaml
engines:
  eslint:
    enabled: true
  pylint:
    enabled: true

languages:
  typescript:
    extensions:
      - ts
      - tsx
  python:
    extensions:
      - py
```

---

## CI/CD Integration

### GitHub Actions

```yaml
- name: Run Code Quality Checks
  run: |
    npx eslint src/ --max-warnings 0
    npx sonar-scanner

- name: Check Complexity Thresholds
  run: |
    # Fail if any function exceeds complexity 15
    npx eslint src/ --rule 'complexity: ["error", 15]'
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: complexity-check
        name: Check Cyclomatic Complexity
        entry: npx eslint --rule 'complexity: ["error", 10]'
        language: system
        types: [typescript]
```
