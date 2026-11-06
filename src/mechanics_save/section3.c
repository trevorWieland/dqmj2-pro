typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u32 first[5]; u8 second[24]; u16 value2c; u16 reserved2e; u32 value30; u32 value34; u32 value38; u8 date[16]; } OpaqueSavedRecord76;
extern u32 *saved_section3_flags_pointer(void);
extern u8 *saved_section3_records76_pointer(void);
extern u8 *saved_section3_records12_pointer(void);
extern int saved_section3_index_valid(int);
extern void native_copy(const void *, void *, u32);
extern void native_copy_words(const void *, void *, u32);
extern void native_fill(void *, u32, u32);
extern void native_date(void *);
void saved_section3_flag_write(int index, int value) {
    u32 *flags = saved_section3_flags_pointer();
    if (value == 1) *flags |= 1U << index;
    else *flags &= ~(1U << index);
}
int saved_section3_flag_get(int index) {
    u32 *flags = saved_section3_flags_pointer();
    return (*flags & (1U << index)) != 0;
}
int saved_section3_first20_differ(const u32 *first, const u32 *second) {
    int index = 0;
    do {
        if (first[index] != second[index]) return 1;
        index++;
    } while (index < 5);
    return 0;
}
int saved_section3_record76_merge(int index, const OpaqueSavedRecord76 *input) {
    if (saved_section3_index_valid(index)) {
        OpaqueSavedRecord76 *record = (OpaqueSavedRecord76 *)saved_section3_records76_pointer() + index;
        u32 previous[5];
        native_fill(previous, 0, 20);
        native_copy(record, previous, 20);
        if (((u8 *)input)[0]) {
            native_fill(record, 0, 20);
            native_copy(input, record, 20);
        }
        if (input->second[0]) {
            native_fill(record->second, 0, 24);
            native_copy(input->second, record->second, 20);
        }
        if (input->value2c) record->value2c = input->value2c;
        if (input->value30) record->value30 = input->value30;
        if (input->value34) record->value34 = input->value34;
        if (input->value38) record->value38 = input->value38;
        native_date(record->date);
        return saved_section3_first20_differ(previous, input->first);
    }
    return 0;
}
int saved_section3_record12_write(int index, const void *input) {
    u8 *record;
    if (!saved_section3_index_valid(index)) return 0;
    record = saved_section3_records12_pointer() + index * 12;
    native_copy_words(input, record, 12);
    return 1;
}
