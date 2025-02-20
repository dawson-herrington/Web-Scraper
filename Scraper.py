import urllib.request
from html.parser import HTMLParser




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

def dict_to_csv(path, dict):

    # headers are static
    headers = ["title", "folder", "review", "metacriticScore", "platform", "completionTime"]


    with open(path, "w", encoding="utf-8") as file:
        # add headers back
        file.write(",".join(headers)+"\n")

        # write entries
        for title, data in dict.items():
            row = [title] + data
            file.write(",".join(row)+"\n")


def get_platforms(html):
    try:
        # platforms
        # locate platform
        # precedes platforms <div class="number color5">
        platforms_list = []
        platform_key = '<span class="detail-content">'
        index = html.find(platform_key)

        if index != -1:
            # emergency end
            # find end of element
            end = html.find('</span>', index)
            platform_element = html[index: end]

            while '<a href="' in platform_element:
                # locate next a href to find platform name
                start = platform_element.find('>', platform_element.find('<a href="')) + 1

                # find where name ends
                end = platform_element.find('</a>', start)

                # check if we hit end
                if end == -1:
                    break

                # get and format
                platform = platform_element[start:end].strip()

                # add to platform llist
                platforms_list.append(platform)

                # remove what we looked at
                platform_element = platform_element[end + 4:]

            platforms = "- ".join(platforms_list)

            return platforms
    except:
        print("Platform error: No Data Found")

def get_score(html):
    try:
        # locate review
        # precedes review <div class="number color5">
        review_key = '<div class="number color5">'
        index = html.find(review_key)

        # review found
        if index != -1:
            # look just after key
            start_index = index + len(review_key)
            review_score = html[start_index:start_index + 3]  # Next 3 characters

            # format
            if '.' not in review_score:
                review_score = review_score[0:2]
        else:
            review_score = "No Review Data Found"

            # locate review
            # precedes review <div class="number color5">
            review_key = '<div class="number color5">'
            index = html.find(review_key)

            # review found
            if index != -1:
                # look just after key
                start_index = index + len(review_key)
                review_score = html[start_index:start_index + 3]  # Next 3 characters

                # format
                if '.' not in review_score:
                    review_score = review_score[0:2]
            else:
                review_score = "No Review Data Found"

        return review_score
    except:
        print("Review Error: No Data Found")

def get_developer(html):
    try:
        # start search here
        dev_key = '<a href="https://www.godisageek.com/reviews-developer/'
        index = html.find(dev_key)

        if index != -1:
            start = html.find('>', index) + 1
            end = html.find('</a>', start)

            if end != -1:
                developer = html[start:end].strip()

        return developer
    except:
        print("Developer Error: No Data Found")

def get_all_data(dict):
    for title, data in dict.items():
        # format title
        formatted_title = title.replace(":","").replace(" ", "-").lower()
        print(formatted_title)
        # generate url
        url = f"https://www.godisageek.com/reviews/{formatted_title}-review/"
        print(url)

        # grab html data
        try:
            response = urllib.request.urlopen(url)
            html = response.read().decode("utf-8")

            # review score
            try:
                review_score = get_score(html)
            except:
                print("No Data Found - Verify spelling")
                review_score = "No Data"

            # paltform info
            try:
                platforms = get_platforms(html)
            except:
                print("No Data Found - Verify spelling")
                platforms = "No Data"

            # dev data
            try:
                developer = get_developer(html)
            except:
                print("No Data Found - Verify spelling")
                developer = "No Data"

            # populate dictionary
            dict[title][2] = review_score
            dict[title][3] = platforms
            dict[title][4] = developer

        except:
            print("Error: Could not find HTML data")

            # populate dictionary
            dict[title][2] = "No Data"
            dict[title][3] = "No Data"
            dict[title][4] = "No Data"





    return dict


# actual calls made below

# update with path to the CSV

# create dictionary from csv
originaal_dictionary = csv_to_dict(r"C:\Users\dawso\OneDrive\Desktop\Web Scraper V1\gameInfo.csv")

# make call to scraper
return_dictionary = get_all_data(originaal_dictionary)

# update with path to csv
# write to file
dict_to_csv(r"C:\Users\dawso\OneDrive\Desktop\Web Scraper V1\gameInfo.csv", return_dictionary)