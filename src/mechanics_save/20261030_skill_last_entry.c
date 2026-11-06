typedef unsigned char u8;
int native_main_0207ad3c(const u8 *table) {
    int index = 0;
    int result;
    do {
        const u8 *threshold = table + index;
        if (table[index] == 0) break;
        if (*(table + index * 4 + 10) == 0 && threshold[50] == 0) break;
        index++;
    } while (index < 10);
    result = index - 1;
    if (result < 0) result = 0;
    return result;
}
