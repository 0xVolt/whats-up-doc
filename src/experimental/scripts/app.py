import typer

app = typer.Typer()


# Create a decorator for our command
@app.command()
def hello(name: str, num: int):
    print(f"This is a test function. Hello {name}!")
    print(f"Your lucky number is: {num}")


@app.command()
def goodbye():
    print("This is another test function. Goodbye!")


if __name__ == "__main__":
    app()