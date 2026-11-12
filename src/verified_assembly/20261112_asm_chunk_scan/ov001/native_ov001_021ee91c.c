/* ov001 row 0x021ee91c: 224 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (2 loads, 2 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xdc -> native_data_0222df1c (image word 0x0222df1c)
 *   branch +0x68 -> +0xd0
 *   test +0x64 cmp r0, #0
 *   test +0x7c cmp r4, #0
 *   8 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ee91c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0222df1c[];
extern void native_fn_02041f74(void);
extern void native_fn_020299ac(void);
extern void native_fn_02210f64(void);


asm u32 native_ov001_021ee91c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #64
    ldr lr, =native_data_0222df1c
    mvn r6, #99
    mov r5, r0
    mov r4, r1
    ldmia lr!, {r0, r1, r2, r3}
    add r12, sp, #16
    stmia r12!, {r0, r1, r2, r3}
    ldmia lr!, {r0, r1, r2, r3}
    stmia r12!, {r0, r1, r2, r3}
    ldr r0, [lr]
    add r1, sp, #52
    str r0, [r12]
    mov r0, r5
    str r6, [sp, #0xc]
    str r6, [sp, #0x8]
    bl native_fn_02041f74
    ldr r1, [sp, #0x38]
    add r0, sp, #52
    add r1, r1, #4096
    str r1, [sp, #0x38]
    add r1, sp, #12
    add r2, sp, #8
    bl native_fn_020299ac
    cmp r0, #0
    beq ov001_021ee91c_Ld0
    ldr r1, [sp, #0xc]
    add r0, r5, #768
    strh r1, [r0, #64]
    ldr r1, [sp, #0x8]
    cmp r4, #0
    strh r1, [r0, #66]
    movge r0, #87
    movlt r0, #119
    and r0, r0, #255
    str r0, [sp]
    mov r0, #0
    str r0, [sp, #0x4]
    ldr r1, [sp, #0x8]
    ldr r0, [sp, #0xc]
    mov r2, r1, lsl #16
    add r1, sp, #16
    add r3, r4, #4
    ldr r3, [r1, r3, lsl #2]
    mov r0, r0, lsl #16
    mov r1, r0, asr #16
    mov r0, r3, lsl #16
    mov r0, r0, asr #16
    mov r2, r2, asr #16
    mov r3, #10
    bl native_fn_02210f64
ov001_021ee91c_Ld0:
    mov r0, #0
    add sp, sp, #64
    ldmia sp!, {r4, r5, r6, pc}
}
