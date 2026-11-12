/* ov000 row 0x02224e38: 172 bytes.
 *
 * What it does: 42 instructions and 3 call(s), then a 12-entry dispatch through an inline branch table at 0x02224e60 (dispatch word at 0x02224e58)
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

extern void native_fn_02049ae4(void);
extern void native_fn_02049d50(void);
extern void native_fn_020c42c8(void);


asm u32 native_ov000_02224e38 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r1, [pc, #0x9c]
    mov r0, #5
    ldrsb r2, [r1, #24]
    cmp r2, #15
    bgt L_02224e90
    bge L_02224ed0
    cmp r2, #11
    addls pc, pc, r2, lsl #2
    ldmia sp!, {r3, pc}
    dcd 0xe8bd8008
    dcd 0xe8bd8008
    dcd 0xe8bd8008
    dcd 0xea000009
    dcd 0xe8bd8008
    dcd 0xe8bd8008
    dcd 0xe8bd8008
    dcd 0xea000010
    dcd 0xe8bd8008
    dcd 0xe8bd8008
    dcd 0xe8bd8008
    dcd 0xe8bd8008
L_02224e90:
    cmp r2, #23
    ldmia sp!, {r3, pc}
    bl native_fn_02049ae4
    ldr r0, [r0, #0x4]
    cmp r0, #0
    beq L_02224eb0
    bl native_fn_02049d50
    bl native_fn_020c42c8
L_02224eb0:
    ldr r0, [pc, #0x28]
    mov r1, #2
    strb r1, [r0, #0x1a]
    mov r0, #6
    ldmia sp!, {r3, pc}
    mov r2, #2
    strb r2, [r1, #0x1a]
    ldmia sp!, {r3, pc}
L_02224ed0:
    mov r0, #11
    strb r0, [r1, #0x1a]
    mov r0, #6
    ldmia sp!, {r3, pc}
    dcd 0x022468b8
}
