typedef unsigned int u32;
typedef signed int s32;
typedef signed char s8;
s8 * native_main_0201b1bc(s8 *destination, s8 *source, u32 count) {
    s8 *end_source;
    s8 *position;
    if ((u32)source >= (u32)destination) {
        position = destination;
        if (count == 0) return destination;
        do { *position++ = *source++; } while (--count != 0);
    } else {
        end_source = source + count;
        position = destination + count;
        if (count == 0) return destination;
        do { *--position = *--end_source; } while (--count != 0);
    }
    return destination;
}
