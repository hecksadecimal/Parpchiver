# -*- coding: utf-8 -*-
import json
import urllib2
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def archive_multipage_search(chat):
    if not os.path.exists(chat):
        os.makedirs(chat)
    initial_url = "https://msparp.com/%s/log/1.json" % chat
    response = urllib2.urlopen(initial_url)
    data = json.loads(response.read())
    total_msgs = data['total']
    msgs_per_page = len(data['messages'])
    divmod_total_msgs = divmod(total_msgs, msgs_per_page)
    if (divmod_total_msgs[1] != 0):
        total_pages = divmod_total_msgs[0] + 1
    else:
        total_pages = divmod_total_msgs[0]
    print("Total pages: %s" % total_pages)
    file_list = os.listdir(chat)
    file_list = [x.replace(".html", "") for x in file_list]
    file_list.sort(key=int)
    if (len(file_list) > 0):
        resume_from = int(file_list[-1])
        print("Resuming from %s" % resume_from)
    else:
        resume_from = 1

    # Unlike group chats, we don't do searched chats (with pages) in reverse order. This is because we can actually calculate the number of pages ourselves.
    # It also doesn't provide any sort of indication as to what the next page is, or if it exists.
    # Thus, this is easier in this instance. It also means we can use a for loop.
    for x in range(resume_from, total_pages + 1):
        loop_url = loop_url = "https://msparp.com/%s/log/%s.json" % (chat, x)
        loop_response = urllib2.urlopen(loop_url)
        loop_data = json.loads(loop_response.read())
        archive_page(loop_data, chat, x)

def archive_search(chat):
    if not os.path.exists(chat):
        os.makedirs(chat)
    final_url = "https://msparp.com/%s/log.json" % chat
    response = urllib2.urlopen(final_url)
    data = json.loads(response.read())
    print("%s" % (chat))
    with open('%s/%s.html' % (chat, chat), 'w+') as f:
        for message in data['messages']:
            f.write("<div style='color:#%s;'>%s: %s</div>" % (message['color'], message['acronym'], message['text']))

def archive_page(page_data, chat, date_code):
    if not os.path.exists(chat):
        os.makedirs(chat)
    print("%s: %s" % (chat, date_code))
    with open('%s/%s.html' % (chat, date_code), 'w+') as f:
        for message in page_data['messages']:
            f.write("<div style='color:#%s;'>%s: %s</div>" % (message['color'], message['acronym'], message['text']))

def archive_chat(chat):
    if not os.path.exists(chat):
        os.makedirs(chat)
    file_list = os.listdir(chat)
    if (len(file_list) > 0):
        resume_from = file_list[0].replace(".html", "")
        print("Resuming from %s" % resume_from)
    else:
        resume_from = None

    if (resume_from is not None):
        final_url = "https://msparp.com/%s/log/%s.json" % (chat, resume_from)
        response = urllib2.urlopen(final_url)
        data = json.loads(response.read())
        page_count = 1
        loop_run = True
        prev_page = data['previous_day']
    else:
        final_url = "https://msparp.com/%s/log.json" % chat
        response = urllib2.urlopen(final_url)
        data = json.loads(response.read())
        page_count = 1
        loop_run = True
        prev_page = data['previous_day']
        secondlast_page = prev_page

        # We need to do this a second time because the datecode for the last page isn't available straight from log.json
        secondlast_url = "https://msparp.com/%s/log/%s.json" % (chat, prev_page)
        secondlast_response = urllib2.urlopen(secondlast_url)
        secondlast_data = json.loads(secondlast_response.read())
        page_count = page_count + 1
        prev_page = secondlast_data['previous_day']
        final_page = secondlast_data['next_day']
        archive_page(data, chat, final_page)
        archive_page(secondlast_data, chat, secondlast_page)

    # We're also doing this in reverse order, because log.json is the only reliable endpoint that gives us the info for the remainder.
    # It's at the tail end of the log though.
    while loop_run:
        if (prev_page):
            loop_url = "https://msparp.com/%s/log/%s.json" % (chat, prev_page)
            loop_response = urllib2.urlopen(loop_url)
            loop_data = json.loads(loop_response.read())
            page_count = page_count + 1
            archive_page(loop_data, chat, prev_page)
            prev_page = loop_data['previous_day']
        else:
            loop_run = False

def is_search_multipage(chat):
    url_second = "https://msparp.com/%s/log/2.json" % chat
    response = urllib2.urlopen(url_second)
    if (response.geturl() is not "https://msparp.com/%s/log/2.json" % chat):
        return True
    else:
        return False

def does_chat_exist(chat):
    url = "https://msparp.com/%s/log.json" % chat
    response = urllib2.urlopen(url)
    try:
        data = json.loads(response.read())
    except ValueError:
        return False
    return True

def is_chat_search(chat):
    search_url = "https://msparp.com/%s/log.json" % chat
    response = urllib2.urlopen(search_url)
    data = json.loads(response.read())
    try:
        msg_number = data['total']
    except KeyError:
        return False
    return True

def main():
    if (len(sys.argv) == 2):
        chat = sys.argv[1]
        print("Getting logs for %s" % chat)
        if (does_chat_exist(chat)):
            if (is_chat_search(chat)):
                if (is_search_multipage(chat)):
                    archive_multipage_search(chat)
                else:
                    archive_search(chat)
            else:
                archive_chat(chat)
    elif (len(sys.argv) >= 3):
        chat = sys.argv[1]
        date_code = sys.argv[2]
        print("Getting %s for %s" % (date_code, chat))
        if (does_chat_exist(chat)):
            if (is_chat_search(chat)):
                print("It's a searched chat. Ignoring datecode")
                if (is_search_multipage(chat)):
                    archive_multipage_search(chat)
                else:
                    archive_search(chat)
            else:
                single_url = "https://msparp.com/%s/log/%s.json" % (chat, date_code)
                single_response = urllib2.urlopen(single_url)
                try:
                    single_data = json.loads(single_response.read())
                except ValueError:
                    print("Datecode does not exist.")
                    return
                archive_page(single_data, chat, date_code)
    else:
        chat = raw_input("Which chat would you like to archive? (leave empty to quit): ")
        if (chat == ""):
            print("Quitting.")
            return
        else:
            date_code = raw_input("Specify log datecode (leave empty for all): ")
            if (date_code == ""):
                print("Getting logs for %s" % chat)
                if (does_chat_exist(chat)):
                    if (is_chat_search(chat)):
                        if (is_search_multipage(chat)):
                            archive_multipage_search(chat)
                        else:
                            archive_search(chat)
                    else:
                        archive_chat(chat)
            else:
                print("Getting %s for %s" % (date_code, chat))
                if (does_chat_exist(chat)):
                    if (is_chat_search(chat)):
                        print("It's a searched chat. Ignoring datecode")
                        if (is_search_multipage(chat)):
                            archive_multipage_search(chat)
                        else:
                            archive_search(chat)
                    else:
                        single_url = "https://msparp.com/%s/log/%s.json" % (chat, date_code)
                        single_response = urllib2.urlopen(single_url)
                        try:
                            single_data = json.loads(single_response.read())
                        except ValueError:
                            print("Datecode does not exist.")
                            return
                        archive_page(single_data, chat, date_code)

if __name__ == '__main__':
    main()
