/* main row 0x0209b6e4: 436 bytes.
 *
 * What it does: Writes 2 blocks of 5 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x190 -> native_data_021d19e0 (image word 0x021d19e0)
 *   pool +0x194 -> native_fn_0209c15c+1 (image word 0x0209c15d)
 *   pool +0x198 -> native_fn_0209c188+1 (image word 0x0209c189)
 *   pool +0x19c -> native_fn_0209d0b8+1 (image word 0x0209d0b9)
 *   pool +0x1a0 -> native_fn_0209d08c+1 (image word 0x0209d08d)
 *   pool +0x1a4 -> native_fn_0209d0d4+1 (image word 0x0209d0d5)
 *   pool +0x1a8 -> constant 0xffffb172 (image word 0xffffb172)
 *   pool +0x1ac -> constant 0xffffb17b (image word 0xffffb17b)
 *   pool +0x1b0 -> constant 0x0000038d (image word 0x0000038d)
 *   branch +0x08 -> +0x0e
 *   branch +0x14 -> +0x76
 *   branch +0x1a -> +0x76
 *   branch +0x22 -> +0x76
 *   branch +0x2c -> +0x58
 *   branch +0x4e -> +0x5a
 *   branch +0x52 -> +0xfc
 *   branch +0x56 -> +0x106
 *   branch +0x58 -> +0x15c
 *   branch +0x74 -> +0x78
 *   branch +0x76 -> +0x18e
 *   branch +0x8e -> +0x18e
 *   branch +0xa6 -> +0x18e
 *   branch +0xbe -> +0x18e
 *   branch +0xd6 -> +0x18e
 *   branch +0xee -> +0x18e
 *   branch +0xfa -> +0x15c
 *   branch +0x114 -> +0x15c
 *   branch +0x120 -> +0x15c
 *   branch +0x12c -> +0x15c
 *   branch +0x140 -> +0x148
 *   branch +0x146 -> +0x150
 *   branch +0x14e -> +0x15c
 *   branch +0x154 -> +0x15c
 *   branch +0x168 -> +0x18e
 *   branch +0x170 -> +0x182
 *   test +0x06 cmp r0, #0x0
 *   test +0x12 cmp r0, #0x0
 *   test +0x18 cmp r0, #0x0
 *   test +0x20 cmp r0, #0x0
 *   test +0x2a cmp r0, #0x6
 *   test +0x4c cmp r0, #0x1
 *   test +0x50 cmp r0, #0x2
 *   test +0x54 cmp r0, #0x3
 *   test +0x72 cmp r0, #0x0
 *   test +0x8c cmp r0, #0x0
 *   test +0xa4 cmp r0, #0x0
 *   test +0xbc cmp r0, #0x0
 *   test +0xd4 cmp r0, #0x0
 *   test +0xec cmp r0, #0x0
 *   test +0x13e cmp r1, #0x2
 *   test +0x144 cmp r0, #0x3
 *   test +0x152 cmp r0, #0x0
 *   test +0x166 cmp r1, #0x1
 *   test +0x16e cmp r0, #0x0
 *   2 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0209b6e4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0209afe8(void);
extern void native_fn_0209be5c(void);
extern u8 native_data12_021d19e0[];
extern void native_fn_0209a9e4(void);
extern void native_fn_020a9448(void);
extern void native_fn_020a9f2c(void);
extern void native_fn_0209becc(void);
extern void native_fn_0209c15c(void);
extern void native_fn_020a9f88(void);
extern void native_fn_0209c188(void);
extern void native_fn_0209d0b8(void);
extern void native_fn_0209d08c(void);
extern void native_fn_0209d0d4(void);
extern void native_fn_0209be60(void);
extern void native_fn_0209c538(void);
extern void native_fn_0209c610(void);
extern void native_fn_0209c55c(void);
extern void native_fn_0209ce3c(void);
extern void native_fn_0209e488(void);
extern void native_fn_020a4208(void);
extern void native_fn_020b74d4(void);


asm u32 native_main_0209b6e4 (register u32 a0)
{
    push {r3, lr}
    bl native_fn_0209afe8
    cmp r0, #0x0
    beq main_0209b6e4_Le
    bl native_fn_0209be5c
main_0209b6e4_Le:
    ldr r0, =native_data12_021d19e0
    ldr r0, [r0, #0]
    cmp r0, #0x0
    beq main_0209b6e4_L76
    ldr r0, [r0, #0x24]
    cmp r0, #0x0
    beq main_0209b6e4_L76
    bl native_fn_0209a9e4
    cmp r0, #0x0
    bne main_0209b6e4_L76
    ldr r0, =native_data12_021d19e0
    ldr r0, [r0, #0]
    ldr r0, [r0, #0x24]
    cmp r0, #0x6
    bhi main_0209b6e4_L58
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    lsl r0, r4, #0x4
    lsl r4, r1, #0
    lsl r4, r2, #0x3
    lsl r2, r3, #0x3
    lsl r2, r3, #0x3
    lsl r6, r4, #0x3
    lsl r2, r6, #0x3
    bl native_fn_020a9448
    cmp r0, #0x1
    beq main_0209b6e4_L5a
    cmp r0, #0x2
    beq main_0209b6e4_Lfc
    cmp r0, #0x3
    beq main_0209b6e4_L106
main_0209b6e4_L58:
    b main_0209b6e4_L15c
main_0209b6e4_L5a:
    ldr r0, =native_data12_021d19e0
    mov r2, #0x10
    ldr r1, [r0, #0]
    mov r3, #0xb
    add r0, r1, #0x0
    add r1, #0xa0
    ldr r1, [r1, #0]
    add r0, #0x1c
    bl native_fn_020a9f2c
    bl native_fn_0209becc
    cmp r0, #0x0
    beq main_0209b6e4_L78
main_0209b6e4_L76:
    b main_0209b6e4_L18e
main_0209b6e4_L78:
    ldr r0, =native_data12_021d19e0
    mov r1, #0x0
    ldr r0, [r0, #0]
    ldr r2, =native_fn_0209c15c+1
    add r0, #0x1c
    add r3, r1, #0x0
    bl native_fn_020a9f88
    bl native_fn_0209becc
    cmp r0, #0x0
    bne main_0209b6e4_L18e
    ldr r0, =native_data12_021d19e0
    ldr r2, =native_fn_0209c188+1
    ldr r0, [r0, #0]
    mov r1, #0x3
    add r0, #0x1c
    mov r3, #0x0
    bl native_fn_020a9f88
    bl native_fn_0209becc
    cmp r0, #0x0
    bne main_0209b6e4_L18e
    ldr r0, =native_data12_021d19e0
    ldr r2, =native_fn_0209d0b8+1
    ldr r0, [r0, #0]
    mov r1, #0x7
    add r0, #0x1c
    mov r3, #0x0
    bl native_fn_020a9f88
    bl native_fn_0209becc
    cmp r0, #0x0
    bne main_0209b6e4_L18e
    ldr r0, =native_data12_021d19e0
    ldr r2, =native_fn_0209d08c+1
    ldr r0, [r0, #0]
    mov r1, #0x1
    add r0, #0x1c
    mov r3, #0x0
    bl native_fn_020a9f88
    bl native_fn_0209becc
    cmp r0, #0x0
    bne main_0209b6e4_L18e
    ldr r0, =native_data12_021d19e0
    ldr r2, =native_fn_0209d0d4+1
    ldr r0, [r0, #0]
    mov r1, #0x2
    add r0, #0x1c
    mov r3, #0x0
    bl native_fn_020a9f88
    bl native_fn_0209becc
    cmp r0, #0x0
    bne main_0209b6e4_L18e
    mov r0, #0x2
    bl native_fn_0209be60
    bl native_fn_0209c538
    b main_0209b6e4_L15c
main_0209b6e4_Lfc:
    ldr r1, =0xffffb172
    mov r0, #0x3
    bl native_fn_0209c610
    pop {r3, pc}
main_0209b6e4_L106:
    ldr r1, =0xffffb17b
    mov r0, #0x4
    bl native_fn_0209c610
    pop {r3, pc}
    bl native_fn_0209c55c
    b main_0209b6e4_L15c
    bl native_fn_0209ce3c
    mov r0, #0x0
    bl native_fn_0209e488
    b main_0209b6e4_L15c
    mov r0, #0x1
    bl native_fn_0209e488
    bl native_fn_0209ce3c
    b main_0209b6e4_L15c
    bl native_fn_020a4208
    bl native_fn_0209ce3c
    ldr r0, =native_data12_021d19e0
    ldr r2, [r0, #0]
    ldr r0, =0x0000038d
    ldrb r1, [r2, r0]
    cmp r1, #0x2
    beq main_0209b6e4_L148
    ldrb r0, [r2, r0]
    cmp r0, #0x3
    bne main_0209b6e4_L150
main_0209b6e4_L148:
    mov r0, #0x1
    bl native_fn_0209e488
    b main_0209b6e4_L15c
main_0209b6e4_L150:
    ldr r0, [r2, #0]
    cmp r0, #0x0
    beq main_0209b6e4_L15c
    mov r0, #0x0
    bl native_fn_0209e488
main_0209b6e4_L15c:
    ldr r0, =native_data12_021d19e0
    ldr r2, [r0, #0]
    mov r0, #0x39
    lsl r0, r0, #0x4
    ldrb r1, [r2, r0]
    cmp r1, #0x1
    bne main_0209b6e4_L18e
    sub r0, #0x8
    ldr r0, [r2, r0]
    cmp r0, #0x0
    beq main_0209b6e4_L182
    bl native_fn_020b74d4
    ldr r0, =native_data12_021d19e0
    mov r2, #0x0
    ldr r1, [r0, #0]
    mov r0, #0xe2
    lsl r0, r0, #0x2
    str r2, [r1, r0]
main_0209b6e4_L182:
    ldr r0, =native_data12_021d19e0
    mov r2, #0x0
    ldr r1, [r0, #0]
    mov r0, #0x39
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
main_0209b6e4_L18e:
    pop {r3, pc}
}
