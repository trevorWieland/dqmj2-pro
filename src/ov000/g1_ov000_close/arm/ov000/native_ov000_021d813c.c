/* ov000 row 0x021d813c: 420 bytes.
 *
 * What it does: 102 instructions; 8 call(s) to 0x02067d54, 0x021d82bc, 0x021d822c, +5 more; loops (back edge at +0x3c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x198 -> constant 0x022301b8 (image word 0x022301b8)
 *   pool +0x19c -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   pool +0x1a0 -> constant 0x022300f0 (image word 0x022300f0)
 *   branch +0x50 -> +0x180
 *   branch +0x6c -> +0x7c
 *   branch +0x74 -> +0x140
 *   branch +0x78 -> +0x16c
 *   branch +0xa8 -> +0xf0
 *   branch +0xbc -> +0xf0
 *   branch +0xc8 -> +0xdc
 *   branch +0xd8 -> +0xe8
 *   branch +0x13c -> +0x16c
 *   back edge +0x17c -> +0x64
 *   back edge +0x18c -> +0x10
 *   test +0x2c cmp r1, r0
 *   test +0x48 cmp r0, #0
 *   test +0x68 cmp r0, #0
 *   test +0x70 cmp r0, #1
 *   test +0x80 cmp r7, #0
 *   test +0xa4 cmp r0, #0
 *   test +0xb8 cmp r0, #0
 *   test +0xc4 cmp r8, #7
 *   test +0x160 tst r0, #255
 *   test +0x178 cmp r8, r0
 *   test +0x184 cmp r7, #2
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d813c; the literal pool and
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

extern void native_fn_02067d54(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048a44(void);


asm u32 native_ov000_021d813c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r9, =0x022301b8
    mov r6, #1
    mov r7, #0
ov000_021d813c_L10:
    ldr r0, [r9, #0xa4]
    ldr r1, [r9, #0xa8]
    mov r0, r0, asr #5
    add r0, r0, #1
    add r1, r1, r0
    str r1, [r9, #0xa8]
    ldr r0, [r9, #0xa4]
    cmp r1, r0
    strgt r0, [r9, #0xa8]
    ldr r0, [r9, #0xa8]
    movle r6, #0
    bl native_fn_02067d54
    add r0, r0, #1
    str r0, [r9, #0xac]
    cmp r0, #0
    mov r8, #0
    ble ov000_021d813c_L180
    ldr r4, =0x020d3fe0
    mov r10, r9
    mov r11, r8
    mvn r5, #0
ov000_021d813c_L64:
    ldrb r0, [r10, #0x10]
    cmp r0, #0
    beq ov000_021d813c_L7c
    cmp r0, #1
    beq ov000_021d813c_L140
    b ov000_021d813c_L16c
ov000_021d813c_L7c:
    ldr r1, [r10]
    cmp r7, #0
    ldr r0, [r1, #0x7c]
    orr r0, r0, #2
    str r0, [r1, #0x7c]
    ldrh r0, [r10, #12]
    subeq r0, r0, #2048
    addne r0, r0, #2048
    strh r0, [r10, #12]
    ldrsh r0, [r10, #14]
    cmp r0, #0
    ble ov000_021d813c_Lf0
    sub r0, r0, #3
    strh r0, [r10, #14]
    ldrsh r0, [r10, #14]
    cmp r0, #0
    bge ov000_021d813c_Lf0
    strh r11, [r10, #14]
    cmp r8, #7
    bne ov000_021d813c_Ldc
    ldr r0, =0x022300f0
    mov r1, #1
    str r1, [r0, r7, lsl #2]
    b ov000_021d813c_Le8
ov000_021d813c_Ldc:
    mov r0, r5
    add r1, r5, #536
    bl native_fn_0205e7a8
ov000_021d813c_Le8:
    mov r0, #1
    strb r0, [r10, #0x10]
ov000_021d813c_Lf0:
    ldrh r1, [r10, #12]
    ldrsh r2, [r10, #14]
    ldr r0, [r10]
    mov r1, r1, asr #4
    mov r12, r1, lsl #1
    mov r3, r12, lsl #1
    ldrsh r6, [r4, r3]
    add r3, r4, r12, lsl #1
    ldrsh r3, [r3, #2]
    smulbb r6, r2, r6
    ldr r1, [r10, #0x4]
    smulbb r2, r2, r3
    ldr r3, [r10, #0x8]
    add r1, r1, r6, asr #4
    add r2, r3, r2, asr #4
    mov r1, r1, asr #8
    mov r2, r2, asr #8
    bl native_fn_02048a60
    mov r6, #0
    b ov000_021d813c_L16c
ov000_021d813c_L140:
    ldr r0, [r10]
    mov r1, #1
    add r0, r0, #8
    bl native_fn_02048a44
    ldrb r0, [r10, #0x11]
    mov r6, #0
    sub r0, r0, #1
    strb r0, [r10, #0x11]
    tst r0, #255
    moveq r0, #2
    streqb r0, [r10, #0x10]
ov000_021d813c_L16c:
    add r10, r10, #20
    add r8, r8, #1
    ldr r0, [r9, #0xac]
    cmp r8, r0
    blt ov000_021d813c_L64
ov000_021d813c_L180:
    add r7, r7, #1
    cmp r7, #2
    add r9, r9, #176
    blt ov000_021d813c_L10
    mov r0, r6
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
