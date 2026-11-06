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
extern u32 native_fn_02034988(void *bank);
extern u32 native_fn_020349f4(void *bank, u32 index);
extern void native_fn_020349a8(signed int block);
void native_main_02034a1c(u32 rawBank) {
    Bank *bank = (Bank *)rawBank;
    bank->cells = (Cell *)((u32)bank->cells + (u32)bank);
    {
        void *oam = (void *)native_fn_02034988(bank);
        u16 i;
        for (i = 0; i < bank->count; ++i) {
            Cell *cell = (Cell *)native_fn_020349f4(bank, i);
            cell->oam = (void *)((u32)cell->oam + (u32)oam);
        }
    }
    if (bank->transfer != (void *)0) {
        Transfer *transfer = bank->transfer = (Transfer *)((u32)bank->transfer + (u32)bank);
        transfer->array = (void *)((u32)transfer->array + (u32)transfer);
        bank->transfer = transfer;
    }
    if (bank->extended != (void *)0) {
        bank->extended = (void *)((u32)bank->extended + (u32)bank);
        native_fn_020349a8((signed int)bank->extended);
    }
}
