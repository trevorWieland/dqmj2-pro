typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u8 id; u8 allocated; } SavedSkill;
typedef struct { u8 id; u8 linked[3]; } NativeActionStage;
typedef struct { u8 thresholds[10]; NativeActionStage stages[10]; u8 features[10]; } NativeSkillRecord;
extern NativeSkillRecord *native_skill_record(u32);
extern int native_feature_count(int, const u8 *);
extern void native_fill_words(u32, void *, u32);
int saved_skill_action_banks(const SavedSkill *skills, const u8 *features, u32 *primary, u32 *secondary) {
    int slot;
    int stage;
    int linked;
    int allocated;
    NativeSkillRecord *record;
    if (primary) native_fill_words(0, primary, 32);
    if (secondary) native_fill_words(0, secondary, 32);
    if (primary) primary[0] |= 3;
    if (skills) {
        slot = 0;
        do {
            int id = skills[slot].id;
            if (id > 0) {
                record = native_skill_record(id);
                if (record) {
                    allocated = skills[slot].allocated;
                    stage = 0;
                    while (stage < 10) {
                        u32 action;
                        if (allocated < record->thresholds[stage]) break;
                        action = record->stages[stage].id;
                        if (action) {
                            if (primary) primary[action >> 5] |= 1u << (action & 31);
                            linked = 0;
                            while (linked < 3) {
                                u32 other = record->stages[stage].linked[linked];
                                if (!other) break;
                                if (secondary) secondary[other >> 5] |= 1u << (other & 31);
                                linked++;
                            }
                        }
                        stage++;
                    }
                }
            }
            slot++;
        } while (slot < 5);
    }
    if (native_feature_count(3, features) > 0) primary[0] |= 4;
    return 1;
}
int saved_skill_action_filter(const SavedSkill *skills, const u8 *features, u32 *primary) {
    u32 secondary[8];
    int index;
    saved_skill_action_banks(skills, features, primary, secondary);
    index = 0;
    do {
        primary[index] &= ~secondary[index];
        index++;
    } while (index < 8);
    return 1;
}
