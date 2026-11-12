/* ov000 row 0x02207018: 696 bytes.
 *
 * What it does: 170 instructions; 26 call(s) to 0x0202a8e0, 0x0203cc2c, 0x020481b8, +23 more; loops (back edge at +0x4c); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x2a8 -> constant 0x022382c4 (image word 0x022382c4)
 *   pool +0x2ac -> native_data_0222f6e0 (image word 0x0222f6e0)
 *   pool +0x2b0 -> native_data_0222ba5c (image word 0x0222ba5c)
 *   pool +0x2b4 -> constant 0x00007fff (image word 0x00007fff)
 *   branch +0x24 -> +0x158
 *   branch +0x48 -> +0x94
 *   branch +0x54 -> +0x94
 *   branch +0x9c -> +0xdc
 *   branch +0xa8 -> +0xdc
 *   branch +0xe4 -> +0x124
 *   branch +0xf0 -> +0x124
 *   branch +0x164 -> +0x184
 *   branch +0x190 -> +0x200
 *   branch +0x1b4 -> +0x200
 *   branch +0x1c0 -> +0x200
 *   branch +0x1dc -> +0x1ec
 *   branch +0x1e8 -> +0x1f0
 *   branch +0x20c -> +0x23c
 *   branch +0x248 -> +0x260
 *   branch +0x26c -> +0x288
 *   test +0x18 cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   test +0x98 cmp r0, #0
 *   test +0xe0 cmp r0, #0
 *   test +0x160 cmp r0, #10
 *   test +0x16c cmp r0, #1
 *   test +0x18c cmp r1, #20
 *   test +0x1a8 cmp r2, r1
 *   test +0x1bc cmp r2, r0
 *   test +0x1d8 cmp r1, #0
 *   test +0x1e4 cmp r0, #1
 *   test +0x1f0 cmp r2, #0
 *   test +0x208 cmp r0, #30
 *   test +0x244 cmp r0, #40
 *   test +0x250 cmp r0, #1
 *   test +0x268 cmp r0, #50
 *   test +0x290 cmp r1, #100
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02207018; the literal pool and
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

extern u8 native_data_0222f6e0[];
extern u8 native_data_0222ba5c[];
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern void native_fn_020481b8(void);
extern void native_fn_02048308(void);
extern void native_fn_0202a498(void);
extern void native_fn_0204540c(void);
extern void native_fn_0204594c(void);
extern void native_fn_02208ca0(void);
extern void native_fn_02041510(void);
extern void native_fn_02041538(void);
extern void native_fn_02041800(void);
extern void native_fn_0202a634(void);
extern void native_fn_02066c3c(void);
extern void native_fn_02045654(void);
extern void native_fn_02208dbc(void);


asm u32 native_ov000_02207018 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r1, =0x022382c4
    mov r7, r0
    ldrb r0, [r1]
    ldr r2, =native_data_0222f6e0
    add r1, r7, r7, lsl #2
    cmp r0, #0
    add r5, r2, r1
    mov r4, #0
    bne ov000_02207018_L158
    mov r0, #12
    mul r1, r7, r0
    ldr r2, =native_data_0222ba5c
    ldr r3, =0x00007fff
    ldr r0, [r2, r1]
    strh r3, [sp]
    cmp r0, #0
    add r6, r2, r1
    beq ov000_02207018_L94
    bl native_fn_0202a8e0
    movs r8, r0
    beq ov000_02207018_L94
    ldr r0, [r6]
    mov r1, #2
    bl native_fn_0203cc2c
    mov r2, r8
    mov r1, r4
    mov r8, r0
    bl native_fn_020481b8
    add r0, sp, #0
    mov r1, r4
    mov r2, #2
    bl native_fn_020481b8
    bl native_fn_02048308
    mov r1, r8
    mov r0, #2
    bl native_fn_0202a498
ov000_02207018_L94:
    ldr r0, [r6, #0x4]
    cmp r0, #0
    beq ov000_02207018_Ldc
    bl native_fn_0202a8e0
    movs r9, r0
    beq ov000_02207018_Ldc
    ldr r0, [r6, #0x4]
    mov r1, #2
    bl native_fn_0203cc2c
    mov r8, r0
    mov r1, r8
    mov r3, r9
    mov r0, #3
    mov r2, #0
    bl native_fn_0204540c
    mov r1, r8
    mov r0, #2
    bl native_fn_0202a498
ov000_02207018_Ldc:
    ldr r0, [r6, #0x8]
    cmp r0, #0
    beq ov000_02207018_L124
    bl native_fn_0202a8e0
    movs r8, r0
    beq ov000_02207018_L124
    ldr r0, [r6, #0x8]
    mov r1, #2
    bl native_fn_0203cc2c
    mov r6, r0
    mov r1, r6
    mov r3, r8
    mov r0, #3
    mov r2, #0
    bl native_fn_0204594c
    mov r1, r6
    mov r0, #2
    bl native_fn_0202a498
ov000_02207018_L124:
    mov r0, r7
    bl native_fn_02208ca0
    ldrb r1, [r5]
    ldrb r2, [r5, #0x1]
    mov r0, #0
    bl native_fn_02041510
    ldrb r1, [r5]
    ldrb r2, [r5, #0x1]
    mov r0, #0
    bl native_fn_02041538
    ldr r0, =0x022382c4
    mov r1, #10
    strb r1, [r0]
ov000_02207018_L158:
    ldr r0, =0x022382c4
    ldrb r0, [r0]
    cmp r0, #10
    bne ov000_02207018_L184
    bl native_fn_02041800
    cmp r0, #1
    ldrne r0, =0x022382c4
    movne r1, #0
    strneb r1, [r0, #0x1]
    movne r1, #20
    strneb r1, [r0]
ov000_02207018_L184:
    ldr r0, =0x022382c4
    ldrb r1, [r0]
    cmp r1, #20
    bne ov000_02207018_L200
    ldrb r1, [r0, #0x1]
    add r2, r1, #1
    strb r2, [r0, #0x1]
    ldrb r1, [r5, #0x2]
    and r2, r2, #255
    cmp r2, r1
    movhi r1, #30
    strhib r1, [r0]
    bhi ov000_02207018_L200
    ldrb r0, [r5, #0x4]
    cmp r2, r0
    bls ov000_02207018_L200
    bl native_fn_0202a634
    mov r6, r0
    bl native_fn_02066c3c
    ldrh r1, [r6, #2]
    mov r2, #0
    cmp r1, #0
    bne ov000_02207018_L1ec
    ldrb r0, [r0]
    cmp r0, #1
    bne ov000_02207018_L1f0
ov000_02207018_L1ec:
    mov r2, #1
ov000_02207018_L1f0:
    cmp r2, #0
    ldrne r0, =0x022382c4
    movne r1, #30
    strneb r1, [r0]
ov000_02207018_L200:
    ldr r0, =0x022382c4
    ldrb r0, [r0]
    cmp r0, #30
    bne ov000_02207018_L23c
    ldrb r1, [r5, #0x3]
    ldrb r2, [r5, #0x1]
    mov r0, #1
    bl native_fn_02041510
    ldrb r1, [r5, #0x3]
    ldrb r2, [r5, #0x1]
    mov r0, #1
    bl native_fn_02041538
    ldr r0, =0x022382c4
    mov r1, #40
    strb r1, [r0]
ov000_02207018_L23c:
    ldr r0, =0x022382c4
    ldrb r0, [r0]
    cmp r0, #40
    bne ov000_02207018_L260
    bl native_fn_02041800
    cmp r0, #1
    ldrne r0, =0x022382c4
    movne r1, #50
    strneb r1, [r0]
ov000_02207018_L260:
    ldr r0, =0x022382c4
    ldrb r0, [r0]
    cmp r0, #50
    bne ov000_02207018_L288
    mov r0, #3
    bl native_fn_02045654
    bl native_fn_02208dbc
    ldr r0, =0x022382c4
    mov r1, #100
    strb r1, [r0]
ov000_02207018_L288:
    ldr r0, =0x022382c4
    ldrb r1, [r0]
    cmp r1, #100
    moveq r1, #0
    moveq r4, #1
    streqb r1, [r0]
    mov r0, r4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
