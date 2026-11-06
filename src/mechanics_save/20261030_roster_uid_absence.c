typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
extern u32 *native_fn_0206bc80(u32 *output, u8 *count);
extern u32 *native_fn_0206bd24(u32 *output, u8 *count);
u32 native_main_020bf61c(u32 uid) {
    u8 count;
    u32 words[4];
    s32 first_index;
    s32 first_count;
    s32 second_count;
    s32 second_index;
    if (uid != 0) {
        native_fn_0206bc80(words, &count);
        first_count = count;
        first_index = 0;
        if (first_count > 0) {
            do {
                if (uid == words[first_index]) {
                    return 0;
                }
                first_index++;
            } while (first_index < first_count);
        }
        native_fn_0206bd24(words, &count);
        second_count = count;
        second_index = 0;
        if (second_count > 0) {
            do {
                if (uid == words[second_index]) {
                    return 0;
                }
                second_index++;
            } while (second_index < second_count);
        }
        return 1;
    }
    return 0;
}
