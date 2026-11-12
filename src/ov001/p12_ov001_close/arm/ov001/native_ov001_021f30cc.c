/* ov001 row 0x021f30cc: 172 bytes.
 *
 * What it does: 43 instructions; 5 call(s) to 0x0207afec, 0x021db438, 0x021f3170, +2 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 5 calls (43 instructions, 5 calls, 3 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0x48
 *   branch +0x54 -> +0xa4
 *   branch +0x6c -> +0x94
 *   branch +0x80 -> +0x94
 *   back edge +0xa0 -> +0x64
 *   test +0x28 cmp r0, #1
 *   test +0x48 cmp r7, #0
 *   test +0x50 cmpgt r7, #0
 *   test +0x68 cmp r0, #0
 *   test +0x7c cmp r0, #0
 *   test +0x98 cmp r6, r7
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f30cc; the literal pool and
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


asm u32 native_ov001_021f30cc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r9, r1
    mov r10, r0
    mov r0, r9
    mov r4, r2
    mov r8, #0
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #16
    mov r0, r0, lsr #28
    cmp r0, #1
    movne r7, #1
    bne ov001_021f30cc_L48
    ldrb r0, [r10, #0x31e]
    mov r1, r8
    bl native_fn_021db438
    mov r10, r0
    mov r7, #3
ov001_021f30cc_L48:
    cmp r7, #0
    mov r6, #0
    cmpgt r7, #0
    ble ov001_021f30cc_La4
    and r5, r4, #255
    mov r4, r6
    mov r11, #1
ov001_021f30cc_L64:
    ldrb r0, [r10, #0x31c]
    cmp r0, #0
    beq ov001_021f30cc_L94
    mov r0, r10
    mov r1, r9
    bl native_fn_021f307c
    cmp r0, #0
    beq ov001_021f30cc_L94
    strb r5, [r10, #0x31d]
    add r0, r10, #768
    mov r8, r11
    strh r4, [r0, #32]
ov001_021f30cc_L94:
    add r6, r6, #1
    cmp r6, r7
    add r10, r10, #1088
    blt ov001_021f30cc_L64
ov001_021f30cc_La4:
    mov r0, r8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
