typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u16 values[29]; } SavedRaw58;
typedef struct { u8 skill; u8 allocated; } SavedSkill;
extern u8 *saved_record_by_id(u32);
extern SavedSkill *saved_record_skill_pointer(u32, int);
extern void native_fill(void *, u32, u32);
int saved_record_has_skill(u32 id, int skill) {
    int result = 0;
    s8 index;
    u32 identity = id;
    int wanted = skill;
    if (saved_record_by_id(identity)) {
        index = 0;
        do {
            SavedSkill *current = saved_record_skill_pointer(identity, index);
            if (current && current->skill == wanted) result = 1;
            index++;
        } while (index < 5);
    }
    return result;
}
void saved_record_raw58_replace(u32 id, const SavedRaw58 *input) {
    u8 *record = saved_record_by_id(id);
    if (record) {
        if (input) *(SavedRaw58 *)(record + 64) = *input;
        else native_fill(record + 64, 0, 58);
    }
}
void saved_record_byte1b_set(u32 id, int value) {
    u8 *record = saved_record_by_id(id);
    if (record) record[27] = value;
}
void saved_record_byte1e_set(u32 id, int value) {
    u8 *record = saved_record_by_id(id);
    if (record) record[30] = value;
}
void saved_record_byte1c_set(u32 id, int value) {
    u8 *record = saved_record_by_id(id);
    if (record) record[28] = value;
}
void saved_record_byte1d_set(u32 id, int value) {
    u8 *record = saved_record_by_id(id);
    if (record) record[29] = value;
}
void saved_record_variant_set(u32 id, int value) {
    u8 *record = saved_record_by_id(id);
    if (record) record[26] = value;
}
