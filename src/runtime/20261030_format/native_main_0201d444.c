typedef unsigned char u8;
typedef unsigned int u32;
typedef char NdsWordPointerRequired[sizeof(void *) == 4 ? 1 : -1];
extern int format_buffer(u8 *, u32, const u8 *, void *);
int native_main_0201d444(u8 *buffer, const u8 *format, ...) {
    void *arguments = (void *)((((u32)&format) & ~3u) + 4);
    return format_buffer(buffer, 0xFFFFFFFFu, format, arguments);
}
