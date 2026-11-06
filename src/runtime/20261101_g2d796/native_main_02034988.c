typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed short s16;
typedef struct { u16 count, attr; void *oam; } Cell;
typedef struct { Cell cell; s16 maxX, maxY, minX, minY; } CellBR;
typedef struct { u32 size; void *array; } Transfer;
typedef struct {
    u16 count, attr;
    Cell *cells;
    u32 mapping;
    Transfer *transfer;
    void *strings;
    void *extended;
} Bank;
u32 native_main_02034988(void *rawBank) {
    Bank *bank = (Bank *)rawBank;
    if (bank->attr & 1) return (u32)((CellBR *)bank->cells + bank->count);
    return (u32)(bank->cells + bank->count);
}
