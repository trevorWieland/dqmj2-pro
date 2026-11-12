/* ov000 row 0x021f9768: 132 bytes.
 *
 * What it does: 33 instructions; 4 call(s) to 0x02215698, 0x021f97e4, 0x0206d250, +1 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x18 -> +0x7c
 *   back edge +0x78 -> +0x24
 *   test +0x14 cmp r1, #0
 *   test +0x54 cmp r0, #0
 *   test +0x6c cmp r1, r0, asr #24
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f9768; the literal pool and
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

extern void native_fn_02215698(void);
extern void native_fn_0206d250(void);
extern void native_fn_0204b920(void);


asm u32 native_ov000_021f9768 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    bl native_fn_02215698
    add r7, r0, #1024
    ldrsb r1, [r7, #149]
    mov r4, #0
    cmp r1, #0
    ble ov000_021f9768_L7c
    add r5, r0, #160
    mov r6, #40
ov000_021f9768_L24:
    ldrsb r0, [r5, #6]
    bl native_fn_0206d250
    add r0, r0, #1
    mov r2, r0, lsl #24
    ldrb r1, [r5, #0x5]
    mov r12, r2, asr #24
    ldrb r0, [r5, #0x4]
    mla r3, r12, r6, r1
    add r2, r0, #40
    and r2, r2, #255
    and r3, r3, #255
    bl native_fn_0204b920
    cmp r0, #0
    movne r0, r4
    ldmneia sp!, {r3, r4, r5, r6, r7, pc}
    ldrsb r1, [r7, #149]
    add r0, r4, #1
    mov r0, r0, lsl #24
    cmp r1, r0, asr #24
    add r5, r5, #8
    mov r4, r0, asr #24
    bgt ov000_021f9768_L24
ov000_021f9768_L7c:
    mvn r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
