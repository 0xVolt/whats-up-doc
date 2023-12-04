import typer

app = typer.Typer()


@app.command()
def hello():
    print("This is a test function. Hello!")


@app.command()
def goodbye():
    print("This is another test function. Goodbye!")


if __name__ == "__main__":
    app()