typedef unsigned int u32;
int native_main_0201b248(const void *left, const void *right, u32 count) {
    const unsigned char *a = left;
    const unsigned char *b = right;
    if (count) {
        do {
            if (*a++ != *b++) {
                return a[-1] < b[-1] ? -1 : 1;
            }
        } while (--count);
    }
    return 0;
}
