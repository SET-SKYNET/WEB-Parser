from Parser import Parser


if __name__ == '__main__':
    # Parse CLI arguments for Parser class
    import argparse
    parser = argparse.ArgumentParser(description='Argumments, to be used in Parser class')
    parser.add_argument(
        '--chromedriver',
        type=str,
        required=True,
        help='Path to chromedriver binary')
    parser.add_argument(
        '--deserialize_links_from',
        type=str,
        required=True,
        help='File.txt with a list of links to be parsed')
    parser.add_argument(
        '--serialize_data_to',
        type=str,
        required=True,
        help='File.xslx where parsed data will be saved to')

    args = parser.parse_args()

    # Initialize Parser class
    parser = Parser(
        chromedriver = args.chromedriver,
        deserialize_links_from = args.deserialize_links_from,
        serialize_data_to = args.serialize_data_to
    )

    # Get links from file.txt
    links = parser.deserialize_links_from_txt()

    # Run application
    parser.parse_data(links)
