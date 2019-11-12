from battlefield import Battlefield


def main():

    try:
        log_type = int(input(f"1 - Print the results to the console.\n"
                             f"2 - Print the results to the file.\n"))

        if log_type == 1:
            battle = Battlefield(log_type)

        elif log_type == 2:
            logfile = input("File for print: ")
            battle = Battlefield(log_type, logfile)

        else:
            raise ValueError("Incorrect input")

        battle.start()

    except ValueError:
        print("Incorrect input")


if __name__ == "__main__":
    main()
