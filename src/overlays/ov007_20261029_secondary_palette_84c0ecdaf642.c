typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {
    u8 selector;
    u8 reserved[3];
    u32 map_bytes;
    void *archive;
    const u16 *palette;
    const void *map;
    const void *tiles;
    u32 tile_bytes;
    u32 palette_bytes;
} Secondary;
extern Secondary data_ov007_021da9b8;
extern void func_0204820c(const void *, u32, u32);
extern void func_02048308(void);
extern void func_02045994(u32, const void *, u32, u32);
extern void func_02045490(u32, const void *, u32, u32);
void native_ov007_021d7d7c(void) {
    u16 zero = 0;
    func_0204820c(data_ov007_021da9b8.palette, 0, data_ov007_021da9b8.palette_bytes);
    func_0204820c(&zero, 0, 2);
    func_02048308();
    func_02045994(2, data_ov007_021da9b8.map, 0, data_ov007_021da9b8.map_bytes);
    func_02045490(2, data_ov007_021da9b8.tiles, 0, data_ov007_021da9b8.tile_bytes);
}
