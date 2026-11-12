/* ov000 row 0x02218714: 164 bytes.
 *
 * What it does: 40 instructions; 9 call(s) to 0x0205f998, 0x0221863c, 0x0205f98c, +6 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa0 -> constant 0x02245f2c (image word 0x02245f2c)
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02218714; the literal pool and
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

extern void native_fn_0205f998(void);
extern void native_fn_0221863c(void);
extern void native_fn_0205f98c(void);
extern void native_fn_0203cfe0(void);
extern void native_fn_02219d70(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a9c(void);
extern void native_fn_0221993c(void);


asm u32 native_ov000_02218714 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r4, =0x02245f2c
    mov r0, r4
    bl native_fn_0205f998
    mov r1, #1
    mov r5, #214
    mov r3, #0
    mov r2, #6
    mov r0, r4
    str r1, [r4]
    strh r5, [r4, #20]
    strh r3, [r4, #22]
    strb r2, [r4, #0x20]
    strb r1, [r4, #0x21]
    bl native_fn_0221863c
    ldr r0, [r4, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    mov r5, r0
    bl native_fn_0203cfe0
    add r0, r0, #2
    and r1, r0, #255
    mov r0, r5
    bl native_fn_02219d70
    ldrsh r1, [r4, #20]
    ldrsh r2, [r4, #22]
    mov r0, r5
    bl native_fn_02048a60
    ldr r1, [r5, #0x7c]
    mov r0, r5
    orr r1, r1, #2
    str r1, [r5, #0x7c]
    ldrb r1, [r4, #0x20]
    bl native_fn_02048a94
    ldrb r1, [r4, #0x21]
    mov r0, r5
    bl native_fn_02048a9c
    mov r0, #1
    bl native_fn_0221993c
    ldmia sp!, {r3, r4, r5, pc}
}
