/* ov000 row 0x02221b50: 108 bytes.
 *
 * What it does: 24 instructions; 2 call(s) to 0x0205ffcc, 0x02221b68; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, r8, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> native_data_0222fb70 (image word 0x0222fb70)
 *   pool +0x64 -> constant 0x02246464 (image word 0x02246464)
 *   pool +0x68 -> constant 0x02246454 (image word 0x02246454)
 *   back edge +0x54 -> +0x18
 *   test +0x48 cmp r5, #21
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02221b50; the literal pool and
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

extern u8 native_data_0222fb70[];
extern void native_fn_0205ffcc(void);


asm u32 native_ov000_02221b50 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #4
    ldr r6, =native_data_0222fb70
    ldr r7, =0x02246464
    ldr r4, =0x02246454
    mov r5, #0
ov000_02221b50_L18:
    ldrb r8, [r6, #0x2]
    mov r0, r7
    ldr r1, [r4, r8, lsl #2]
    mov r3, r8
    str r1, [sp]
    ldrsb r1, [r6]
    ldrb r2, [r6, #0x1]
    bl native_fn_0205ffcc
    ldr r1, [r4, r8, lsl #2]
    add r5, r5, #1
    add r0, r1, r0
    str r0, [r4, r8, lsl #2]
    cmp r5, #21
    add r6, r6, #3
    add r7, r7, #12
    blt ov000_02221b50_L18
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
