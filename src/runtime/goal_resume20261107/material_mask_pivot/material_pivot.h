#ifndef DQM_MATERIAL_PIVOT_H
#define DQM_MATERIAL_PIVOT_H
typedef struct NativeMaterialPivot {
    const unsigned long masks[8];
    const unsigned char pivots[9][4];
} NativeMaterialPivot;
extern const NativeMaterialPivot native_data_main_020d9068;
typedef char MaterialSDKWordWidth[sizeof(unsigned long)==4?1:-1];
typedef char MaterialPivotBytes[sizeof(NativeMaterialPivot)==68?1:-1];
#endif
