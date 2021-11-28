import logging
import os

import fitz
from fitz import Point
from fitz import Rect


def draw_guides(
    shape, x0: int, y0: float, x1: float, y1: float, width: float, height: float
):
    # This all could've been done more elegantly I am certain.
    logging.debug(f'points ({x0}, {y0})\t({x1}, {y1})')
    size = 20
    shape.draw_line(Point(x0, y0 - size), Point(x0, y0 + size))
    shape.draw_line(Point(x0 - size, y0), Point(x0 + size, y0))
    shape.draw_line(Point(x1, y1 - size), Point(x1, y1 + size))
    shape.draw_line(Point(x1 - size, y1), Point(x1 + size, y1))
    shape.draw_line(Point(x0, y1 - size), Point(x0, y1 + size))
    shape.draw_line(Point(x0 - size, y1), Point(x0 + size, y1))
    shape.draw_line(Point(x1, y0 - size), Point(x1, y0 + size))
    shape.draw_line(Point(x1 - size, y0), Point(x1 + size, y0))
    # lol at these hard coded values
    if y0 < 20:
        shape.draw_line(Point(x0, 0), Point(x0, y0))
        shape.draw_line(Point(x1, 0), Point(x1, y0))
    if y0 > 500:
        shape.draw_line(Point(x0, height), Point(x0, y1))
        shape.draw_line(Point(x1, height), Point(x1, y1))
    if x0 < 40:
        shape.draw_line(Point(0, y0), Point(x0, y0))
        shape.draw_line(Point(0, y1), Point(x0, y1))
    if x0 > 390:
        shape.draw_line(Point(x1, y0), Point(width, y0))
        shape.draw_line(Point(x1, y1), Point(width, y1))

    shape.finish()
    shape.commit()


def create_pdf(cards_path: str, side_size: int = 3):
    doc = fitz.open()
    width, height = fitz.paper_size('letter')
    imglist = os.listdir(cards_path + '/front')
    columns = side_size
    rows = side_size
    page = doc.new_page(width=width, height=height)
    horizontal_padding = width * (1 / 17)
    vertical_padding = height * (1 / 44)
    card_width = (width - (horizontal_padding * 2)) / columns
    card_height = (height - (vertical_padding * 2)) / rows
    count = 0
    row = 0
    column = 0
    for i, f in enumerate(imglist):
        path = os.path.join(cards_path, f)
        if not os.path.isfile(path) or 'DS_Store' in path or 'pdf' in path:
            continue
        x0 = column * card_width + horizontal_padding
        x1 = x0 + card_width
        y0 = row * card_height + vertical_padding
        y1 = y0 + card_height

        img = fitz.open(path)
        rect = Rect(x0, y0, x1, y1)
        pdfbytes = img.convert_to_pdf()
        img.close()
        imgPDF = fitz.open('pdf', pdfbytes)
        page.show_pdf_page(rect, imgPDF, 0)
        count = count + 1
        if count % columns == 0:
            row = row + 1
        column = count % columns

        shape = page.new_shape()
        draw_guides(shape, x0, y0, x1, y1, width, height)

    # for a new page call
    # page = doc.new_page(width = width, height = height)
    doc.save('cards.pdf')


def main():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    create_pdf('static/cards')


# i'm not sure how to tell vscode to run __main__.py lmao
if __name__ == '__main__':
    main()
