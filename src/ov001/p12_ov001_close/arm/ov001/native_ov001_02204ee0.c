/* ov001 row 0x02204ee0: 168 bytes.
 *
 * What it does: 42 instructions; 3 call(s) to 0x0205f98c, 0x022023a8, 0x02048a60; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 3 calls (42 instructions, 3 calls, 3 branches, 3 back edges, 0 literal slots).
 *
 *   branch +0x60 -> +0x78
 *   branch +0x74 -> +0x90
 *   branch +0x7c -> +0x90
 *   test +0x5c tst r0, #2
 *   test +0x78 tst r0, #1
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02204ee0; the literal pool and
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


asm u32 native_ov001_02204ee0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r5, r0
    mov r4, r1
    ldr r0, [r5, #0x1c]
    and r1, r4, #255
    mov r7, r2
    bl native_fn_0205f98c
    ldr r5, [r5, #0x40]
    mov r1, #12
    mul r6, r4, r1
    add r3, r5, #2
    ldrsb r1, [r3, r6]
    add r2, r5, #6
    mov r4, r0
    add r1, r1, r7
    strb r1, [r3, r6]
    ldrb r1, [r2, r6]
    sub r1, r1, r7
    strb r1, [r2, r6]
    ldrb r1, [r3, r6]
    bl native_fn_022023a8
    add r0, r5, r6
    ldrb r0, [r0, #0x7]
    tst r0, #2
    beq ov001_02204ee0_L78
    add r1, r5, #8
    ldrsh r0, [r1, r6]
    sub r0, r0, r7, lsl #3
    strh r0, [r1, r6]
    b ov001_02204ee0_L90
ov001_02204ee0_L78:
    tst r0, #1
    beq ov001_02204ee0_L90
    add r1, r5, #10
    ldrsh r0, [r1, r6]
    sub r0, r0, r7, lsl #3
    strh r0, [r1, r6]
ov001_02204ee0_L90:
    add r0, r5, r6
    ldrsh r1, [r0, #8]
    ldrsh r2, [r0, #10]
    mov r0, r4
    bl native_fn_02048a60
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
