/* ov000 row 0x022098d8: 676 bytes.
 *
 * What it does: 165 instructions; 21 call(s) to 0x0220980c, 0x02209880, 0x0207e4ac, +18 more; loops (back edge at +0x24); returns through pop {r4, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x294 -> constant 0x0223856c (image word 0x0223856c)
 *   pool +0x298 -> constant 0x02238570 (image word 0x02238570)
 *   pool +0x29c -> constant 0x00000ff7 (image word 0x00000ff7)
 *   pool +0x2a0 -> constant 0x02101ae8 (image word 0x02101ae8)
 *   branch +0x18 -> +0x38
 *   branch +0x44 -> +0x64
 *   branch +0x70 -> +0x98
 *   branch +0x88 -> +0x98
 *   branch +0xa4 -> +0x100
 *   branch +0xc0 -> +0x100
 *   branch +0x10c -> +0x154
 *   branch +0x118 -> +0x154
 *   branch +0x130 -> +0x154
 *   branch +0x160 -> +0x190
 *   branch +0x19c -> +0x1c8
 *   branch +0x1b0 -> +0x1c8
 *   branch +0x1d4 -> +0x1e0
 *   branch +0x1ec -> +0x1f8
 *   branch +0x204 -> +0x224
 *   branch +0x230 -> +0x248
 *   branch +0x254 -> +0x270
 *   test +0x14 cmp r1, #0
 *   test +0x40 cmp r1, #10
 *   test +0x54 cmp r1, #30
 *   test +0x6c cmp r0, #15
 *   test +0x78 cmp r0, #0
 *   test +0xa0 cmp r0, #20
 *   test +0xb0 cmp r0, #0
 *   test +0x108 cmp r0, #30
 *   test +0x114 cmp r0, #0
 *   test +0x120 cmp r0, #0
 *   test +0x15c cmp r0, #40
 *   test +0x198 cmp r0, #50
 *   test +0x1ac tst r1, r0
 *   test +0x1d0 cmp r0, #100
 *   test +0x1e8 cmp r0, #110
 *   test +0x200 cmp r0, #150
 *   test +0x22c cmp r0, #160
 *   test +0x238 cmp r0, #1
 *   test +0x250 cmp r0, #200
 *   0 block transfer(s), 20 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022098d8; the literal pool and
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

extern void native_fn_0220980c(void);
extern void native_fn_02209880(void);
extern void native_fn_0207e4ac(void);
extern void native_fn_0207dd5c(void);
extern void native_fn_02217bdc(void);
extern void native_fn_0205fa4c(void);
extern void native_fn_0207dea8(void);
extern void native_fn_0207e3f8(void);
extern void native_fn_02217c9c(void);
extern void native_fn_0202a634(void);
extern void native_fn_020c225c(void);
extern void native_fn_02041538(void);
extern void native_fn_02041814(void);
extern void native_fn_0204073c(void);
extern void native_fn_022098c4(void);
extern void native_fn_020851d4(void);
extern void native_fn_02085200(void);


asm u32 native_ov000_022098d8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #8
    ldr r0, =0x0223856c
    mov r4, #5
    ldrb r1, [r0, #0x1]
    cmp r1, #0
    bne ov000_022098d8_L38
    mov r1, #0
    strb r1, [r0]
    bl native_fn_0220980c
    bl native_fn_02209880
    ldr r0, =0x0223856c
    mov r1, #10
    strb r1, [r0, #0x1]
ov000_022098d8_L38:
    ldr r0, =0x0223856c
    ldrb r1, [r0, #0x1]
    cmp r1, #10
    bne ov000_022098d8_L64
    ldrb r1, [r0]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0]
    movhi r1, #15
    strhib r1, [r0, #0x1]
ov000_022098d8_L64:
    ldr r0, =0x0223856c
    ldrb r0, [r0, #0x1]
    cmp r0, #15
    bne ov000_022098d8_L98
    bl native_fn_0207e4ac
    cmp r0, #0
    ldreq r0, =0x0223856c
    moveq r1, #110
    streqb r1, [r0, #0x1]
    beq ov000_022098d8_L98
    ldr r0, =0x0223856c
    mov r1, #20
    strb r1, [r0, #0x1]
ov000_022098d8_L98:
    ldr r0, =0x0223856c
    ldrb r0, [r0, #0x1]
    cmp r0, #20
    bne ov000_022098d8_L100
    mov r0, #2
    bl native_fn_0207dd5c
    cmp r0, #0
    ldreq r0, =0x0223856c
    moveq r1, #100
    streqb r1, [r0, #0x1]
    beq ov000_022098d8_L100
    mov r0, #0
    str r0, [sp]
    mov r12, #87
    mov r0, #5
    mov r1, #6
    mov r2, #8
    mov r3, #1
    str r12, [sp, #0x4]
    bl native_fn_02217bdc
    ldr r0, =0x02238570
    mov r1, #1
    bl native_fn_0205fa4c
    ldr r0, =0x0223856c
    mov r1, #30
    strb r1, [r0, #0x1]
ov000_022098d8_L100:
    ldr r0, =0x0223856c
    ldrb r0, [r0, #0x1]
    cmp r0, #30
    bne ov000_022098d8_L154
    bl native_fn_0207dea8
    cmp r0, #0
    beq ov000_022098d8_L154
    bl native_fn_0207e3f8
    cmp r0, #0
    ldrne r0, =0x0223856c
    movne r1, #100
    strneb r1, [r0, #0x1]
    bne ov000_022098d8_L154
    mov r0, #0
    bl native_fn_02217c9c
    ldr r0, =0x02238570
    mov r1, #0
    bl native_fn_0205fa4c
    ldr r0, =0x0223856c
    mov r1, #40
    strb r1, [r0, #0x1]
ov000_022098d8_L154:
    ldr r0, =0x0223856c
    ldrb r0, [r0, #0x1]
    cmp r0, #40
    bne ov000_022098d8_L190
    mov r3, #0
    str r3, [sp]
    mov r12, #87
    mov r0, #5
    mov r1, #6
    mov r2, #9
    str r12, [sp, #0x4]
    bl native_fn_02217bdc
    ldr r0, =0x0223856c
    mov r1, #50
    strb r1, [r0, #0x1]
ov000_022098d8_L190:
    ldr r0, =0x0223856c
    ldrb r0, [r0, #0x1]
    cmp r0, #50
    bne ov000_022098d8_L1c8
    bl native_fn_0202a634
    ldrh r1, [r0, #2]
    ldr r0, =0x00000ff7
    tst r1, r0
    beq ov000_022098d8_L1c8
    mov r0, #1
    bl native_fn_02217c9c
    ldr r0, =0x0223856c
    mov r1, #150
    strb r1, [r0, #0x1]
ov000_022098d8_L1c8:
    ldr r0, =0x0223856c
    ldrb r0, [r0, #0x1]
    cmp r0, #100
    bne ov000_022098d8_L1e0
    mov r0, #536870912
    bl native_fn_020c225c
ov000_022098d8_L1e0:
    ldr r0, =0x0223856c
    ldrb r0, [r0, #0x1]
    cmp r0, #110
    bne ov000_022098d8_L1f8
    mov r0, #536870912
    bl native_fn_020c225c
ov000_022098d8_L1f8:
    ldr r0, =0x0223856c
    ldrb r0, [r0, #0x1]
    cmp r0, #150
    bne ov000_022098d8_L224
    mov r0, #1
    mov r2, r0
    mov r1, #2
    bl native_fn_02041538
    ldr r0, =0x0223856c
    mov r1, #160
    strb r1, [r0, #0x1]
ov000_022098d8_L224:
    ldr r0, =0x0223856c
    ldrb r0, [r0, #0x1]
    cmp r0, #160
    bne ov000_022098d8_L248
    bl native_fn_02041814
    cmp r0, #1
    ldrne r0, =0x0223856c
    movne r1, #200
    strneb r1, [r0, #0x1]
ov000_022098d8_L248:
    ldr r0, =0x0223856c
    ldrb r0, [r0, #0x1]
    cmp r0, #200
    bne ov000_022098d8_L270
    mov r0, #0
    bl native_fn_0204073c
    ldr r0, =0x0223856c
    mov r1, #0
    strb r1, [r0, #0x1]
    mov r4, #9
ov000_022098d8_L270:
    bl native_fn_022098c4
    bl native_fn_020851d4
    bl native_fn_02085200
    ldr r1, =0x02101ae8
    mov r2, #1
    mov r0, r4
    str r2, [r1, #0xc84]
    add sp, sp, #8
    ldmia sp!, {r4, pc}
}
