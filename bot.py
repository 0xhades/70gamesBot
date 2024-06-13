import requests
from bs4 import BeautifulSoup
import math, time, json

client = requests.session()
cookies = {
    'bbs_sid': 'YOUR_SID_HERE',
    'bbs_token': 'YOUR_TOKEN_HERE'
}

def get_threads(page):
    
    page = abs(math.floor(page))
    url = "https://70games.net/index-" + str(page) + ".htm"

    headers = {
        'Host': '70games.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.1;) AppleWebKit/533.26 (KHTML, like Gecko) Chrome/49.0.3208.106 Safari/537',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Alt-Used': '70games.net',
        'Connection': 'keep-alive',
        'Referer': 'https://70games.net/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=1'
    }

    response = client.get(url, cookies=cookies, headers=headers)
    print(f"[+] Status code: {response.status_code}")
    response.encoding = "utf-8"

    return BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

def get_thread(page):
    
    url = "https://70games.net/thread-" + str(page) + ".htm"

    headers = {
        'Host': '70games.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.1;) AppleWebKit/533.26 (KHTML, like Gecko) Chrome/49.0.3208.106 Safari/537',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Alt-Used': '70games.net',
        'Connection': 'keep-alive',
        'Referer': 'https://70games.net/forum-1.htm',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=1'
    }

    response = client.get(url, cookies=cookies, headers=headers)
    print(f"[+] Status code: {response.status_code}")
    response.encoding = "utf-8"

    return BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

def parse_threads(soup):

    li_elements = soup.select('ul.list-unstyled.threadlist.mb-0 li.mdui-ripple.media.thread.threadItem.pop_peopleSimple')

    hrefs = [li.find('a', class_='post_title') for li in li_elements if li.find('a', class_='post_title')]

    for i in range(len(hrefs)):
      
        part_after_hyphen = hrefs[i]['href'].split('-')[1]
        number = part_after_hyphen.split('.')[0]

        hrefs[i] = [hrefs[i]['title'], number, "https://70games.net/" + hrefs[i]['href']]

    if len(hrefs) == 0:
        print("[-] No threads found")
        exit(1)

    return hrefs

def get_credentials(soup):
    fieldset = soup.find('fieldset', class_='fieldset') 

    inputs = fieldset.find_all('input')

    input_values = [input_tag.get('value') for input_tag in inputs]

    if len(input_values) == 1:
        print("[-] Only username found, password is hidden")
        return
    
    if len(input_values) == 0:
        print("[-] No username, password found")
        return
    
    for value in input_values:
        print("[+] " + value)

def get_thread_items(soup):

    ul_element = soup.find('ul', class_='site-list-ul')

    # scraped_data = []

    if ul_element:

        span = ul_element.find('span', class_='text-danger')
        if span:
            number = span.get_text(strip=True)
            print(f"[+] Number of items: {number}")

    b_tags = ul_element.find_all('b')

    i = 0

    for b_tag in b_tags:
        type_ = b_tag.get_text(strip=True)

        next_sibling = b_tag.next_sibling
        while next_sibling and next_sibling.name != 'br':
            if next_sibling.name == 'span' and 'text-success' in next_sibling.get('class', []):
                id_ = next_sibling.get_text(strip=True)
                break
            next_sibling = next_sibling.next_sibling
        else:
            text = b_tag.next_sibling.strip()
            id_ = text.split(' ')[1]

        a_tag = b_tag.find_next('a')
        link = a_tag['href'] if a_tag else None
        link_text = a_tag.get_text(strip=True)

        # scraped_data.append({'type': type_, 'id': id_, 'link': link, 'link_text': link_text})

        print(f"[{i+1}] Type: {type_}, Title: {link_text}, ID: {id_}, Link: {link}")
        i += 1
        if i >= 100:
            print(f"[-] Too many items to display, only displayed first 100 items")
            break

def comment(thread):
    url = "https://70games.net/post-create-" + thread + "-1.htm"

    headers = {
        'Host': '70games.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.1;) AppleWebKit/533.26 (KHTML, like Gecko) Chrome/49.0.3208.106 Safari/537',
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '87',
        'Origin': 'https://70games.net',
        'Alt-Used': '70games.net',
        'Connection': 'keep-alive',
        'Referer': 'https://70games.net/thread-' + thread + '.htm',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Priority': 'u=1'
    }

    data = {
        'doctype': '1',
        'return_html': '1',
        'quotepid': '0',
        'sid': cookies["bbs_sid"],
        'message': 'thanks+!+dude'
    }

    response = client.post(url, cookies=cookies, headers=headers, data=data)
    print(f"[+] Status code: {response.status_code}")
    response.encoding = "utf-8"
    text = response.content.decode('utf-8')
    
    j = json.loads(text)

    if j["code"] == "0" and response.status_code == 200:
        print("[+] Comment posted!")
        return True
    else:
        print("[-] Comment not posted")
    
    return False

p = 0
while True:

    threads = get_threads(p)
    list_of_threads = parse_threads(threads)

    for i in range(len(list_of_threads)):
        print(f"[{i+1}] Title: {list_of_threads[i][0]}, Number: {list_of_threads[i][1]}, Link: {list_of_threads[i][2]}")

    i = 0
    for thread in list_of_threads:

        print()

        print(f"[{i+1}] --> Title: {thread[0]}, Number: {thread[1]}, Link: {thread[2]}")

        thread_page = get_thread(thread[1])
        get_thread_items(thread_page)

        if input("Do you want to continue? (y/n): ").lower() != "y":
            continue

        if comment(thread[1]):
            time.sleep(2)
            thread_page = get_thread(thread[1])
            get_credentials(thread_page)
        
        i += 1

    p += 1
