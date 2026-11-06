typedef signed char s8;
typedef unsigned int u32;
typedef unsigned long long u64;
extern int native_identity_code_valid(u64, u32, int);
u64 saved_identity_decimal12(const s8 *text) {
    const s8 *end = text;
    u64 value = 0;
    u64 multiplier = 1;
    int index = 0;
    end += 11;
    do {
        int digit = *(end - index);
        if (digit < 48 || digit > 57) return 0;
        value += (u64)(digit - 48) * multiplier;
        multiplier *= 10;
        index++;
    } while (index < 12);
    return value;
}
u64 saved_identity_login_words(const u32 *identity) {
    return ((u64)(identity[0] & 0x7ff) << 32) | identity[1];
}
u64 saved_identity_pair_words(const u32 *identity) {
    return ((u64)identity[2] << 32) | identity[1];
}
int saved_identity_masked_write(u32 *word, u32 value, int shift, u32 mask) {
    if (value & ~mask) return 0;
    *word = (*word & ~(mask << shift)) | (value << shift);
    return 1;
}
u32 saved_identity_code_extract(u64 code, u32 key) {
    int mode = 0;
    do {
        if (native_identity_code_valid(code, key, mode)) return (u32)(code & 0xffffffffULL);
        mode++;
    } while (mode < 2);
    return 0;
}
