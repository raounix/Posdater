from pick import pick
import json
import medium
from print_color import print

def show_other_blogs():
    data_file = open('./db/blogs.json',"r")
    blogs_list = json.load(data_file)
    for number,blog in enumerate(blogs_list['urls']):
        print("{} - {}".format(number+1,blog), color='green', background='grey')
if __name__ == "__main__":
    title = 'Select Option: '
    options = ['Medium Updates','Add Medium Account','Add Medium Topic','Other Blogs','Exit']

    option, index = pick(options, title, indicator='=>')
    if (index == 0):
        options = ['Accounts','Topics','Exit']
        option, index = pick(options, title, indicator='=>')
        if (index == 0):
            medium.update_medium("account")
        elif (index == 1):
            medium.update_medium("topic")
    elif (index == 1):
        userID = input("Enter UserID with @ symbol : ")
        if(userID[0] == "@") :
            medium.add_medium_account(userID)
        else:
            print("UserID not Valid")
    elif (index == 2):
        topic = input("Enter Topic you Want add : ")
        medium.add_medium_topic(topic)
        
    elif (index == 3):
        show_other_blogs()