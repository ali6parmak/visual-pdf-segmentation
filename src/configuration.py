from pdf_token_type_labels.TokenType import TokenType

PDF_LABELED_DATA_ROOT_PATH = "/home/ali/Desktop/pdf-labeled-data"
pdfs_root_path = "/home/ali/Desktop/pdf-labeled-data/pdfs"

CATEGORIES = {
    "DocTitle": 1,
    "ParaTitle": 2,
    "ParaText": 3,
    "ListText": 4,
    "RegionTitle": 5,
    "Date": 6,
    "LetterHead": 7,
    "LetterDear": 8,
    "LetterSign": 9,
    "Question": 10,
    "OtherText": 11,
    "RegionKV": 12,
    "RegionList": 13,
    "Abstract": 14,
    "Author": 15,
    "TableName": 16,
    "Table": 17,
    "Figure": 18,
    "FigureName": 19,
    "Equation": 20,
    "Reference": 21,
    "Footer": 22,
    "PageHeader": 23,
    "PageFooter": 24,
    "Number": 25,
    "Catalog": 26,
    "PageNumber": 27
}

D4LA_TYPES_TO_TOKEN_TYPES = {
    1: TokenType.TITLE,
    2: TokenType.TITLE,
    3: TokenType.TEXT,
    4: TokenType.LIST,
    5: TokenType.TITLE,
    6: TokenType.TEXT,
    7: TokenType.TEXT,
    8: TokenType.TITLE,
    9: TokenType.TEXT,
    10: TokenType.TEXT,
    11: TokenType.TEXT,
    12: TokenType.TEXT,
    13: TokenType.LIST,
    14: TokenType.TEXT,
    15: TokenType.TEXT,
    16: TokenType.TABLE,
    17: TokenType.TABLE,
    18: TokenType.FIGURE,
    19: TokenType.IMAGE_CAPTION,
    20: TokenType.FORMULA,
    21: TokenType.TEXT,
    22: TokenType.FOOTER,
    23: TokenType.HEADER,
    24: TokenType.FOOTER,
    25: TokenType.FORMULA,
    26: TokenType.TEXT,
    27: TokenType.PAGE_NUMBER
}

REVERSED_CATEGORIES = {
    TokenType.FORMULA: 20,
    TokenType.FOOTNOTE: 24,
    TokenType.LIST: 4,
    TokenType.TABLE: 27,
    TokenType.FIGURE: 18,
    TokenType.TITLE: 2,
    TokenType.TEXT: 3,
    TokenType.HEADER: 23,
    TokenType.PAGE_NUMBER: 27,
    TokenType.IMAGE_CAPTION: 19,
    TokenType.FOOTER: 24,
    TokenType.TABLE_OF_CONTENT: 21,
    TokenType.MARK: 11
}

COLOR_BY_TOKEN_TYPE = {
    TokenType.FORMULA: "#808000",
    TokenType.FOOTNOTE: "#7B68EE",
    TokenType.LIST: "#008B8B",
    TokenType.TABLE: "#FF8C00",
    TokenType.FIGURE: "#C71585",
    TokenType.TITLE: "#FFD700",
    TokenType.TEXT: "#808080",
    TokenType.HEADER: "#A2D7E8",
    TokenType.PAGE_NUMBER: "#E8D3A2",
    TokenType.IMAGE_CAPTION: "#FC92FC",
    TokenType.FOOTER: "#988DD9",
    TokenType.TABLE_OF_CONTENT: "#FFA07A",
    TokenType.MARK: "#FF7A99"
}
