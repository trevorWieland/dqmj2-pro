typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u32 values[8]; } SavedBlock;
typedef struct { u16 values[29]; } SavedRaw58;
typedef struct { u8 id; u8 allocated; } SavedSkill;
typedef struct { u8 name[20]; u32 id; s16 species; u8 variant; u8 byte1b; u8 byte1c; u8 byte1d; u8 byte1e; u8 byte1f; SavedBlock block; SavedRaw58 raw; SavedSkill skills[5]; } SavedRecord;
extern int native_species_count(int, int);
extern int native_record_skill_count(SavedRecord *);
extern void native_feature_collect(int, int, SavedSkill *, u8 *);
extern int native_action_filter(SavedSkill *, const u8 *, u32 *);
extern void native_projection(int, int, const u8 *, u8 *);
extern void native_copy(const void *, void *, u32);
int saved_record_runtime_view(u8 *view, SavedRecord *record, int extra) {
    if (record) {
        *(u32 *)(view + 4) = record->id;
        *(s16 *)(view + 46) = record->species;
        view[48] = record->variant;
        view[171] = native_species_count(record->species, record->variant);
        view[172] = native_record_skill_count(record);
        *(SavedRaw58 *)(view + 224) = record->raw;
        *(SavedBlock *)(view + 284) = record->block;
        native_feature_collect(record->species, record->variant, record->skills, view + 74);
        native_action_filter(record->skills, view + 74, (u32 *)(view + 12));
        native_projection(record->species, record->variant, view + 74, view + 138);
        view[175] = record->byte1c;
        native_copy(record, view + 182, 20);
        if (extra) {
            native_copy(record->skills, view + 214, 10);
            view[178] = record->byte1e;
            view[177] = record->byte1b;
        }
        return 1;
    }
    *(s16 *)(view + 46) = -1;
    return 0;
}
