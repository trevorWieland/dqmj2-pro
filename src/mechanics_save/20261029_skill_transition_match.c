typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef struct { u8 id; u8 inputs[3]; } NativeSkillAction;
typedef struct { u8 threshold[10]; NativeSkillAction actions[10]; u8 features[10]; } NativeSkillRecord;
extern NativeSkillRecord *native_fn_0207aa98(u32);
u32 native_main_0207ae2c(u32 skill, int allocated, u32 candidate) {
    int index;
    NativeSkillRecord *record;
    NativeSkillAction *actions;
    int result = 0;
    int found = 0;
    s8 member;
    record = native_fn_0207aa98(skill);
    actions = record->actions;
    index = 0;
    do {
        if (actions->id != 0 && allocated >= record->threshold[index]) {
            member = 0;
            do {
                if (candidate == actions->inputs[member]) {
                    found = 1;
                    result = actions->id;
                    break;
                }
                member++;
            } while (member < 3);
        }
        if (found) break;
        index++;
        actions++;
    } while (index < 10);
    return result;
}
