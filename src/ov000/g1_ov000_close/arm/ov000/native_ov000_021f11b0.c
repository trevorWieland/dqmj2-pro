/* ov000 row 0x021f11b0: 232 bytes.
 *
 * What it does: 56 instructions and 9 call(s), then a 7-entry dispatch through an inline branch table at 0x021f11e8 (dispatch word at 0x021f11e0)
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

extern void native_fn_021f3194(void);
extern void native_fn_021f2fbc(void);
extern void native_fn_021f2a7c(void);
extern void native_fn_021f31a4(void);
extern void native_fn_021f2a64(void);


asm u32 native_ov000_021f11b0 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r1, [pc, #0xd4]
    mov r2, #1
    ldr lr, [r1, #0x8]
    add r0, lr, #6400
    ldrsb r3, [r0, #31]
    ldrsb r12, [lr, #32]
    cmp r3, #6
    strb r3, [lr, #0x20]
    ldr r0, [r1, #0x8]
    add r0, r0, #4096
    strb r2, [r0, #0x91d]
    addls pc, pc, r3, lsl #2
    b L_021f1268
    dcd 0xea00001e
    dcd 0xea000004
    dcd 0xea000014
    dcd 0xea000002
    dcd 0xea000012
    dcd 0xea000000
    dcd 0xea000010
    cmp r12, #6
    addls pc, pc, r12, lsl #2
    b L_021f1240
    b L_021f1240
    b L_021f1240
    b L_021f122c
    b L_021f1240
    b L_021f122c
    b L_021f1240
    b L_021f122c
L_021f122c:
    bl native_fn_021f3194
    bl native_fn_021f2fbc
    mov r0, #0
    bl native_fn_021f2a7c
    b L_021f1274
L_021f1240:
    bl native_fn_021f31a4
    b L_021f1274
    cmp r12, #1
    cmpne r12, #3
    cmpne r12, #5
    bne L_021f1260
    bl native_fn_021f3194
    b L_021f1274
L_021f1260:
    bl native_fn_021f31a4
    b L_021f1274
L_021f1268:
    bl native_fn_021f31a4
    mov r0, #0
    bl native_fn_021f2a7c
L_021f1274:
    mov r0, #0
    bl native_fn_021f2a64
    ldr r0, [pc, #0x10]
    mov r1, #1
    str r1, [r0, #0xc84]
    mov r0, #4
    ldmia sp!, {r3, pc}
    dcd 0x02236d98
    dcd 0x02101ae8
}
