# Simple Expression Calculator CLI

def main():
    print("Welcome to Simple Expression Calculator!")
    print("You can type expressions like: 2 + 3 * 4, 10 / 2, (5 + 3) * 2")
    print("Type 'exit' to quit.\n")

    while True:
        expr = input("calc> ")

        if expr.lower() == "exit":
            print("Goodbye!")
            break

        try:
            # Evaluate expression safely
            allowed_names = {"abs": abs, "round": round}
            result = eval(expr, {"__builtins__": None}, allowed_names)
            print("Result:", result)
        except ZeroDivisionError:
            print("Error: Division by zero is not allowed.")
        except Exception:
            print("Invalid expression. Please try again.")

if __name__ == "__main__":
    main()