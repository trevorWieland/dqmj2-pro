/* ov000 row 0x0220a650: 152 bytes.
 *
 * What it does: 38 instructions; 8 call(s) to 0x0220a0d0, 0x02209c68, 0x020c56b4, +5 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x24 -> +0x78
 *   branch +0x54 -> +0x70
 *   branch +0x74 -> +0x90
 *   test +0x4c cmp r4, #3
 *   test +0x50 cmpne r4, #6
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220a650; the literal pool and
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

extern void native_fn_0220a0d0(void);
extern void native_fn_02209c68(void);
extern void native_fn_020c56b4(void);
extern void native_fn_0221089c(void);
extern void native_fn_02042c0c(void);


asm u32 native_ov000_0220a650 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r4, #0
    bl native_fn_0220a0d0
    mov r2, #409600
    subs r0, r2, r0
    mov r0, r4
    sbcs r0, r0, r1
    mov r0, r5
    bge ov000_0220a650_L78
    mov r1, #3
    bl native_fn_02209c68
    add r0, r5, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r4, [r0, #0x7]
    mov r0, r5
    mov r1, #1
    bl native_fn_0221089c
    cmp r4, #3
    cmpne r4, #6
    bne ov000_0220a650_L70
    mov r0, r5
    mov r1, #0
    bl native_fn_02042c0c
    mov r0, r5
    mov r1, #0
    bl native_fn_0221089c
ov000_0220a650_L70:
    mov r4, #1
    b ov000_0220a650_L90
ov000_0220a650_L78:
    mov r1, #10
    bl native_fn_02209c68
    mov r1, r4
    mov r0, r5
    strb r1, [r5, #0x1e2]
    bl native_fn_0221089c
ov000_0220a650_L90:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
