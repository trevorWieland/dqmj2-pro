typedef unsigned int u32;
void *native_main_0201b21c(const void *buffer, int value, u32 count) {
    const unsigned char *cursor = buffer;
    unsigned char target = value;
    if (count) {
        do {
            if (*cursor++ == target) {
                return (void *)(cursor - 1);
            }
        } while (--count);
    }
    return 0;
}
