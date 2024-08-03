# Contribution Guidelines

We welcome contributions from the community! To ensure a smooth process, please follow these guidelines:

### Prerequisites

Make sure you have the following installed on your machine:

- [Python 3.10+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)

### Fork the Repository

Fork the repository on GitHub by clicking the "Fork" button on the upper right corner of the repository page.

### Clone Your Fork

Clone your forked repository to your local machine:

```sh
git clone https://github.com/DhruvGoyal375/chakshu.git
cd chakshu
```

### Create a Branch

Create a new branch for your feature or bugfix:

```sh
git checkout -b my-feature-branch
```

### Set up Virtual Environment

Set up Poetry to create virtual environments within the project directory:

```sh
pip install poetry
poetry config virtualenvs.in-project true
```

Install dependencies using Poetry:

```sh
poetry install
```

Activate the virtual environment:

```sh
poetry shell
```

### Make Your Changes

Make your changes in the codebase. Be sure to follow the existing coding style and conventions.

### Code Formatting

We use [Ruff](https://github.com/charliermarsh/ruff) for code formatting. Ensure your code is properly formatted before committing.

- **Option 1: Install the Ruff extension in your code editor.**
- **Option 2: Use Ruff commands in the terminal:**

  <br>

  - Check code for formatting issues:

  ```sh
  ruff check
  ```

  This command will analyze your code and report any formatting issues.
  
  <br>

  - Automatically format your code:

  ```sh
  ruff format
  ```

  This command will automatically format your code to meet the project's standards.

### Commit Your Changes

Commit your changes with a descriptive commit message:

```sh
git add .
git commit -m "Description of your changes"
```

### Push Your Changes

Push your changes to your forked repository:

```sh
git push origin my-feature-branch
```

### Create a Pull Request

Open a pull request on the main repository. Provide a clear and detailed description of your changes and why they are necessary.

### Code Review

Your pull request will be reviewed by the maintainers. Please address any feedback and make necessary changes.
