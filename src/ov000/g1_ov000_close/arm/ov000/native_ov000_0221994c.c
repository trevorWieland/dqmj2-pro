/* ov000 row 0x0221994c: 108 bytes.
 *
 * What it does: 26 instructions; 3 call(s) to 0x021df1f0, 0x0205f98c, 0x021df3bc; loops (back edge at +0x08); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x68 -> constant 0x02245ee4 (image word 0x02245ee4)
 *   branch +0x40 -> +0x4c
 *   branch +0x48 -> +0x50
 *   test +0x30 cmp r0, #255
 *   test +0x3c cmp r0, #192
 *   test +0x44 cmp r0, #0
 *   test +0x54 cmp r6, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221994c; the literal pool and
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

extern void native_fn_021df1f0(void);
extern void native_fn_0205f98c(void);
extern void native_fn_021df3bc(void);


asm u32 native_ov000_0221994c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, #1
    bl native_fn_021df1f0
    ldr r1, =0x02245ee4
    mov r5, r0
    ldr r0, [r1, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    mov r4, r0
    mov r0, r5
    bl native_fn_021df3bc
    ldrb r0, [r0, #0x3]
    cmp r0, #255
    ldr r0, [r4, #0x70]
    moveq r6, #0
    cmp r0, #192
    bgt ov000_0221994c_L4c
    cmp r0, #0
    bge ov000_0221994c_L50
ov000_0221994c_L4c:
    mov r6, #0
ov000_0221994c_L50:
    ldr r0, [r4, #0x7c]
    cmp r6, #0
    orrne r0, r0, #2
    biceq r0, r0, #2
    str r0, [r4, #0x7c]
    ldmia sp!, {r4, r5, r6, pc}
}
