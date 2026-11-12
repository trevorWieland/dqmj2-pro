/* ov000 row 0x021e31f0: 304 bytes.
 *
 * What it does: 74 instructions and 7 call(s), then a 14-entry dispatch through an inline branch table at 0x021e320c (dispatch word at 0x021e3204)
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

extern void native_fn_0205cba4(void);
extern void native_fn_021e3370(void);


asm u32 native_ov000_021e31f0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r4, r1
    cmp r5, #13
    mvn r2, #0
    addls pc, pc, r5, lsl #2
    b L_021e32f8
    dcd 0xea000039
    dcd 0xea000038
    dcd 0xea000037
    dcd 0xea000036
    dcd 0xea000035
    dcd 0xea000034
    dcd 0xea00000e
    dcd 0xea000032
    dcd 0xea000031
    dcd 0xea000003
    dcd 0xea00002f
    dcd 0xea00002e
    dcd 0xea000015
    dcd 0xea000020
    ldr r1, [pc, #0xcc]
    mov r2, r4
    bl native_fn_0205cba4
    mov r0, r0, lsl #24
    ldr r1, [pc, #0xc0]
    mov r2, r0, asr #24
    strb r2, [r1]
    b L_021e3310
    mov r0, #2
    bl native_fn_021e3370
    mov r0, #3
    bl native_fn_021e3370
    ldr r1, [pc, #0x9c]
    mov r0, r5
    mov r2, r4
    bl native_fn_0205cba4
    mov r0, r0, lsl #24
    ldr r1, [pc, #0x8c]
    mov r2, r0, asr #24
    strb r2, [r1, #0x1]
    b L_021e3310
    ldr r1, [pc, #0x7c]
    ldrsb r1, [r1, #1]
    cmp r1, #0
    bge L_021e3310
    ldr r1, [pc, #0x68]
    mov r2, r4
    bl native_fn_0205cba4
    mov r0, r0, lsl #24
    ldr r1, [pc, #0x5c]
    mov r2, r0, asr #24
    strb r2, [r1, #0x2]
    b L_021e3310
    ldr r1, [pc, #0x4c]
    ldrsb r1, [r1, #1]
    cmp r1, #0
    bge L_021e3310
    ldr r1, [pc, #0x38]
    mov r2, r4
    bl native_fn_0205cba4
    mov r0, r0, lsl #24
    ldr r1, [pc, #0x2c]
    mov r2, r0, asr #24
    strb r2, [r1, #0x3]
    b L_021e3310
L_021e32f8:
    ldr r1, [pc, #0x18]
    mov r0, r5
    mov r2, r4
    bl native_fn_0205cba4
    mov r0, r0, lsl #24
    mov r2, r0, asr #24
L_021e3310:
    mov r0, r2
    ldmia sp!, {r3, r4, r5, pc}
    dcd 0x022322d4
    dcd 0x022322d0
}
