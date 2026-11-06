typedef unsigned char u8;
typedef unsigned int u32;
typedef unsigned long long u64;
extern const char native_identity_decimal_format[];
extern const char native_identity_base32_alphabet[];
extern const char native_identity_combined_format[];
extern int native_snprintf(char *, u32, const char *, ...);
extern u64 native_identity_login(const void *);
extern u32 native_identity_word2(const void *);
void saved_identity_decimal_format(char *output, u64 code) {
    native_snprintf(output, 13, native_identity_decimal_format, code);
}
void saved_identity_base32_format(u64 code, int bits, char *output) {
    int index;
    int length = (bits + 4) / 5;
    const char *alphabet = native_identity_base32_alphabet;
    index = 0;
    if (length > 0) {
        do {
            *(output + length - 1 - index) = alphabet[code & 31];
            code >>= 5;
            index++;
        } while (index < length);
    }
    output[length] = 0;
}
void saved_identity_combined_format(const void *identity, u32 key, char *output) {
    char login[21];
    char value[20];
    saved_identity_base32_format(native_identity_login(identity), 43, login + 1);
    saved_identity_base32_format(native_identity_word2(identity), 32, value);
    native_snprintf(output, 21, native_identity_combined_format, login + 1, (u8)(key >> 24), (u8)(key >> 16), (u8)(key >> 8), (u8)key, value);
}
