import typer

app = typer.Typer()


# Create a decorator for our command
@app.command()
# Note: All arguments are required but those with default values aren't
def generate(file: str, useDefault: bool = True):
    print(f"Here's the file you'd passed in: {file}")
    print(f"Here's the value of the useDefault flag: {useDefault}")


@app.command()
def testCommand():
    print("This is a test command! Just placeholder, nothing to see here ://")


if __name__ == "__main__":
    app()