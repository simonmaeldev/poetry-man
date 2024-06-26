# Poetry Man

Poetry Man is a Python project that helps manage poetry projects using the Poetry package manager. It provides an interactive interface to handle various Poetry-related tasks.

## Purpose

The main purpose of this project is to simplify the process of creating, managing, and publishing Python projects using Poetry. It offers a conversational interface that guides users through common Poetry operations.

## Installation

To install Poetry Man, follow these steps:

1. Ensure you have Python 3.7+ installed on your system.
2. Install Poetry if you haven't already:
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Clone this repository:
   ```
   git clone https://github.com/yourusername/poetry-man.git
   cd poetry-man
   ```
4. Install the project dependencies:
   ```
   poetry install
   ```

## Running the Project

To run Poetry Man:

1. Activate the virtual environment:
   ```
   poetry shell
   ```
2. Run the main script:
   ```
   python poetry_man/main.py
   ```

Follow the prompts to interact with the Poetry Man assistant and manage your Poetry projects.

## Configuration

Make sure to set your Anthropic API key in the `.env` file:

```
ANTHROPIC_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual Anthropic API key.
