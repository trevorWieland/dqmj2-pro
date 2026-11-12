/* ov001 row 0x02205c88: 136 bytes.
 *
 * What it does: 34 instructions; 6 call(s) to 0x0205f98c, 0x022023a8, 0x02048a60, +3 more; loops (back edge at +0x28); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 6 calls (34 instructions, 6 calls, 0 branches, 6 back edges, 0 literal slots).
 *
 *   back edge +0x80 -> +0x20
 *   test +0x10 cmp r0, #0
 *   test +0x7c cmp r6, r0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02205c88; the literal pool and
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

extern void native_fn_0205f98c(void);
extern void native_fn_022023a8(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a9c(void);


asm u32 native_ov001_02205c88 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r8, r0
    ldr r0, [r8, #0x2c]
    mov r6, #0
    cmp r0, #0
    ldmleia sp!, {r4, r5, r6, r7, r8, pc}
    mov r7, r6
    mov r4, #106
ov001_02205c88_L20:
    ldr r0, [r8, #0x1c]
    and r1, r6, #255
    bl native_fn_0205f98c
    mov r1, r4
    mov r5, r0
    bl native_fn_022023a8
    ldrsh r2, [r8, #22]
    ldrsh r1, [r8, #20]
    mov r0, r5
    add r2, r2, r7
    bl native_fn_02048a60
    ldrb r1, [r8, #0x20]
    mov r0, r5
    bl native_fn_02048a94
    mov r0, r5
    ldrb r1, [r8, #0x21]
    bl native_fn_02048a9c
    ldr r0, [r5, #0x7c]
    add r7, r7, #40
    orr r0, r0, #2
    str r0, [r5, #0x7c]
    add r6, r6, #1
    ldr r0, [r8, #0x2c]
    cmp r6, r0
    blt ov001_02205c88_L20
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
