typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 *native_fn_02062a10(u32);
extern u8 native_fn_02044fac(s32,s32);
extern u32 native_fn_02044f9c(s32,s32);
extern u32 native_fn_0207c880(void);
extern u32 native_fn_0207c8a4(u32,u32);
extern u32 native_fn_0207c9b8(u32,u32);
extern u32 native_fn_0207c8fc(u32);
u32 native_main_02057cb0(u32 id) {
    u8 *record;
    u8 level;
    u32 table;
    record=native_fn_02062a10(id);
    level=native_fn_02044fac(*(s16 *)(record+0x18),record[0x1A]);
    record[0x30]=level;
    table=native_fn_02044f9c(*(s16 *)(record+0x18),record[0x1A]);
    native_fn_0207c880();
    native_fn_0207c8a4(1,table);
    *(u32 *)(record+0x34)=native_fn_0207c9b8(table,level);
    *(u32 *)(record+0x38)=native_fn_0207c9b8(table,level+1);
    return native_fn_0207c8fc(1);
}
