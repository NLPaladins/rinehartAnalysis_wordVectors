from processed_book import ProcessedBook

books = {'The_Window_at_the_White_Cat': 'https://www.gutenberg.org/cache/epub/34020/pg34020.txt',
         'The_Amazing_Interlude': 'https://www.gutenberg.org/cache/epub/1590/pg1590.txt',
         'Dangerous_Days': 'https://www.gutenberg.org/files/1693/1693-0.txt',
         'The_Case_of_Jennie_Brice': 'https://www.gutenberg.org/cache/epub/11127/pg11127.txt',
         'The_After_House': 'https://www.gutenberg.org/files/2358/2358-0.txt',
         'The_Street_of_Seven_Stars': 'https://www.gutenberg.org/files/1214/1214-0.txt',
         'Locked_Doors': 'https://www.gutenberg.org/files/54273/54273-0.txt',
         'The_Bat': 'https://www.gutenberg.org/cache/epub/2019/pg2019.txt',
         'The_Confession': 'https://www.gutenberg.org/cache/epub/1963/pg1963.txt',
         'Tenting_To-night': 'https://www.gutenberg.org/cache/epub/19475/pg19475.txt',
         'Affinities and Other Stories': 'https://www.gutenberg.org/cache/epub/41408/pg41408.txt',
         'Sight_Unseen': 'https://www.gutenberg.org/files/1960/1960-0.txt',
         'Tish,_The_Chronicle_of_Her_Escapades_and_Excursions': 'https://www.gutenberg.org/cache/epub/3464/pg3464.txt',
         'A_Poor_Wise_Man': 'https://www.gutenberg.org/files/1970/1970-0.txt',
         'The_Truce_of_God': 'https://www.gutenberg.org/cache/epub/14573/pg14573.txt',
         'More_Tish': 'https://www.gutenberg.org/cache/epub/19851/pg19851.txt',
         'Where_Theres_A_Will': 'https://www.gutenberg.org/cache/epub/330/pg330.txt',
         'K': 'https://www.gutenberg.org/files/9931/9931-0.txt'}

for title, url in books.items():
    meta = {'url': url}
    book = ProcessedBook(title, meta)
