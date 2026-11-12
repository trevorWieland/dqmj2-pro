/* ov001 row 0x02213154: 256 bytes.
 *
 * What it does: 63 instructions; 7 call(s) to 0x0205f98c, 0x022129f4, 0x022131bc, +4 more; loops (back edge at +0x7c); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 7 calls (63 instructions, 7 calls, 11 branches, 6 back edges, 1 literal slot).
 *
 *   pool +0xfc -> constant 0x00000119 (image word 0x00000119)
 *   branch +0x18 -> +0xd8
 *   branch +0x1c -> +0x2c
 *   branch +0x20 -> +0x44
 *   branch +0x24 -> +0x60
 *   branch +0x28 -> +0xd0
 *   branch +0x40 -> +0xd8
 *   branch +0x5c -> +0xd8
 *   branch +0x70 -> +0x90
 *   back edge +0x9c -> +0x68
 *   branch +0xbc -> +0xd8
 *   branch +0xcc -> +0xd8
 *   branch +0xe4 -> +0xf4
 *   back edge +0xec -> +0x00
 *   test +0x10 cmp r1, #3
 *   test +0x50 cmp r1, #0
 *   test +0x6c cmp r7, r0
 *   test +0x98 cmp r7, #24
 *   test +0xb0 cmp r0, #24
 *   test +0xe0 cmp r4, #0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02213154; the literal pool and
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
extern void native_fn_022129f4(void);
extern void native_fn_021f949c(void);
extern void native_fn_02212f14(void);
extern void native_fn_02213588(void);


asm u32 native_ov001_02213154 (register u32 a0)
{
ov001_02213154_L0:
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r5, r0
    ldr r1, [r5, #0x34]
    mov r4, #0
    cmp r1, #3
    addls pc, pc, r1, lsl #2
    b ov001_02213154_Ld8
    b ov001_02213154_L2c
    b ov001_02213154_L44
    b ov001_02213154_L60
    b ov001_02213154_Ld0
ov001_02213154_L2c:
    strb r4, [r5, #0x24]
    mov r0, #5
    strh r0, [r5, #38]
    mov r0, #1
    str r0, [r5, #0x34]
    b ov001_02213154_Ld8
ov001_02213154_L44:
    ldrsh r1, [r5, #38]
    sub r0, r1, #1
    strh r0, [r5, #38]
    cmp r1, #0
    movlt r0, #2
    strlt r0, [r5, #0x34]
    b ov001_02213154_Ld8
ov001_02213154_L60:
    mov r7, r4
    mov r6, #4
ov001_02213154_L68:
    ldrsb r0, [r5, #36]
    cmp r7, r0
    bne ov001_02213154_L90
    ldr r0, [r5, #0x1c]
    mov r1, r7
    bl native_fn_0205f98c
    mov r0, r5
    mov r1, r7
    mov r2, r6
    bl native_fn_022129f4
ov001_02213154_L90:
    add r0, r7, #1
    and r7, r0, #255
    cmp r7, #24
    blo ov001_02213154_L68
    ldrsb r0, [r5, #36]
    add r0, r0, #1
    strb r0, [r5, #0x24]
    ldrsb r0, [r5, #36]
    cmp r0, #24
    movge r0, #3
    strge r0, [r5, #0x34]
    bge ov001_02213154_Ld8
    ldr r0, =0x00000119
    mov r1, #1
    bl native_fn_021f949c
    b ov001_02213154_Ld8
ov001_02213154_Ld0:
    mov r1, r4
    bl native_fn_02212f14
ov001_02213154_Ld8:
    mov r0, r5
    bl native_fn_02213588
    cmp r4, #0
    beq ov001_02213154_Lf4
    mov r0, r5
    bl ov001_02213154_L0
    mov r4, r0
ov001_02213154_Lf4:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
