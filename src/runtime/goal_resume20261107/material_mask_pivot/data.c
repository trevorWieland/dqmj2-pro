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
#define MATERIAL_MASK(i) (((i)&1?0x7fffUL:0)|((i)&2?0x7fff0000UL:0)|((i)&4?0x8000UL:0))
#define REMAIN_FIRST(i) ((i)==0?1:0)
#define REMAIN_SECOND(i) ((i)==2?1:2)
#define MATRIX_INDEX(r,c) (3*(r)+(c))
#define PIVOT_ROW(p) { \
    MATRIX_INDEX(REMAIN_FIRST((p)/3),REMAIN_FIRST((p)%3)), \
    MATRIX_INDEX(REMAIN_FIRST((p)/3),REMAIN_SECOND((p)%3)), \
    MATRIX_INDEX(REMAIN_SECOND((p)/3),REMAIN_FIRST((p)%3)), \
    MATRIX_INDEX(REMAIN_SECOND((p)/3),REMAIN_SECOND((p)%3)) }
const NativeMaterialPivot native_data_main_020d9068 = {
    { MATERIAL_MASK(0), MATERIAL_MASK(1), MATERIAL_MASK(2), MATERIAL_MASK(3),
      MATERIAL_MASK(4), MATERIAL_MASK(5), MATERIAL_MASK(6), MATERIAL_MASK(7) },
    { PIVOT_ROW(0), PIVOT_ROW(1), PIVOT_ROW(2),
      PIVOT_ROW(3), PIVOT_ROW(4), PIVOT_ROW(5),
      PIVOT_ROW(6), PIVOT_ROW(7), PIVOT_ROW(8) }
};
