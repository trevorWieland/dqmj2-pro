/* main row 0x02053cb4: 76 bytes.
 *
 * Decoded shape: 2 calls, no loop.
 *
 *   call +0x0c -> native_fn_02040424
 *   call +0x14 -> native_fn_021dd4d8
 *   memory +0x10 ldrsb r1, [r5, #8]
 *   memory +0x18 ldrb r1, [r4, #3]
 *   memory +0x28 ldr r3, [lr, ip]
 *   memory +0x2c ldr r1, [r5, #4]
 *   memory +0x38 str r1, [lr, ip]
 *   memory +0x3c ldrb r1, [r4, #3]
 *   memory +0x44 strb r2, [r0, #0x477]
 *   2 store instruction(s)
 *
 * Why transcribed rather than written as C: donor shape uses `smulbb` and an `ldrsb` argument; the target
 * uses `mul` and passes the field address
 * Recorded in docs/authoring/2026-11-11-main-rows-2.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02053cb4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts
 * the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02040424(void);
extern void native_fn_021dd4d8(void);


asm u32 native_main_02053cb4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r1
    mov r4, r0
    bl native_fn_02040424
    ldrsb r1, [r5, #8]
    bl native_fn_021dd4d8
    ldrb r1, [r4, #3]
    mov r0, #0x10c
    add lr, r4, #0x470
    mul ip, r1, r0
    ldr r3, [lr, ip]
    ldr r1, [r5, #4]
    mov r2, #0
    add r1, r3, r1
    str r1, [lr, ip]
    ldrb r1, [r4, #3]
    mla r0, r1, r0, r4
    strb r2, [r0, #0x477]
    ldmia sp!, {r3, r4, r5, pc}
}
