from pdfminer.high_level import extract_text


def main() -> None:

    pages: range = range(10)
    book_name: str = 'Deep learning with python.pdf'

    text = extract_text(
        book_name, page_numbers=pages
    )

    print(text)

    with open('t.txt', 'w') as f:
        f.write(text)


if __name__ == '__main__':
    main()