/* ov000 row 0x0221db58: 708 bytes.
 *
 * What it does: 175 instructions; 23 call(s) to 0x0221db74, 0x0221db9c, 0x02062a50, +20 more; loops (back edge at +0x38); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x2bc -> constant 0x02246348 (image word 0x02246348)
 *   pool +0x2c0 -> constant 0x02246318 (image word 0x02246318)
 *   back edge +0x38 -> +0x1c
 *   back edge +0x64 -> +0x44
 *   branch +0x84 -> +0x160
 *   branch +0x94 -> +0x160
 *   branch +0xb8 -> +0xf4
 *   branch +0xcc -> +0xf4
 *   branch +0x100 -> +0x144
 *   branch +0x114 -> +0x144
 *   back edge +0x14c -> +0xac
 *   back edge +0x15c -> +0xa0
 *   branch +0x1e8 -> +0x220
 *   branch +0x1f8 -> +0x220
 *   branch +0x230 -> +0x270
 *   branch +0x240 -> +0x270
 *   back edge +0x278 -> +0x1d8
 *   branch +0x284 -> +0x29c
 *   back edge +0x2b0 -> +0x1bc
 *   test +0x24 cmp r1, #0
 *   test +0x34 cmp r3, #5
 *   test +0x50 cmp r1, #0
 *   test +0x60 cmp r3, #4
 *   test +0x80 cmp r0, #2
 *   test +0x90 cmp r0, #0
 *   test +0xc8 cmp r1, r0
 *   test +0x110 cmp r1, r0
 *   test +0x148 cmp r4, #3
 *   test +0x154 cmp r8, #2
 *   test +0x168 cmp r0, #2
 *   test +0x178 cmp r0, #0
 *   test +0x18c cmp r0, #0
 *   test +0x1e0 cmp r0, #0
 *   test +0x1e4 cmpne r7, r4
 *   test +0x1f4 cmp r1, r0
 *   test +0x228 cmp r0, #0
 *   test +0x22c cmpne r7, r4
 *   test +0x23c cmp r1, r0
 *   test +0x274 cmp r10, #3
 *   test +0x280 cmp r7, r0
 *   test +0x2ac cmp r0, #6
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221db58; the literal pool and
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

extern void native_fn_02062a50(void);
extern void native_fn_0221f8a0(void);
extern void native_fn_02048a60(void);
extern void native_fn_02062a88(void);
extern void native_fn_02220150(void);
extern void native_fn_022213d8(void);
extern void native_fn_0221f6e8(void);
extern void native_fn_0207cd98(void);
extern void native_fn_02062a10(void);
extern void native_fn_0221f7d4(void);


asm u32 native_ov000_0221db58 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #8
    mov r5, #0
    ldr r2, =0x02246348
    str r0, [sp]
    mov r6, r5
    mov r3, r5
ov000_0221db58_L1c:
    ldr r1, [r2, r3, lsl #2]
    add r3, r3, #1
    cmp r1, #0
    ldrne r0, [r1, #0x7c]
    bicne r0, r0, #2
    strne r0, [r1, #0x7c]
    cmp r3, #5
    blt ov000_0221db58_L1c
    ldr r2, =0x02246348
    mov r3, #0
ov000_0221db58_L44:
    add r0, r2, r3, lsl #2
    ldr r1, [r0, #0x14]
    add r3, r3, #1
    cmp r1, #0
    ldrne r0, [r1, #0x7c]
    bicne r0, r0, #2
    strne r0, [r1, #0x7c]
    cmp r3, #4
    blt ov000_0221db58_L44
    ldr r0, [sp]
    ldrsb r0, [r0, #16]
    sub r0, r0, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    and r0, r0, #255
    cmp r0, #2
    bhi ov000_0221db58_L160
    ldr r0, =0x02246318
    ldrb r0, [r0]
    cmp r0, #0
    bne ov000_0221db58_L160
    mov r8, #0
    mov r7, #48
ov000_0221db58_La0:
    ldr r10, =0x02246348
    mov r4, #0
    mov r11, #24
ov000_0221db58_Lac:
    mov r0, r4
    bl native_fn_02062a50
    movs r9, r0
    beq ov000_0221db58_Lf4
    mov r0, r8
    bl native_fn_0221f8a0
    ldr r1, [r9, #0x14]
    cmp r1, r0
    bne ov000_0221db58_Lf4
    ldr r0, [r10, r5, lsl #2]
    mov r1, r11
    mov r2, r7
    bl native_fn_02048a60
    ldr r1, [r10, r5, lsl #2]
    add r5, r5, #1
    ldr r0, [r1, #0x7c]
    orr r0, r0, #2
    str r0, [r1, #0x7c]
ov000_0221db58_Lf4:
    mov r0, r4
    bl native_fn_02062a88
    movs r9, r0
    beq ov000_0221db58_L144
    mov r0, r8
    bl native_fn_0221f8a0
    ldr r1, [r9, #0x14]
    cmp r1, r0
    bne ov000_0221db58_L144
    add r0, r10, r6, lsl #2
    ldr r0, [r0, #0x14]
    mov r1, #24
    mov r2, r7
    bl native_fn_02048a60
    add r0, r10, r6, lsl #2
    ldr r1, [r0, #0x14]
    add r6, r6, #1
    ldr r0, [r1, #0x7c]
    orr r0, r0, #2
    str r0, [r1, #0x7c]
ov000_0221db58_L144:
    add r4, r4, #1
    cmp r4, #3
    blt ov000_0221db58_Lac
    add r8, r8, #1
    cmp r8, #2
    add r7, r7, #16
    blt ov000_0221db58_La0
ov000_0221db58_L160:
    ldr r0, [sp]
    ldrsb r0, [r0, #16]
    cmp r0, #2
    addne sp, sp, #8
    ldmneia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    bl native_fn_02220150
    cmp r0, #0
    addeq sp, sp, #8
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, =0x02246318
    ldrb r0, [r0]
    cmp r0, #0
    addne sp, sp, #8
    ldmneia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    bl native_fn_022213d8
    mov r1, r0
    ldr r0, [sp]
    ldr r0, [r0, #0x4]
    bl native_fn_0221f6e8
    mov r7, r0
    mov r0, #0
    str r0, [sp, #0x4]
    mov r9, #48
ov000_0221db58_L1bc:
    mov r0, r7
    bl native_fn_0207cd98
    bl native_fn_02062a10
    ldr r11, =0x02246348
    mov r8, r0
    mov r10, #0
    mvn r4, #0
ov000_0221db58_L1d8:
    mov r0, r10
    bl native_fn_02062a50
    cmp r0, #0
    cmpne r7, r4
    beq ov000_0221db58_L220
    ldr r1, [r8, #0x14]
    ldr r0, [r0, #0x14]
    cmp r1, r0
    bne ov000_0221db58_L220
    ldr r0, [r11, r5, lsl #2]
    mov r1, #148
    mov r2, r9
    bl native_fn_02048a60
    ldr r1, [r11, r5, lsl #2]
    add r5, r5, #1
    ldr r0, [r1, #0x7c]
    orr r0, r0, #2
    str r0, [r1, #0x7c]
ov000_0221db58_L220:
    mov r0, r10
    bl native_fn_02062a88
    cmp r0, #0
    cmpne r7, r4
    beq ov000_0221db58_L270
    ldr r1, [r8, #0x14]
    ldr r0, [r0, #0x14]
    cmp r1, r0
    bne ov000_0221db58_L270
    add r0, r11, r6, lsl #2
    ldr r0, [r0, #0x14]
    mov r1, #148
    mov r2, r9
    bl native_fn_02048a60
    add r0, r11, r6, lsl #2
    ldr r1, [r0, #0x14]
    add r6, r6, #1
    ldr r0, [r1, #0x7c]
    orr r0, r0, #2
    str r0, [r1, #0x7c]
ov000_0221db58_L270:
    add r10, r10, #1
    cmp r10, #3
    blt ov000_0221db58_L1d8
    mvn r0, #0
    cmp r7, r0
    beq ov000_0221db58_L29c
    bl native_fn_022213d8
    mov r1, r0
    mov r0, r7
    bl native_fn_0221f7d4
    mov r7, r0
ov000_0221db58_L29c:
    ldr r0, [sp, #0x4]
    add r9, r9, #16
    add r0, r0, #1
    str r0, [sp, #0x4]
    cmp r0, #6
    blt ov000_0221db58_L1bc
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
