/* ov000 row 0x021f77b4: 196 bytes.
 *
 * What it does: 49 instructions and 7 call(s), then a 6-entry dispatch through an inline branch table at 0x021f77d8 (dispatch word at 0x021f77d0)
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


asm u32 native_ov000_021f77b4 (register u32 a0)
{
L_021f77b4:
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, r0
    mov r5, r1
    mov r4, r2
    bl native_fn_02061944
    mov r6, r0
    cmp r7, #5
    addls pc, pc, r7, lsl #2
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
    dcd 0xea000004
    dcd 0xea000008
    dcd 0xea000014
    dcd 0xea000013
    dcd 0xea000012
    dcd 0xea00001c
    mov r1, r5
    mov r2, r4
    add r0, r6, #16
    bl native_fn_02065818
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
    add r0, r6, #512
    ldrsb r0, [r0, #105]
    cmp r0, #27
    ldmgeia sp!, {r3, r4, r5, r6, r7, pc}
    mov r1, r5
    mov r2, r4
    mov r0, #0
    bl L_021f77b4
    mov r1, r5
    mov r2, r4
    add r0, r6, #28
    bl native_fn_02065818
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
    mov r1, r5
    mov r2, r4
    mov r0, #0
    bl L_021f77b4
    add r1, r6, #16
    mov r0, #12
    mla r0, r7, r0, r1
    mov r1, r5
    mov r2, r4
    bl native_fn_02065818
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
    mov r1, r5
    mov r2, r4
    add r0, r6, #76
    bl native_fn_02065818
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
