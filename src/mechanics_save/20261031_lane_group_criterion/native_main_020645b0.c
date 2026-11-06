#include "group_criterion.h"
u32 native_main_020645b0(u32 criterion,u32 include_second) {
    const CriterionGroups *groups=(const CriterionGroups *)native_fn_020633b0();
    const CriterionRecord *record;
    s32 index;
    if (criterion==0) return 1;
    index=0;
    do {
        record=(const CriterionRecord *)native_fn_02062a10(groups->first[index]);
        if (record && !native_fn_02064654(criterion,record)) return 0;
        index++;
    } while (index<3);
    if (include_second==0) return 1;
    index=0;
    do {
        record=(const CriterionRecord *)native_fn_02062a10(groups->second[index]);
        if (record && !native_fn_02064654(criterion,record)) return 0;
        index++;
    } while (index<3);
    return 1;
}
