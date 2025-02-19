


def csv_to_dict(path):
    """Function to read in CSV, saves as a dictionary.Keys are titles, the data is stored in a list"""

    game_dict = {}

    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

        # skip headers and begin processing
        for line in lines[1:]:
            data = line.strip().split(",")

            # first is title
            title = data[0]

            # rest is info
            information = data[1:]

            # assign each dictionary entry
            game_dict[title] = information



    return game_dict


print(csv_to_dict(r"C:\Users\dawso\OneDrive\Desktop\Web Scraper V1\gameInfo.csv"))