/* ov000 row 0x0222390c: 116 bytes.
 *
 * What it does: 29 instructions; 5 call(s) to 0x02049ad0, 0x022238c0, 0x02223c40, +2 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x1c -> +0x5c
 *   branch +0x2c -> +0x5c
 *   back edge +0x6c -> +0x08
 *   test +0x18 cmp r0, #0
 *   test +0x28 cmp r0, #127
 *   test +0x68 cmp r5, #31
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222390c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02049ad0(void);
extern void native_fn_022238c0(void);
extern void native_fn_02223c40(void);
extern void native_fn_0206006c(void);


asm u32 native_ov000_0222390c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, #0
ov000_0222390c_L8:
    mov r0, r5
    bl native_fn_02049ad0
    mov r4, r0
    ldr r0, [r4]
    cmp r0, #0
    beq ov000_0222390c_L5c
    ldrsb r0, [r4, #5]
    bl native_fn_022238c0
    cmp r0, #127
    beq ov000_0222390c_L5c
    ldr r1, [r4]
    mov r0, r0, lsl #24
    ldr r4, [r1, #0x4]
    mov r0, r0, asr #24
    bl native_fn_02223c40
    ldrsb r1, [r4, #31]
    str r1, [sp]
    ldrsb r1, [r4, #28]
    ldrsb r2, [r4, #29]
    ldrsb r3, [r4, #30]
    bl native_fn_0206006c
ov000_0222390c_L5c:
    add r0, r5, #1
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    cmp r5, #31
    blt ov000_0222390c_L8
    ldmia sp!, {r3, r4, r5, pc}
}
