# Minimal CLI Todo Tracker

A simple command-line todo tracker that stores todos in a JSON file.

## Features

- Add new todos
- List all todos
- Mark todos as complete
- Delete todos

## Usage

### Add a new todo
```bash
python main.py add "Buy groceries"
```

### List all todos
```bash
python main.py list
```

### Complete a todo
```bash
python main.py complete 1
```

### Delete a todo
```bash
python main.py delete 1
```

## How it works

Todos are stored in a `todos.json` file in the same directory as the script. Each todo has:
- An ID (auto-generated)
- The todo item text
- Completion status
- Creation timestamp

## Requirements

- Python 3.x

## Example session

```bash
$ python main.py add "Buy groceries"
Added todo: Buy groceries

$ python main.py add "Walk the dog"
Added todo: Walk the dog

$ python main.py list
Todos:
  [○] 1: Buy groceries
  [○] 2: Walk the dog

$ python main.py complete 1
Completed todo 1: Buy groceries

$ python main.py list
Todos:
  [✓] 1: Buy groceries
  [○] 2: Walk the dog
```