typedef unsigned char u8;
typedef signed char s8;
typedef struct { u8 threshold[10]; u8 actions[40]; u8 features[10]; } NativeSkillRecord;
int native_main_0207ad98(NativeSkillRecord *record, s8 index) {
    u8 *bytes = (u8 *) record;
    u8 *actions = bytes + 10 + index * 4;
    u8 *features = bytes + 50;
    int action = *actions;
    if (action == 0) action = features[index];
    return action;
}
