/* ov000 row 0x02222c90: 224 bytes.
 *
 * What it does: 55 instructions and 9 call(s), then a 14-entry dispatch through an inline branch table at 0x02222cd8 (dispatch word at 0x02222cd0)
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

extern void native_fn_0202a32c(void);
extern void native_fn_0202a164(void);
extern void native_fn_02223f24(void);
extern void native_fn_0206258c(void);
extern void native_fn_020c1898(void);
extern void native_fn_02223318(void);


asm u32 native_ov000_02222c90 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, [pc, #0xd0]
    mov r4, #7
    ldr r1, [r0, #0x8]
    cmp r1, #8
    beq L_02222cc8
    mov r0, #8
    mov r4, r1
    bl native_fn_0202a32c
    cmp r0, #1
    bne L_02222d5c
    mov r0, #8
    bl native_fn_0202a164
    b L_02222d5c
L_02222cc8:
    bl native_fn_02223f24
    cmp r0, #13
    addls pc, pc, r0, lsl #2
    b L_02222d3c
    dcd 0xea000017
    dcd 0xea000016
    dcd 0xea000015
    dcd 0xea000014
    dcd 0xea000013
    dcd 0xea000012
    dcd 0xea000019
    dcd 0xea000018
    dcd 0xea000017
    dcd 0xea000016
    dcd 0xea000004
    dcd 0xea000007
    dcd 0xea000000
    dcd 0xea000007
    mov r4, #3
    b L_02222d5c
    mov r0, #0
    bl native_fn_0206258c
    mov r4, #2
    b L_02222d5c
    mov r4, #15
    b L_02222d5c
    mov r0, #1
    bl native_fn_020c1898
    b L_02222d5c
L_02222d3c:
    mov r0, #8
    bl native_fn_0202a32c
    cmp r0, #1
    bne L_02222d54
    mov r0, #8
    bl native_fn_0202a164
L_02222d54:
    mov r0, #1
    bl native_fn_020c1898
L_02222d5c:
    mov r0, #0
    bl native_fn_02223318
    mov r0, r4
    ldmia sp!, {r4, pc}
    dcd 0x02246574
}
