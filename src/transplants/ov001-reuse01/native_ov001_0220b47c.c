typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u8 prefix[0x14]; u32 id; u8 remaining[0x6c]; } SavedRecord;
extern SavedRecord native_saved_records[];
extern u32 native_data_ov001_0223e058[];
extern u32 native_reserve_ids[];
extern u8 native_main[];
extern u8 native_section2[];
SavedRecord *save_record_by_id(u32 id) {
    int index;
    SavedRecord *record;
    SavedRecord *found = 0;
    if (id) {
        record = native_saved_records;
        index = 0;
        do {
            if (record->id == id) {
                found = record;
                break;
            }
            index++;
            record++;
        } while (index < 100);
    }
    return found;
}
SavedRecord *save_party_record(int slot) { return save_record_by_id(native_data_ov001_0223e058[slot]); }
u32 native_ov001_0220b47c(int slot) { return native_data_ov001_0223e058[slot]; }
u32 save_reserve_id(int slot) { return native_reserve_ids[slot]; }
SavedRecord *save_reserve_record(int slot) { return save_record_by_id(native_reserve_ids[slot]); }
u32 save_party_count(void) {
    int slot;
    u32 count = 0;
    slot = 0;
    do {
        if (save_party_record(slot)) count++;
        slot++;
    } while (slot < 3);
    return count;
}
u32 save_reserve_count(void) {
    int slot;
    u32 count = 0;
    slot = 0;
    do {
        if (save_reserve_record(slot)) count++;
        slot++;
    } while (slot < 3);
    return count;
}
SavedRecord *save_records_pointer(void) { return native_saved_records; }
u32 *save_summary_word_pointer(void) { return (u32 *)native_main; }
u8 *save_summary_tail_pointer(void) { return native_section2; }
u32 save_record_byte_query(u32 value) {
    if (value < 4) return 50;
    if (value < 10) return 75;
    return 100;
}
void save_record_byte32_set(u32 id, u32 value) {
    SavedRecord *record = save_record_by_id(id);
    if (record) ((u8 *)record)[0x32] = value;
}
