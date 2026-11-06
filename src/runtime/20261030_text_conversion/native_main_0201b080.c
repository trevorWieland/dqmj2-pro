typedef unsigned int u32;
typedef unsigned short u16;
typedef struct { int (*decode)(u16 *, const char *, u32); int (*encode)(char *, u32); } encoding;
typedef struct { u32 fields[2]; encoding *text; } locale_view;
extern locale_view native_data_020dcf1c;
int native_main_0201b080(char *output, u32 input) {
    return native_data_020dcf1c.text->encode(output, input);
}
