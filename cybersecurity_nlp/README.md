# Text Processing

## Text Extraction

Text extraction from PDFs is performed with `pdfminer.six`.

## Text Cleaning

The text extracted from the PDFs is often very messy, so there is a text cleaning step to adjust spacing and normalizing certain unicode characters.

## Sentence Tokenization

The `PunktSentenceTokenizer` is extended to allow for custom tokenization rules.

## Sentence Filtering

There is a sentence filter to remove bad sentences after tokenizing.

## Paragraph Detection

Inititally, paragraphs have been defined as runs of good sentences, but that could be improved dramatically.