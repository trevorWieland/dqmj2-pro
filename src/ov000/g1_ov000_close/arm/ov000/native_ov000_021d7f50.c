/* ov000 row 0x021d7f50: 460 bytes.
 *
 * What it does: 113 instructions; 18 call(s) to 0x0202a37c, 0x021d7da4, 0x02048a9c, +15 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1c4 -> constant 0x022301b8 (image word 0x022301b8)
 *   pool +0x1c8 -> constant 0x022300c0 (image word 0x022300c0)
 *   branch +0x54 -> +0x68
 *   branch +0x64 -> +0x74
 *   branch +0xf8 -> +0x108
 *   back edge +0x158 -> +0xb0
 *   back edge +0x168 -> +0x0c
 *   branch +0x174 -> +0x1ac
 *   test +0x4c cmp r4, #0
 *   test +0xe8 cmp r4, #0
 *   test +0x154 cmp r5, #8
 *   test +0x160 cmp r4, #2
 *   test +0x170 cmp r0, #0
 *   0 block transfer(s), 16 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d7f50; the literal pool and
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

extern void native_fn_0202a37c(void);
extern void native_fn_021d7da4(void);
extern void native_fn_02048a9c(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048644(void);
extern void native_fn_020ba574(void);


asm u32 native_ov000_021d7f50 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r6, =0x022301b8
    mov r4, #0
ov000_021d7f50_Lc:
    mov r0, #0
    str r0, [r6, #0xa4]
    str r0, [r6, #0xa8]
    str r0, [r6, #0xac]
    mov r0, #2
    mov r1, #144
    mov r2, #4
    bl native_fn_0202a37c
    str r0, [r6, #0xa0]
    bl native_fn_021d7da4
    ldr r0, [r6, #0xa0]
    mov r1, #3
    bl native_fn_02048a9c
    ldr r0, [r6, #0xa0]
    mov r1, #0
    bl native_fn_02048a94
    cmp r4, #0
    ldr r0, [r6, #0xa0]
    bne ov000_021d7f50_L68
    mov r1, #152
    mov r2, #32
    bl native_fn_02048a60
    b ov000_021d7f50_L74
ov000_021d7f50_L68:
    mov r1, #8
    mov r2, #128
    bl native_fn_02048a60
ov000_021d7f50_L74:
    ldr r1, =0x022300c0
    ldr r0, [r6, #0xa0]
    ldr r1, [r1, #0x20]
    mov r2, #11
    bl native_fn_02048644
    ldr r1, [r6, #0xa0]
    mov r5, #0
    ldr r0, [r1, #0x7c]
    mov r7, r6
    bic r0, r0, #2
    mov r10, r5
    str r0, [r1, #0x7c]
    mov r8, #152
    mov r9, #8
    mov r11, r5
ov000_021d7f50_Lb0:
    strb r11, [r7, #0x10]
    mov r0, #2
    mov r1, #144
    mov r2, #4
    bl native_fn_0202a37c
    str r0, [r7]
    bl native_fn_021d7da4
    ldr r0, [r7]
    mov r1, #3
    bl native_fn_02048a9c
    add r1, r5, #1
    ldr r0, [r7]
    and r1, r1, #255
    bl native_fn_02048a94
    cmp r4, #0
    movne r0, r9, lsl #8
    strne r0, [r7, #0x4]
    movne r0, #32768
    bne ov000_021d7f50_L108
    mov r0, r8, lsl #8
    str r0, [r7, #0x4]
    mov r0, #8192
ov000_021d7f50_L108:
    str r0, [r7, #0x8]
    strh r10, [r7, #12]
    mov r0, #128
    strh r0, [r7, #14]
    mov r0, #15
    strb r0, [r7, #0x11]
    ldr r1, =0x022300c0
    ldr r0, [r7]
    ldr r1, [r1, #0x20]
    mov r2, #3
    bl native_fn_02048644
    ldr r1, [r7], #20
    add r5, r5, #1
    ldr r0, [r1, #0x7c]
    add r8, r8, #10
    bic r0, r0, #2
    add r9, r9, #10
    str r0, [r1, #0x7c]
    add r10, r10, #8192
    cmp r5, #8
    blt ov000_021d7f50_Lb0
    add r4, r4, #1
    cmp r4, #2
    add r6, r6, #176
    blt ov000_021d7f50_Lc
    bl native_fn_020ba574
    cmp r0, #0
    blt ov000_021d7f50_L1ac
    ldr r0, =0x022300c0
    ldr r1, [r0, #0x18]
    ldr r0, [r1, #0x7c]
    orr r0, r0, #2
    str r0, [r1, #0x7c]
    bl native_fn_020ba574
    add r2, r0, #40
    ldr r1, =0x022300c0
    and r2, r2, #255
    ldr r0, [r1, #0x18]
    ldr r1, [r1, #0x20]
    bl native_fn_02048644
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_021d7f50_L1ac:
    ldr r0, =0x022300c0
    ldr r1, [r0, #0x18]
    ldr r0, [r1, #0x7c]
    bic r0, r0, #2
    str r0, [r1, #0x7c]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
