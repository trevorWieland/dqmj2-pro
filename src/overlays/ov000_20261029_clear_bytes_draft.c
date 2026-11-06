typedef signed char s8;
typedef signed int s32;

extern s8 data_ov000_022322d0[4];

s32 native_ov000_021e3180(void) {
    s32 index;
    s8 *cursor;
    cursor = data_ov000_022322d0;
    index = 0;
    do {
        index++;
        *cursor = -1;
        cursor++;
    } while (index < 4);
    return -1;
}
