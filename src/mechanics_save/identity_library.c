typedef unsigned char u8;
typedef unsigned int u32;
typedef unsigned long long u64;
extern void *native_identity_record(int);
extern void *native_identity_profile(void);
extern int native_identity_insert(const void *);
extern void native_copy(const void *, void *, u32);
extern void native_fill(void *, int, u32);
extern int native_sdk_thumb_02097198(const void *);
extern u64 native_sdk_thumb_02096f50(const char *);
extern u64 native_sdk_thumb_02097330(const void *);
extern int native_sdk_thumb_02096ed0(const void *, u32, u32);
extern void native_sdk_thumb_0209734c(void *, u32, u32);
extern int native_sdk_thumb_020973d8(const void *, const void *);
extern void native_sdk_thumb_0209cd4c(void *);
extern int native_sdk_thumb_0209ccf4(const void *, u32);
extern int native_sdk_thumb_0209cc88(const void *, void *, u32 *);
int saved_identity_first_free(void) {
    int index = 0;
    do {
        if (!native_sdk_thumb_02097198(native_identity_record(index))) return index;
        index++;
    } while (index < 64);
    return -1;
}
void *saved_identity_string_parse(void *output, const char *text) {
    u64 code = native_sdk_thumb_02096f50(text);
    if (code != native_sdk_thumb_02097330(native_identity_profile())) {
        if (native_sdk_thumb_02096ed0(native_identity_profile(), (u32)code, (u32)(code >> 32))) {
            native_fill(output, 0, 12);
            native_sdk_thumb_0209734c(output, (u32)code, (u32)(code >> 32));
            return output;
        }
    }
    return 0;
}
int saved_identity_find(const void *identity) {
    if (identity) {
        int index = 0;
        do {
            if (native_sdk_thumb_020973d8(identity, native_identity_record(index))) return index;
            index++;
        } while (index < 64);
    }
    return -1;
}
int saved_identity_string_find(const char *text) {
    u8 data[12];
    return saved_identity_find(saved_identity_string_parse(data, text));
}
int saved_identity_string_insert(const char *text) {
    u8 data[12];
    return native_identity_insert(saved_identity_string_parse(data, text));
}
int saved_identity_record_write(int index, const void *identity) {
    if (identity && native_sdk_thumb_02097198(identity)) {
        native_copy(identity, native_identity_record(index), 12);
        return index;
    }
    return -2;
}
int saved_identity_record_clear(int index) {
    void *identity = native_identity_record(index);
    if (native_sdk_thumb_02097198(identity)) native_sdk_thumb_0209cd4c(identity);
    else native_fill(identity, 0, 12);
    return 1;
}
int saved_identity_record_data_valid(u32 length, const void *input) {
    return native_sdk_thumb_0209ccf4(input, length) != 0;
}
int saved_identity_record_data_read(int index, u32 expected_length, void *output) {
    u32 length;
    if (native_sdk_thumb_0209cc88(native_identity_record(index), output, &length)) return length == expected_length;
    return 0;
}
