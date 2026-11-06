typedef unsigned char u8;
extern const u8 native_data_020d8d04[128];
static inline int mapped(int value) {
    if (value < 0 || value >= 128) return value;
    return native_data_020d8d04[value];
}
int native_main_02023ef8(const u8 *left, const u8 *right) {
    u8 a, b;
    do {
        a = mapped(*left++);
        b = mapped(*right++);
        if (a < b) return -1;
        if (a > b) return 1;
    } while (a);
    return 0;
}
