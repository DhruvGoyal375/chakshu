# Contribution Guidelines

We welcome contributions from the community! To ensure a smooth process, please follow these guidelines:

### Fork the Repository

1. Fork the repository on GitHub by clicking the "Fork" button on the upper right corner of the repository page.

### Clone Your Fork

2. Clone your forked repository to your local machine:

```sh
git clone https://github.com/DhruvGoyal375/chakshu.git
cd chakshu
```

### Create a Branch

3. Create a new branch for your feature or bugfix:

```sh
git checkout -b my-feature-branch
```

### Set up Virtual Environment

4. Set up Poetry to create virtual environments within the project directory:

```sh
pip install poetry
poetry config virtualenvs.in-project true
```

5. Install dependencies using Poetry:

```sh
poetry install
```

6. Activate the virtual environment:

```sh
poetry shell
```

### Make Your Changes

7. Make your changes in the codebase. Be sure to follow the existing coding style and conventions.

### Code Formatting

8. We use [Ruff](https://github.com/charliermarsh/ruff) for code formatting. Ensure your code is properly formatted before committing.

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

9. Commit your changes with a descriptive commit message:

```sh
git add .
git commit -m "Description of your changes"
```

### Push Your Changes

10. Push your changes to your forked repository:

```sh
git push origin my-feature-branch
```

### Create a Pull Request

11. Open a pull request on the main repository. Provide a clear and detailed description of your changes and why they are necessary.

### Code Review

12. Your pull request will be reviewed by the maintainers. Please address any feedback and make necessary changes.
