/* ov000 row 0x021fe1e8: 392 bytes.
 *
 * What it does: 96 instructions; 21 call(s) to 0x02215698, 0x0202a634, 0x022156c4, +18 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x180 -> constant 0x022372bc (image word 0x022372bc)
 *   pool +0x184 -> constant 0x022372c4 (image word 0x022372c4)
 *   branch +0x34 -> +0x44
 *   branch +0x3c -> +0x94
 *   branch +0x40 -> +0x124
 *   branch +0x90 -> +0x124
 *   branch +0xa4 -> +0xd0
 *   branch +0xbc -> +0x10c
 *   branch +0xcc -> +0x10c
 *   branch +0xd4 -> +0x100
 *   branch +0xe4 -> +0x10c
 *   branch +0xfc -> +0x10c
 *   branch +0x118 -> +0x124
 *   branch +0x128 -> +0x168
 *   branch +0x134 -> +0x154
 *   branch +0x144 -> +0x154
 *   branch +0x16c -> +0x178
 *   test +0x2c cmp r1, #0
 *   test +0x38 cmp r1, #1
 *   test +0x9c tst r0, #2
 *   test +0xb8 cmp r0, #0
 *   test +0xd0 tst r0, #1
 *   test +0xe0 cmp r0, #0
 *   test +0x114 cmp r0, #0
 *   test +0x124 cmp r8, #0
 *   test +0x130 cmp r9, r0
 *   test +0x140 cmp r0, #0
 *   test +0x168 cmp r6, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fe1e8; the literal pool and
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

extern void native_fn_02215698(void);
extern void native_fn_0202a634(void);
extern void native_fn_022156c4(void);
extern void native_fn_021fe450(void);
extern void native_fn_02215094(void);
extern void native_fn_0204b61c(void);
extern void native_fn_02217ac8(void);
extern void native_fn_021fe0ac(void);
extern void native_fn_02063bdc(void);
extern void native_fn_02063c94(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_0221794c(void);
extern void native_fn_02072590(void);
extern void native_fn_021fe0d4(void);
extern void native_fn_021fe4b0(void);
extern void native_fn_021fe724(void);


asm u32 native_ov000_021fe1e8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    bl native_fn_02215698
    mov r5, r0
    mov r6, #0
    bl native_fn_0202a634
    mov r4, r0
    bl native_fn_022156c4
    ldr r1, =0x022372bc
    mov r8, r6
    ldr r1, [r1]
    mov r7, r0
    cmp r1, #0
    sub r9, r8, #1
    beq ov000_021fe1e8_L44
    cmp r1, #1
    beq ov000_021fe1e8_L94
    b ov000_021fe1e8_L124
ov000_021fe1e8_L44:
    ldr r6, =0x022372c4
    mov r0, #1
    bl native_fn_021fe450
    mov r1, #240
    mov r4, #128
    mov r3, r1
    add r0, r6, #168
    mov r2, #40
    str r4, [sp]
    bl native_fn_02215094
    add r0, r5, #16
    mov r1, #1
    bl native_fn_0204b61c
    ldr r1, =0x022372bc
    mov r2, #1
    mov r0, r8
    str r2, [r1]
    bl native_fn_02217ac8
    mov r8, #1
    b ov000_021fe1e8_L124
ov000_021fe1e8_L94:
    ldrh r0, [r4, #2]
    ldr r6, =0x022372c4
    tst r0, #2
    ldr r9, [r6]
    beq ov000_021fe1e8_Ld0
    mov r0, #1
    bl native_fn_021fe0ac
    mov r0, r9
    bl native_fn_02063bdc
    cmp r0, #0
    beq ov000_021fe1e8_L10c
    mov r0, r9
    mov r1, r8
    bl native_fn_02063c94
    b ov000_021fe1e8_L10c
ov000_021fe1e8_Ld0:
    tst r0, #1
    beq ov000_021fe1e8_L100
    mov r0, r9
    bl native_fn_02063bdc
    cmp r0, #0
    beq ov000_021fe1e8_L10c
    mov r0, r9
    mov r1, r8
    bl native_fn_02063c94
    mov r0, #82
    bl native_fn_021e7b9c
    b ov000_021fe1e8_L10c
ov000_021fe1e8_L100:
    mov r0, r6
    bl native_fn_0221794c
    mov r8, r0
ov000_021fe1e8_L10c:
    mov r0, #0
    bl native_fn_02072590
    cmp r0, #0
    bne ov000_021fe1e8_L124
    ldr r0, [r6]
    bl native_fn_021fe0d4
ov000_021fe1e8_L124:
    cmp r8, #0
    beq ov000_021fe1e8_L168
    mvn r0, #0
    cmp r9, r0
    beq ov000_021fe1e8_L154
    mov r0, r9
    bl native_fn_02063bdc
    cmp r0, #0
    beq ov000_021fe1e8_L154
    mov r0, r9
    mov r1, #0
    bl native_fn_02063c94
ov000_021fe1e8_L154:
    ldr r0, =0x022372bc
    ldr r0, [r0]
    bl native_fn_021fe4b0
    ldr r0, [r6]
    bl native_fn_021fe0d4
ov000_021fe1e8_L168:
    cmp r6, #0
    beq ov000_021fe1e8_L178
    mov r0, r6
    bl native_fn_021fe724
ov000_021fe1e8_L178:
    mov r0, r7
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
