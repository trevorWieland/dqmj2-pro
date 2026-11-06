typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 prefix[24]; s16 species; u8 variant; u8 before_block[5]; u8 block[32]; u8 middle[58]; u8 skills[10]; } SavedRecord;
extern SavedRecord *saved_record_by_id(u32);
extern void native_record_feature_collect(int, int, const u8 *, u8 *);
extern u32 native_record_derive24(void *, const u8 *);
extern u32 native_record_derive26(void *, const u8 *);
extern int native_party_record_refresh(int);
extern int native_reserve_record_refresh(int);
int saved_record_derived_refresh(u32 id) {
    u8 features[64];
    SavedRecord *record = saved_record_by_id(id);
    if (!record) return 0;
    native_record_feature_collect(record->species, record->variant, record->skills, features);
    ((u16 *)record->block)[2] = native_record_derive24(record->block, features);
    ((u16 *)record->block)[3] = native_record_derive26(record->block, features);
    record->block[19] = 0;
    return 1;
}
int saved_party_derived_refresh(void) {
    int index = 0;
    int count = 0;
    do {
        if (native_party_record_refresh(index)) count++;
        index++;
    } while (index < 3);
    return count;
}
int saved_reserve_derived_refresh(void) {
    int index = 0;
    int count = 0;
    do {
        if (native_reserve_record_refresh(index)) count++;
        index++;
    } while (index < 3);
    return count;
}
