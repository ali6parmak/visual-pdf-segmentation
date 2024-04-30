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

CATEGORY_BY_ID = {
    1: "DocTitle",
    2: "ParaTitle",
    3: "ParaText",
    4: "ListText",
    5: "RegionTitle",
    6: "Date",
    7: "LetterHead",
    8: "LetterDear",
    9: "LetterSign",
    10: "Question",
    11: "OtherText",
    12: "RegionKV",
    13: "RegionList",
    14: "Abstract",
    15: "Author",
    16: "TableName",
    17: "Table",
    18: "Figure",
    19: "FigureName",
    20: "Equation",
    21: "Reference",
    22: "Footer",
    23: "PageHeader",
    24: "PageFooter",
    25: "Number",
    26: "Catalog",
    27: "PageNumber"
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


COLOR_BY_CATEGORY = {
    "DocTitle": "#FFD700",
    "ParaTitle": "#EED400",
    "ParaText": "#808080",
    "ListText": "#008B8B",
    "RegionTitle": "#DDD100",
    "Date": "#FFC300",
    "LetterHead": "#581845",
    "LetterDear": "#FF5733",
    "LetterSign": "#FFC300",
    "Question": "#900C3F",
    "OtherText": "#A0A0A0",
    "RegionKV": "#581845",
    "RegionList": "#449C8B",
    "Abstract": "#C70039",
    "Author": "#FFC300",
    "TableName": "#DD5C00",
    "Table": "#FF8C00",
    "Figure": "#C70039",
    "FigureName": "#FFC300",
    "Equation": "#581845",
    "Reference": "#FF5733",
    "Footer": "#C70039",
    "PageHeader": "#FF5733",
    "PageFooter": "#581845",
    "Number": "#C70039",
    "Catalog": "#FF5733",
    "PageNumber": "#E8D3A2"
}


PUBLAYNET_TYPE_BY_ID = {
    1: "Text",
    2: "Title",
    3: "Table",
    4: "Figure",
    5: "List"
}


PUBLAYNET_COLOR_BY_TYPE = {
    "Text": "#A0A0A0",
    "Title": "#EED400",
    "Table": "#FF8C00",
    "Figure": "#C70039",
    "List": "#008B8B",
}


DOCLAYNET_TYPE_BY_ID = {
    1: "Caption",
    2: "Footnote",
    3: "Formula",
    4: "ListItem",
    5: "PageFooter",
    6: "PageHeader",
    7: "Picture",
    8: "SectionHeader",
    9: "Table",
    10: "Text",
    11: "Title"
}

DOCLAYNET_COLOR_BY_TYPE = {
    "Caption": "#FFC300",
    "Footnote": "#581845",
    "Formula": "#FF5733",
    "ListItem": "#008B8B",
    "PageFooter": "#FF5733",
    "PageHeader": "#581845",
    "Picture": "#C70039",
    "SectionHeader": "#C70039",
    "Table": "#FF8C00",
    "Text": "#A0A0A0",
    "Title": "#EED400"
}


DOCBANK_TYPE_BY_ID = {
    1: "Abstract",
    2: "Author",
    3: "Caption",
    4: "Equation",
    5: "Figure",
    6: "Footer",
    7: "List",
    8: "Paragraph",
    9: "Reference",
    10: "Section",
    11: "Table",
    12: "Title"
}


DOCBANK_COLOR_BY_TYPE = {
    "Abstract": "#C70039",
    "Author": "#FFC300",
    "Caption": "#FFC300",
    "Equation": "#FF5733",
    "Figure": "#C70039",
    "Footer": "#581845",
    "List": "#008B8B",
    "Paragraph": "#A0A0A0",
    "Reference": "#FF5733",
    "Section": "#581845",
    "Table": "#FF8C00",
    "Title": "#EED400"
}