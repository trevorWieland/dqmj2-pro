typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
extern u8 native_records76[];
extern u8 native_records12[];
extern u8 native_scratch76[];
extern int native_index_valid(int);
extern int native_record_data_read(int, u32, void *);
extern int native_identity_find(const void *);
extern int native_identity_insert(const void *);
extern int native_string_identity_find(const char *);
extern int native_string_identity_insert(const char *);
extern int native_identity_remove(int);
extern int native_data_valid(u32, const void *);
extern void native_copy(const void *, void *, u32);
extern void native_copy_words(const void *, void *, u32);
extern void native_fill(void *, int, u32);
extern void native_word_fill(u32, void *, u32);
u8 *saved_identity_records76_pointer(void) { return native_records76; }
u8 *saved_identity_records12_pointer(void) { return native_records12; }
u8 *saved_identity_scratch76_pointer(void) { return native_scratch76; }
int saved_identity_data_read(int index, void *output) {
    if (native_index_valid(index)) return native_record_data_read(index, 76, output) != 0;
    return 0;
}
int saved_identity_name_write(const void *identity, const void *name) {
    int index = native_identity_find(identity);
    if (index == -1) index = native_identity_insert(identity);
    if (index >= 0) native_copy(name, saved_identity_records76_pointer() + index * 76, 20);
    return index;
}
int saved_identity_digits_write(const s8 *digits) {
    int offset;
    u8 *records;
    int index;
    index = native_string_identity_find((const char *)digits);
    if (index != -1) return index;
    index = native_string_identity_insert((const char *)digits);
    if (index >= 0) {
        u8 name[20];
        int input;
        int output;
        records = saved_identity_records76_pointer();
        offset = index * 76;
        native_fill(name, 0, 20);
        input = 0;
        output = 0;
        do {
            if (input / 4 && !(input % 4)) {
                name[output] = 0xe1;
                name[output + 1] = 0x43;
                output += 2;
            }
            name[output] = digits[input] - 0x2f;
            input++;
            output++;
        } while (input < 12);
        native_copy(name, records + offset, 20);
    }
    return index;
}
int saved_identity_remove(int index) {
    int result;
    if (native_index_valid(index)) {
        result = native_identity_remove(index);
        if (result) {
            native_word_fill(0, saved_identity_records76_pointer() + index * 76, 76);
            native_word_fill(0, saved_identity_records12_pointer() + index * 12, 12);
        }
        return result;
    }
    return 0;
}
int saved_identity_scratch_import(const void *input) {
    native_copy_words(input, saved_identity_scratch76_pointer(), 76);
    return native_data_valid(76, input);
}
