typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
extern void native_copy(const void *, void *, u32);
extern u32 *native_summary_word_pointer(void);
extern u32 native_summary_byte_get(void);
extern u32 save_event_get(int);
extern u8 *native_party_slot_get(int);
extern u32 native_party_byte_query(u32);
extern u8 *native_summary_tail_pointer(void);
void save_header_summary(u8 *summary, u8 *main_state) {
    u8 *record;
    int index;
    native_copy(main_state + 8, summary + 4, 0x14);
    *(u32 *)summary = *native_summary_word_pointer();
    summary[0x5d] = native_summary_byte_get();
    summary[0x5f] = save_event_get(0xac) != 0;
    summary[0x5f] |= (u8)(save_event_get(0xad) ? 2 : 0);
    summary[0x5f] |= (u8)(save_event_get(0xae) ? 4 : 0);
    summary[0x5f] |= (u8)(save_event_get(0xaf) ? 8 : 0);
    summary[0x5f] |= (u8)(save_event_get(0xb2) ? 16 : 0);
    summary[0x5f] |= (u8)(save_event_get(0xb1) ? 32 : 0);
    summary[0x5f] |= (u8)(save_event_get(0x22f) ? 64 : 0);
    for (index = 0; index < 3; index++) {
        record = native_party_slot_get(index);
        if (record) {
            native_copy(record, summary + 0x18 + index * 0x14, 0x14);
            summary[0x5a + index] = record[0x30];
            if (record[0x30] == native_party_byte_query(record[0x1c])) summary[0x5a + index] |= 0x80;
            *(s16 *)(summary + 0x54 + index * 2) = *(s16 *)(record + 0x18);
        } else {
            summary[0x18 + index * 0x14] = 0xe3;
            summary[0x19 + index * 0x14] = 0x1b;
            summary[0x5a + index] = 0;
            *(s16 *)(summary + 0x54 + index * 2) = 0;
        }
    }
    summary[0x5e] = *native_summary_tail_pointer();
}
