/* ov000 row 0x0220d72c: 140 bytes.
 *
 * What it does: 35 instructions and 7 call(s), then a 6-entry dispatch through an inline branch table at 0x0220d750 (dispatch word at 0x0220d748)
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

extern void native_fn_020c56b4(void);
extern void native_fn_0220cd28(void);
extern void native_fn_0220ceb4(void);
extern void native_fn_0220cf90(void);
extern void native_fn_0220d074(void);
extern void native_fn_0220d46c(void);
extern void native_fn_02209c68(void);


asm u32 native_ov000_0220d72c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    add r0, r4, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x9]
    cmp r0, #5
    addls pc, pc, r0, lsl #2
    b L_0220d7a4
    dcd 0xea000013
    dcd 0xea000003
    dcd 0xea000005
    dcd 0xea000007
    dcd 0xea000009
    dcd 0xea00000b
    mov r0, r4
    bl native_fn_0220cd28
    b L_0220d7b0
    mov r0, r4
    bl native_fn_0220ceb4
    b L_0220d7b0
    mov r0, r4
    bl native_fn_0220cf90
    b L_0220d7b0
    mov r0, r4
    bl native_fn_0220d074
    b L_0220d7b0
    mov r0, r4
    bl native_fn_0220d46c
    b L_0220d7b0
L_0220d7a4:
    mov r0, r4
    mov r1, #6
    bl native_fn_02209c68
L_0220d7b0:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
