/* ov001 row 0x021f3178: 316 bytes.
 *
 * What it does: 76 instructions; 12 call(s) to 0x0207afec, 0x021db438, 0x021f32a0, +9 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 12 calls (76 instructions, 12 calls, 4 branches, 10 back edges, 3 literal slots).
 *
 *   pool +0x130 -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   pool +0x134 -> constant 0x0b60b60b (image word 0x0b60b60b)
 *   pool +0x138 -> constant 0x55555556 (image word 0x55555556)
 *   branch +0x2c -> +0x44
 *   branch +0x4c -> +0x128
 *   branch +0x64 -> +0x118
 *   branch +0x78 -> +0x118
 *   branch +0x90 -> +0xa8
 *   branch +0xa4 -> +0xb4
 *   back edge +0x124 -> +0x5c
 *   test +0x24 cmp r0, #1
 *   test +0x44 cmp r7, #0
 *   test +0x60 cmp r0, #0
 *   test +0x74 cmp r0, #0
 *   test +0x88 cmp r0, #0
 *   test +0x11c cmp r6, r7
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f3178; the literal pool and
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

extern void native_fn_0207afec(void);
extern void native_fn_021db438(void);
extern void native_fn_021f307c(void);
extern void native_fn_02025a28(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);
extern void native_fn_021d96d4(void);


asm u32 native_ov001_021f3178 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r9, r1
    mov r10, r0
    mov r0, r9
    mov r8, #0
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #16
    mov r0, r0, lsr #28
    cmp r0, #1
    movne r7, #1
    bne ov001_021f3178_L44
    ldrb r0, [r10, #0x31e]
    mov r1, r8
    bl native_fn_021db438
    mov r10, r0
    mov r7, #3
ov001_021f3178_L44:
    cmp r7, #0
    mov r6, #0
    ble ov001_021f3178_L128
    ldr r5, =0x020d3fe0
    ldr r4, =0x0b60b60b
    ldr r11, =0x55555556
ov001_021f3178_L5c:
    ldrb r0, [r10, #0x31c]
    cmp r0, #0
    beq ov001_021f3178_L118
    mov r0, r10
    mov r1, r9
    bl native_fn_021f307c
    cmp r0, #0
    beq ov001_021f3178_L118
    add r0, r10, #768
    ldrsh r0, [r0, #32]
    mov r0, r0, lsl #5
    cmp r0, #0
    mov r0, r0, lsl #12
    ble ov001_021f3178_La8
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov001_021f3178_Lb4
ov001_021f3178_La8:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov001_021f3178_Lb4:
    bl native_fn_020259b4
    umull r8, r3, r0, r4
    adds r1, r8, #0
    mov r1, #182
    mla r3, r0, r1, r3
    mov r2, r0, asr #31
    mla r3, r2, r4, r3
    mov r0, #2048
    adc r0, r3, r0
    mov r0, r0, lsl #4
    mov r0, r0, lsr #16
    mov r0, r0, asr #4
    add r0, r5, r0, lsl #2
    ldrsh r1, [r0, #2]
    mov r0, r10
    rsb r1, r1, #0
    add r1, r1, #4096
    mov r1, r1, asr #8
    mov r2, r1, lsl #1
    smull r1, r3, r11, r2
    add r3, r3, r2, lsr #31
    add r1, r3, #4
    and r1, r1, #255
    bl native_fn_021d96d4
    mov r8, #1
ov001_021f3178_L118:
    add r6, r6, #1
    cmp r6, r7
    add r10, r10, #1088
    blt ov001_021f3178_L5c
ov001_021f3178_L128:
    mov r0, r8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
