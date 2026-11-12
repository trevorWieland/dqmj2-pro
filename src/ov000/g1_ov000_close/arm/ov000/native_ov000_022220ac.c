/* ov000 row 0x022220ac: 128 bytes.
 *
 * What it does: 31 instructions and 5 call(s), then a 8-entry dispatch through an inline branch table at 0x022220c8 (dispatch word at 0x022220c0)
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles, the meaning of the table entries and every callee contract are not established by byte identity; the dispatch range and the table bounds are measured.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02221cb4(void);
extern void native_fn_02221dac(void);
extern void native_fn_02221dd4(void);
extern void native_fn_02221ec0(void);
extern void native_fn_02222030(void);


asm u32 native_ov000_022220ac (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r4, [pc, #0x70]
    mov r0, #1
L_022220b8:
    ldr r1, [r4, #0x18]
    cmp r1, #7
    addls pc, pc, r1, lsl #2
    b L_02222118
    dcd 0xea000012
    dcd 0xea000011
    dcd 0xea000004
    dcd 0xea000005
    dcd 0xea000006
    dcd 0xea000007
    dcd 0xea000008
    dcd 0xea000009
    bl native_fn_02221cb4
    b L_02222118
    bl native_fn_02221dac
    b L_02222118
    bl native_fn_02221dd4
    b L_02222118
    bl native_fn_02221ec0
    b L_02222118
    bl native_fn_02222030
    b L_02222118
    mov r0, #1
    ldmia sp!, {r4, pc}
L_02222118:
    cmp r0, #0
    bne L_022220b8
    mov r0, #0
    ldmia sp!, {r4, pc}
    dcd 0x02246438
}
