import argparse
import tkinter
from common.logger import logging
from core import CrawlProcess


def get_screen_size():
    try:
        tk = tkinter.Tk()
        width = tk.winfo_screenwidth()
        height = tk.winfo_screenheight()
        tk.quit()
        return {'width': width, 'height': height}
    except:
        return None


def main():
    parse = argparse.ArgumentParser(description='Interactive Crawl')
    parse.add_argument('url', help='url of website to be crawled')
    # browser config
    parse.add_argument('-t', '--timeout', metavar='', type=int, help='The timeout for all page requests, which is 5 seconds by default', default=5)
    parse.add_argument('--cookie', metavar='', help='Set Http Cookie')
    parse.add_argument('--proxy-server', metavar='', help='Http proxy address in the form of host:port')
    parse.add_argument('--headless', help='operation mode of browser and false by default', action="store_true")
    parse.add_argument('--exclude-links', metavar='', help='If the link contains this keyword, no request will be made. Multiple keywords are separated by the characters\', \'')
    parse.add_argument('--crawl-link-type', metavar='', help='Types of network resources crawled by the crawler, including xhr,fetch,document', default='xhr,fetch,document')
    parse.add_argument('--crawl-external-links', help='Enable external link crawling. only the same site link is crawled by default', action='store_true')


    args = parse.parse_args()
    browser_options = {
        'headless': args.headless,
        'external-links': args.crawl_external_links,
        'args': [],
        'req_type': [],
        'timeout': args.timeout,
        'headers': {},
        'screen_size': None
    }

    try:
        if args.proxy_server:
            browser_options['args'].append('--proxy-server={}'.format(args.proxy_server))
        if args.crawl_link_type:
            browser_options['req_type'] = args.crawl_link_type.split(',')
        if args.cookie:
            browser_options['headers']['cookie'] = args.cookie
        if args.headless or get_screen_size():
            browser_options['screen_size'] = get_screen_size()
        CrawlProcess(args.url, options=browser_options)
    except Exception as e:
        logging.error(e)



if __name__ == '__main__':
    main()

