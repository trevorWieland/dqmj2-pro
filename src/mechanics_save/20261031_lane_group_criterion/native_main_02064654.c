#include "group_criterion.h"
u32 native_main_02064654(u32 criterion,const CriterionRecord *record) {
    u32 value=native_fn_02044dc4(record->species,record->variant);
    switch (criterion) {
    case 0:
    default:
        break;
    case 1:
        if (value!=1 && value!=2 && value!=3) return 0;
        break;
    case 2:
        if (value!=4 && value!=5 && value!=6) return 0;
        break;
    case 3:
        if (value!=7 && value!=8 && value!=9) return 0;
        break;
    }
    return 1;
}
