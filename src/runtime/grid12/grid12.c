typedef signed int s32;
unsigned int native_main_020cfa78(s32 index, s32 *x, s32 *y) {
    if (index >= 0 && index < 12) {
        *x = (index % 4) * 40 + 48;
        *y = ((index / 4) + 1) * 40;
        return 1;
    }
    return 0;
}
