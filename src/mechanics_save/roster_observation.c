typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned int u32;
typedef struct { u8 prefix[20]; u32 id; s16 species; u8 variant; u8 tail[105]; } SavedRecord;
typedef struct { u8 prefix[28]; u32 party[3]; u32 reserve[3]; } SavedGroups;
extern SavedRecord native_records[100];
extern SavedGroups native_groups;
extern SavedRecord *saved_record_by_id(u32);
extern int native_record_exists(u32);
extern u32 native_record_next_id(void);
extern int native_obtained_set(int, int);
extern int native_seen_set(int, int);
extern int native_category(int);
extern int native_event16_get(void);
extern void native_record_features_observe(SavedRecord *);
extern int native_records_sort(void);
extern void native_fill(void *, u32, u32);
extern void native_secondary_set(int, int);
extern void native_feature_collect(int, int, const u8 *, u8 *);
extern void native_feature_observed_set(int);
extern SavedRecord *native_record_base(void);
extern int native_record_skill_count(u32);
extern u8 *native_record_skill_pointer(u32, int);
extern void native_skill_observe(int, int, int);
void saved_roster_skills_observe(void) {
    SavedRecord *record;
    int count;
    int index;
    record = native_record_base();
    index = 0;
    do {
        if (record->id) {
            s8 slot;
            count = native_record_skill_count(record->id);
            slot = 0;
            if (count > 0) do {
                u8 *skill = native_record_skill_pointer(record->id, slot);
                native_skill_observe(record->species, skill[0], skill[1]);
                slot++;
            } while (slot < count);
        }
        index++;
        record++;
    } while (index < 100);
}
