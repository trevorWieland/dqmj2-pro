#include "filter_categories.h"
s32 native_ov001_0222595c(s32 *available, const void *roster, s32 capability) {
    s32 values[3];
    s32 index, allowed, result;
    const CandidateRosterRecord *object = roster;
    native_fn_02008e0c(available, values, sizeof(values));
    index = 0;
    do {
        if (values[index]) {
            allowed = 0;
            if ((u8)((const SpeciesPrefix *)native_fn_020449d4(object->child->species))->category == 1) {
                if (native_fn_0207b02c(capability, 0x80000001)) allowed = 1;
            }
            if ((u8)((const SpeciesPrefix *)native_fn_020449d4(object->child->species))->category == 2) {
                if (native_fn_0207b02c(capability, 0x80000002)) allowed = 1;
            }
            if ((u8)((const SpeciesPrefix *)native_fn_020449d4(object->child->species))->category == 3) {
                if (native_fn_0207b02c(capability, 0x80000004)) allowed = 1;
            }
            if ((u8)((const SpeciesPrefix *)native_fn_020449d4(object->child->species))->category == 5) {
                if (native_fn_0207b02c(capability, 0x80000010)) allowed = 1;
            }
            if ((u8)((const SpeciesPrefix *)native_fn_020449d4(object->child->species))->category == 6) {
                if (native_fn_0207b02c(capability, 0x80000020)) allowed = 1;
            }
            if ((u8)((const SpeciesPrefix *)native_fn_020449d4(object->child->species))->category == 7) {
                if (native_fn_0207b02c(capability, 0x80000040)) allowed = 1;
            }
            if ((u8)((const SpeciesPrefix *)native_fn_020449d4(object->child->species))->category == 8) {
                if (native_fn_0207b02c(capability, 0x80000080)) allowed = 1;
            }
            if ((u8)((const SpeciesPrefix *)native_fn_020449d4(object->child->species))->category == 4) {
                if (native_fn_0207b02c(capability, 0x80000008)) allowed = 1;
            }
            if (allowed == 0) values[index] = 0;
        }
        index++;
        object++;
    } while (index < 3);
    result = native_fn_ov001_02223f20(values);
    if (result > 0) native_fn_02008e0c(values, available, sizeof(values));
    return result;
}
