typedef unsigned int u32;
typedef unsigned short u16;
typedef struct { int (*decode)(u16 *, const char *, u32); int (*encode)(char *, u32); } encoding;
typedef struct { u32 fields[2]; encoding *text; } locale_view;
extern locale_view native_data_020dcf1c;
extern u32 native_fn_0201d69c(const char *);
extern int native_fn_0201b018(u16 *, const char *, u32);
extern int native_fn_0201b080(char *, u32);
extern void *native_fn_0201d780(void *, const void *, u32);
u32 native_main_0201b09c(u16 *output, const char *input, u32 limit) {
    u32 count;
    u32 remaining = native_fn_0201d69c(input);
    int step;
    count = 0;
    if (output) {
        while (count < limit) {
            if (*input) {
                step = native_fn_0201b018(output, input, remaining);
                output++;
                if (step > 0) {
                    input += step;
                    remaining -= step;
                } else {
                    return (u32)-1;
                }
            } else {
                *output = 0;
                break;
            }
            count++;
        }
    }
    return count;
}
