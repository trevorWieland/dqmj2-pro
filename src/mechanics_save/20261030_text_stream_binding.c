typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {
    u8 prefix[0xA4];
    const u16 *stream;
    u8 changed;
    u8 count;
} TextBinding;
TextBinding *native_main_020853c8(TextBinding *target, const u16 *stream) {
    u8 index;
    u32 result = 1;
    target->changed = 1;
    target->stream = stream;
    index = 0;
    do {
        if (stream[index] == 0) {
            result = index;
            break;
        }
        index++;
    } while (index < 32);
    target->count = result;
    return target;
}
