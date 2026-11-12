/* ov000 row 0x021f5518: 152 bytes.
 *
 * What it does: 38 instructions and 5 call(s), then a 6-entry dispatch through an inline branch table at 0x021f553c (dispatch word at 0x021f5534)
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

extern void native_fn_02061944(void);
extern void native_fn_02065818(void);


asm u32 native_ov000_021f5518 (register u32 a0)
{
L_021f5518:
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r6, r0
    mov r5, r1
    mov r4, r2
    bl native_fn_02061944
    mov r7, r0
    cmp r6, #5
    addls pc, pc, r6, lsl #2
    b L_021f5594
    dcd 0xea000014
    dcd 0xea000013
    dcd 0xea000002
    dcd 0xea000006
    dcd 0xea000005
    dcd 0xea000004
    mov r1, r5
    mov r2, r4
    add r0, r7, #40
    bl native_fn_02065818
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
    mov r1, r5
    mov r2, r4
    mov r0, #2
    bl L_021f5518
    add r1, r7, #16
    mov r0, #12
    mla r0, r6, r0, r1
    mov r1, r5
    mov r2, r4
    bl native_fn_02065818
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
L_021f5594:
    add r1, r7, #16
    mov r0, #12
    mla r0, r6, r0, r1
    mov r1, r5
    mov r2, r4
    bl native_fn_02065818
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
