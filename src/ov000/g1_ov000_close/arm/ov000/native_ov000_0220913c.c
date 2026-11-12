/* ov000 row 0x0220913c: 264 bytes.
 *
 * What it does: 65 instructions; 8 call(s) to 0x02209100, 0x02208e14, 0x02084924, +5 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x104 -> constant 0x02238514 (image word 0x02238514)
 *   branch +0x20 -> +0x8c
 *   branch +0x78 -> +0xf0
 *   branch +0x88 -> +0xf0
 *   branch +0xe0 -> +0xf0
 *   test +0x1c cmp r7, #0
 *   test +0x70 cmp r0, #0
 *   test +0xd8 cmp r0, #0
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220913c; the literal pool and
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

extern void native_fn_02209100(void);
extern void native_fn_02208e14(void);
extern void native_fn_02084924(void);
extern void native_fn_02208ff8(void);
extern void native_fn_02208e8c(void);
extern void native_fn_0208497c(void);
extern void native_fn_02088578(void);


asm u32 native_ov000_0220913c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #24
    mov r7, r0
    mov r0, r1
    mov r6, r2
    mov r5, r3
    bl native_fn_02209100
    cmp r7, #0
    bne ov000_0220913c_L8c
    bl native_fn_02208e14
    ldr r0, [sp, #0x34]
    mov r1, #2
    and r0, r0, #255
    str r0, [sp]
    ldr r0, [sp, #0x30]
    str r1, [sp, #0x4]
    mov r1, #1
    str r1, [sp, #0x8]
    mov r12, #0
    str r12, [sp, #0xc]
    str r12, [sp, #0x10]
    and r1, r6, #255
    and r2, r5, #255
    and r3, r0, #255
    mov r0, #7
    str r12, [sp, #0x14]
    bl native_fn_02084924
    ldr r1, =0x02238514
    cmp r0, #0
    str r0, [r1, #0x4]
    beq ov000_0220913c_Lf0
    mov r1, #1
    bl native_fn_02208ff8
    mov r4, r0
    b ov000_0220913c_Lf0
ov000_0220913c_L8c:
    bl native_fn_02208e8c
    ldr r0, [sp, #0x34]
    mov r1, #2
    and r0, r0, #255
    str r0, [sp]
    ldr r0, [sp, #0x30]
    str r1, [sp, #0x4]
    mov r1, #1
    str r1, [sp, #0x8]
    mov r12, #0
    str r12, [sp, #0xc]
    str r12, [sp, #0x10]
    and r1, r6, #255
    and r2, r5, #255
    and r3, r0, #255
    mov r0, #7
    str r12, [sp, #0x14]
    bl native_fn_0208497c
    ldr r1, =0x02238514
    cmp r0, #0
    str r0, [r1]
    beq ov000_0220913c_Lf0
    mov r1, #1
    bl native_fn_02208ff8
    mov r4, r0
ov000_0220913c_Lf0:
    mov r0, #1
    bl native_fn_02088578
    mov r0, r4
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
