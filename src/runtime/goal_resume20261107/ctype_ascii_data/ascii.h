#ifndef DQM_ASCII_DATA_H
#define DQM_ASCII_DATA_H
enum ASCIIClass {
    ASCII_ALPHA=1, ASCII_BLANK=2, ASCII_CONTROL=4, ASCII_DIGIT=8,
    ASCII_GRAPH=16, ASCII_LOWER=32, ASCII_PRINT=64, ASCII_PUNCT=128,
    ASCII_SPACE=256, ASCII_UPPER=512, ASCII_HEX=1024
};
#define ASCII_BETWEEN(c,a,b) ((c)>=(a)&&(c)<=(b))
#define ASCII_IS_UPPER(c) ASCII_BETWEEN(c,'A','Z')
#define ASCII_IS_LOWER(c) ASCII_BETWEEN(c,'a','z')
#define ASCII_IS_ALPHA(c) (ASCII_IS_UPPER(c)||ASCII_IS_LOWER(c))
#define ASCII_IS_DIGIT(c) ASCII_BETWEEN(c,'0','9')
#define ASCII_IS_GRAPH(c) ASCII_BETWEEN(c,'!','~')
#define ASCII_IS_SPACE(c) ((c)==' '||ASCII_BETWEEN(c,9,13))
#define ASCII_TO_UPPER(c) (ASCII_IS_LOWER(c)?(c)-'a'+'A':(c))
#define ASCII_CLASS(c) (\
    (ASCII_IS_ALPHA(c)?ASCII_ALPHA:0)|\
    ((c)==9||(c)==' '?ASCII_BLANK:0)|\
    ((c)<32||(c)==127?ASCII_CONTROL:0)|\
    (ASCII_IS_DIGIT(c)?ASCII_DIGIT:0)|\
    (ASCII_IS_GRAPH(c)?ASCII_GRAPH:0)|\
    (ASCII_IS_LOWER(c)?ASCII_LOWER:0)|\
    (ASCII_BETWEEN(c,' ','~')?ASCII_PRINT:0)|\
    (ASCII_IS_GRAPH(c)&&!ASCII_IS_ALPHA(c)&&!ASCII_IS_DIGIT(c)?ASCII_PUNCT:0)|\
    (ASCII_IS_SPACE(c)?ASCII_SPACE:0)|\
    (ASCII_IS_UPPER(c)?ASCII_UPPER:0)|\
    (ASCII_IS_DIGIT(c)||ASCII_BETWEEN(c,'A','F')||ASCII_BETWEEN(c,'a','f')?ASCII_HEX:0))
typedef char ASCIIByteWidth[sizeof(unsigned char)==1?1:-1];
typedef char ASCIIClassWidth[sizeof(unsigned short)==2?1:-1];
typedef char ASCIIExecutionSet['A'==65&&'a'==97&&'0'==48&&'~'==126?1:-1];
#endif
