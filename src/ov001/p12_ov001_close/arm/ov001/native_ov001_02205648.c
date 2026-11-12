/* ov001 row 0x02205648: 352 bytes.
 *
 * What it does: 88 instructions; 3 call(s) to 0x022056e4, 0x02204df0, 0x02204d60; loops (back edge at +0xb8); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill (88 instructions, 3 calls, 10 branches, 3 back edges, 0 literal slots).
 *
 *   branch +0x34 -> +0x48
 *   branch +0x44 -> +0x54
 *   branch +0x60 -> +0x7c
 *   branch +0x78 -> +0x9c
 *   branch +0x84 -> +0x9c
 *   branch +0xa4 -> +0xb0
 *   branch +0xe4 -> +0x150
 *   branch +0xf8 -> +0x150
 *   branch +0x100 -> +0x11c
 *   branch +0x118 -> +0x134
 *   back edge +0x14c -> +0x58
 *   test +0x18 cmp r9, r8
 *   test +0x30 cmp r9, r8
 *   test +0x58 cmp r9, r8
 *   test +0x7c cmp r9, r8
 *   test +0x9c cmp r5, #4
 *   test +0xa8 cmp r5, #1
 *   test +0xe0 cmp r0, r11
 *   test +0xf0 cmp r9, r8
 *   test +0xfc cmp r9, r8
 *   test +0x110 cmp r8, r0, asr #16
 *   test +0x128 cmp r8, r0, asr #16
 *   test +0x134 cmp r6, #0
 *   1 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02205648; the literal pool and
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

extern void native_fn_02204df0(void);
extern void native_fn_02204d60(void);


asm u32 native_ov001_02205648 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    str r1, [sp, #0xc]
    mov r10, r0
    mov r9, r2
    mov r8, r3
    cmp r9, r8
    ldr r7, [sp, #0x38]
    ldr r4, [r10, #0x40]
    addeq sp, sp, #16
    mvneq r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    cmp r9, r8
    bge ov001_02205648_L48
    add r0, r9, #8
    mov r0, r0, lsl #16
    mov r9, r0, asr #16
    b ov001_02205648_L54
ov001_02205648_L48:
    subgt r0, r9, #8
    movgt r0, r0, lsl #16
    movgt r9, r0, asr #16
ov001_02205648_L54:
    mvn r11, #0
ov001_02205648_L58:
    cmp r9, r8
    mov r6, #0
    bge ov001_02205648_L7c
    sub r0, r8, r9
    add r1, r0, #7
    mov r0, r1, asr #2
    add r0, r1, r0, lsr #29
    mov r5, r0, asr #3
    b ov001_02205648_L9c
ov001_02205648_L7c:
    cmp r9, r8
    movle r5, #1
    ble ov001_02205648_L9c
    sub r0, r9, r8
    add r1, r0, #7
    mov r0, r1, asr #2
    add r0, r1, r0, lsr #29
    mov r5, r0, asr #3
ov001_02205648_L9c:
    cmp r5, #4
    movgt r5, #4
    bgt ov001_02205648_Lb0
    cmp r5, #1
    movlt r5, #1
ov001_02205648_Lb0:
    mov r0, r10
    mov r1, #4
    bl native_fn_02204df0
    ldr r1, [sp, #0xc]
    mov r3, r0
    stmia sp, {r1, r9}
    mov r1, #7
    str r1, [sp, #0x8]
    ldrsb r1, [r10, #36]
    mov r0, r10
    mov r2, r7
    bl native_fn_02204d60
    cmp r0, r11
    beq ov001_02205648_L150
    mov r1, #12
    mla r1, r0, r1, r4
    cmp r9, r8
    strb r5, [r1, #0x6]
    beq ov001_02205648_L150
    cmp r9, r8
    bge ov001_02205648_L11c
    add r0, r9, r5, lsl #3
    mov r0, r0, lsl #16
    mov r9, r0, asr #16
    cmp r8, r0, asr #16
    movlt r9, r8
    b ov001_02205648_L134
ov001_02205648_L11c:
    sub r0, r9, r5, lsl #3
    mov r0, r0, lsl #16
    mov r9, r0, asr #16
    cmp r8, r0, asr #16
    movgt r9, r8
    mov r6, #1
ov001_02205648_L134:
    cmp r6, #0
    movne r0, #1
    strneb r0, [r1, #0x7]
    add r0, r7, r5
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    b ov001_02205648_L58
ov001_02205648_L150:
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
