/* ov001 row 0x02212144: 248 bytes.
 *
 * What it does: 62 instructions; 6 call(s) to 0x0205f98c, 0x02211470, 0x02212208, +3 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 6 calls (62 instructions, 6 calls, 9 branches, 5 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0x40
 *   branch +0x3c -> +0xf0
 *   branch +0x44 -> +0x80
 *   branch +0x58 -> +0xf0
 *   branch +0x7c -> +0xf0
 *   branch +0x84 -> +0xf0
 *   branch +0x90 -> +0xc4
 *   branch +0xa0 -> +0xb0
 *   branch +0xac -> +0xb8
 *   branch +0xe0 -> +0xf0
 *   test +0x20 cmp r1, #0
 *   test +0x30 cmp r0, #0
 *   test +0x40 cmp r1, #5
 *   test +0x4c cmp r0, #0
 *   test +0x80 cmp r1, #10
 *   test +0x8c cmp r1, #0
 *   test +0x98 cmp r1, #4
 *   test +0xd4 cmp r0, #0
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02212144; the literal pool and
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
extern void native_fn_02211470(void);
extern void native_fn_02048a6c(void);
extern void native_fn_02048a44(void);


asm u32 native_ov001_02212144 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    mov r4, #0
    ldr r0, [r6, #0x1c]
    mov r1, r4
    bl native_fn_0205f98c
    mov r5, r0
    ldr r1, [r5, #0x84]
    cmp r1, #0
    bne ov001_02212144_L40
    mov r0, r6
    bl native_fn_02211470
    cmp r0, #0
    movne r0, #5
    strne r0, [r5, #0x84]
    b ov001_02212144_Lf0
ov001_02212144_L40:
    cmp r1, #5
    bne ov001_02212144_L80
    ldrsh r0, [r6, #38]
    cmp r0, #0
    subgt r0, r0, #2
    strgth r0, [r6, #38]
    bgt ov001_02212144_Lf0
    ldr r0, [r5, #0x7c]
    mov r1, #10
    orr r0, r0, #2
    str r0, [r5, #0x7c]
    str r1, [r5, #0x84]
    mov r0, #30
    strh r0, [r6, #38]
    strb r1, [r6, #0x24]
    b ov001_02212144_Lf0
ov001_02212144_L80:
    cmp r1, #10
    bne ov001_02212144_Lf0
    ldrsb r1, [r6, #36]
    cmp r1, #0
    ble ov001_02212144_Lc4
    ldr r1, [r6]
    cmp r1, #4
    mov r1, r4
    bne ov001_02212144_Lb0
    sub r2, r1, #1
    bl native_fn_02048a6c
    b ov001_02212144_Lb8
ov001_02212144_Lb0:
    mov r2, #1
    bl native_fn_02048a6c
ov001_02212144_Lb8:
    ldrsb r0, [r6, #36]
    sub r0, r0, #1
    strb r0, [r6, #0x24]
ov001_02212144_Lc4:
    add r0, r5, #8
    mov r1, #1
    bl native_fn_02048a44
    ldrsh r0, [r6, #38]
    cmp r0, #0
    subgt r0, r0, #2
    strgth r0, [r6, #38]
    bgt ov001_02212144_Lf0
    mov r0, #0
    str r0, [r5, #0x84]
    mov r4, #1
ov001_02212144_Lf0:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, pc}
}
