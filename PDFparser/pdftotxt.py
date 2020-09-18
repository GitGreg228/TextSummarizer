from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage


def process_content(input_string):
    """
    Processes string: removes all newlines
    and redundant spaces.
    """
    content = input_string
    content = content.replace("- \n", "")
    content = content.replace("-\n", "")
    content = content.replace("\n", " ")
    while "  " in content:
        content = content.replace("  ", " ")
    return content


class Book:
    """
    A class which contains pdf book path and content.
    Can create a txt book from pdf.
    """
    __path_to_pdf = ''
    __content = ''

    def auto(self, path, *txt_name):
        """
        Automatically creates txt file from the book.
        """
        Book.set_path(self, path)
        Book.get_content(self)
        Book.write_to_txt(self, txt_name)

    def set_path(self, path):
        """
        Checks if file exists and sets a path for it.
        """
        try:
            self.__path_to_pdf = path
        except FileNotFoundError:
            print("File does not exist")

    def path(self):
        """
        Returns the path of pdf file.
        """
        return self.__path_to_pdf

    def get_content(self):
        """
        Extract text from pdf and sets a content for it.
        """
        try:
            resource_manager = PDFResourceManager(caching=True)
            out_text = StringIO()
            la_params = LAParams()

            text_converter = TextConverter(resource_manager,
                                           out_text, laparams=la_params)
            file = open(self.__path_to_pdf, "rb")

            interpreter = PDFPageInterpreter(resource_manager,
                                             text_converter)
            for page in PDFPage.get_pages(
                    file, pagenos=set(), maxpages=0, password="",
                    caching=True, check_extractable=True
            ):
                interpreter.process_page(page)

            self.__content = out_text.getvalue()

            file.close()
            text_converter.close()
            out_text.close()

            return self.__content

        except not Book.path(self):
            print("First specify the path")

    def if_content(self):
        """
        If the content is parsed, returns True.
        Else returns False.
        """
        return bool(self.__content)

    def write_to_txt(self, txt_name):
        """
        Creates a txt file (default name: "txtbook.txt")
        with processed content.
        """
        try:
            self.__content = process_content(self.__content)
            if not txt_name:
                txt_name = "txtbook.txt"
            file = open(txt_name, "w")
            file.write(self.__content)
            file.close()
        except not self.__content:
            print("First process the content by using .get_content()")
