typedef signed char s8;
typedef unsigned char u8;
typedef struct { s8 *cursor; int eof; } Reader;
int native_main_0201d618(Reader *reader, int value, int mode) {
    s8 byte;
    switch (mode) {
    case 0:
        byte = *reader->cursor;
        if (byte == 0) {
            reader->eof = 1;
            return -1;
        }
        reader->cursor++;
        return (u8)byte;
    case 1:
        if (reader->eof == 0) reader->cursor--;
        else reader->eof = 0;
        return value;
    case 2:
        return reader->eof;
    default:
        return 0;
    }
}
