typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u32 words[8]; } SavedBlock20;
typedef struct { u8 skill; u8 allocated; } SavedSkill;
typedef struct { u8 prefix[20]; u32 id; s16 species; u8 variant; u8 before_block[5]; SavedBlock20 block; u8 middle[58]; SavedSkill skills[5]; } SavedRecord;
typedef struct { u8 prefix[28]; u16 initial[6]; u8 middle[55]; u8 default_skill; u8 remaining[4]; } NativeEktRecord;
extern SavedRecord *saved_record_by_id(u32);
extern NativeEktRecord *saved_native_ekt_record(int);
extern SavedSkill *saved_record_skill_pointer(u32, int);
extern void native_record_skill_bits(int, int, SavedSkill *, u8 *);
extern u32 native_record_derive24(void *, u8 *);
extern u32 native_record_derive26(void *, u8 *);
extern u32 native_record_next_word(int, int, int);
extern void native_record_skill_changed(int, int, int);
extern void native_fill(void *, u32, u32);
int saved_record_block20_initialize(u32 id, const SavedBlock20 *input) {
    u8 bits[64];
    int result = 0;
    SavedRecord *record = saved_record_by_id(id);
    NativeEktRecord *kind;
    native_record_skill_bits(record->species, record->variant, record->skills, bits);
    if (record) {
        if (input) {
            record->block = *input;
            result = 1;
        } else {
            kind = saved_native_ekt_record(record->species);
            if (kind) {
                native_fill(&record->block, 0, 32);
                ((u16 *)&record->block)[0] = kind->initial[0];
                ((u16 *)&record->block)[1] = kind->initial[1];
                ((u16 *)&record->block)[2] = native_record_derive24(&record->block, bits);
                ((u16 *)&record->block)[3] = native_record_derive26(&record->block, bits);
                ((u16 *)&record->block)[4] = kind->initial[2];
                ((u16 *)&record->block)[5] = kind->initial[3];
                ((u16 *)&record->block)[6] = kind->initial[4];
                ((u16 *)&record->block)[7] = kind->initial[5];
                ((u8 *)&record->block)[16] = 1;
                record->block.words[6] = native_record_next_word(record->species, record->variant, 2);
                result = 1;
            }
        }
    }
    return result;
}
int saved_record_skill_initialize(u32 id, int slot, const SavedSkill *input) {
    SavedSkill *skill;
    int result = 0;
    SavedRecord *record = saved_record_by_id(id);
    NativeEktRecord *kind;
    if (record) {
        skill = &record->skills[slot];
        if (input) {
            *skill = *input;
            result = 1;
        } else {
            kind = saved_native_ekt_record(record->species);
            if (kind) {
                skill->skill = kind->default_skill;
                skill->allocated = 0;
                result = 1;
            }
        }
        if (result) native_record_skill_changed(record->species, skill->skill, skill->allocated);
    }
    return result;
}
int saved_record_skill_nonzero_count(u32 id) {
    s8 index;
    int count;
    saved_record_by_id(id);
    count = 0;
    index = 0;
    do {
        if (saved_record_skill_pointer(id, index)->skill) count++;
        index++;
    } while (index < 5);
    return count;
}
int saved_record_skill_allocated_add(u32 id, int slot, int delta) {
    int result = 1;
    SavedRecord *record = saved_record_by_id(id);
    if (!record) result = 0;
    else record->skills[slot].allocated += delta;
    return result;
}
