typedef unsigned int u32;
typedef unsigned short u16;
typedef struct { int (*decode)(u16 *, const char *, u32); int (*encode)(char *, u32); } encoding;
typedef struct { u32 fields[2]; encoding *text; } locale_view;
extern locale_view native_data_020dcf1c;
extern u32 native_fn_0201d69c(const char *);
extern int native_fn_0201b018(u16 *, const char *, u32);
extern int native_fn_0201b080(char *, u32);
extern void *native_fn_0201d780(void *, const void *, u32);
u32 native_main_0201b124(char *output, const u16 *input, u32 limit) {
    char converted[4];
    u32 count = 0;
    int bytes;
    if (!output || !input) {
        return 0;
    }
    do {
        if (!*input) {
            output[count] = 0;
            break;
        }
        bytes = native_fn_0201b080(converted, *input++);
        if (count + bytes > limit) {
            break;
        }
        native_fn_0201d780(output + count, converted, bytes);
        count += bytes;
    } while (count <= limit);
    return count;
}
