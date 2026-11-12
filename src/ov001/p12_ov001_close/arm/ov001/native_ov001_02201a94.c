/* ov001 row 0x02201a94: 300 bytes.
 *
 * What it does: 73 instructions; 18 call(s) to 0x021e13b8, 0x022139f8, 0x02041944, +15 more; loops (back edge at +0x08); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 18 calls (73 instructions, 18 calls, 5 branches, 11 back edges, 2 literal slots).
 *
 *   pool +0x124 -> native_data_0222ed34 (image word 0x0222ed34)
 *   pool +0x128 -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x18 -> +0x34
 *   branch +0x3c -> +0x70
 *   branch +0x50 -> +0x64
 *   branch +0x78 -> +0xa8
 *   branch +0xb4 -> +0xdc
 *   branch +0xf8 -> +0x11c
 *   test +0x0c cmp r0, #1
 *   test +0x14 cmp r4, #1
 *   test +0x38 cmp r0, #2
 *   test +0x4c cmp r0, r1
 *   test +0x74 cmp r0, #1
 *   test +0xb0 cmp r0, #0
 *   test +0xf4 cmp r0, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02201a94; the literal pool and
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

extern void native_fn_021e13b8(void);
extern u8 native_data_0222ed34[];
extern void native_fn_022139f8(void);
extern void native_fn_02041944(void);
extern void native_fn_02041538(void);
extern void native_fn_0220268c(void);
extern void native_fn_020414c8(void);
extern void native_fn_022023f8(void);
extern void native_fn_021fcd14(void);
extern void native_fn_021fe74c(void);
extern void native_fn_021fe9b0(void);
extern void native_fn_0220b70c(void);


asm u32 native_ov001_02201a94 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, #0
    bl native_fn_021e13b8
    cmp r0, #1
    moveq r4, #1
    cmp r4, #1
    bne ov001_02201a94_L34
    ldr r1, =native_data_0222ed34
    mvn r3, #0
    ldr r0, =0x02239c10
    mov r2, #2
    strb r3, [r1, #0x1]
    strb r2, [r0, #0xa]
ov001_02201a94_L34:
    bl native_fn_022139f8
    cmp r0, #2
    bne ov001_02201a94_L70
    mov r4, #1
    bl native_fn_02041944
    mvn r1, #15
    cmp r0, r1
    ble ov001_02201a94_L64
    mov r0, r4
    mov r1, #2
    mov r2, #30
    bl native_fn_02041538
ov001_02201a94_L64:
    ldr r0, =0x02239c10
    mov r1, #24
    strb r1, [r0, #0xa]
ov001_02201a94_L70:
    bl native_fn_022139f8
    cmp r0, #1
    bne ov001_02201a94_La8
    mov r0, #1
    bl native_fn_0220268c
    ldr r3, =0x02239c10
    mov r12, #23
    mov r0, #1
    mov r1, #2
    mov r2, #10
    strb r12, [r3, #0xa]
    bl native_fn_02041538
    mov r0, #63
    bl native_fn_020414c8
ov001_02201a94_La8:
    mov r0, #16
    bl native_fn_022023f8
    cmp r0, #0
    beq ov001_02201a94_Ldc
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    mov r0, #63
    bl native_fn_020414c8
    ldr r0, =0x02239c10
    mov r1, #15
    strb r1, [r0, #0xa]
ov001_02201a94_Ldc:
    mov r0, #0
    bl native_fn_021fcd14
    mov r0, #1
    bl native_fn_021fcd14
    mov r0, #32
    bl native_fn_022023f8
    cmp r0, #0
    beq ov001_02201a94_L11c
    mov r0, #0
    bl native_fn_021fe74c
    bl native_fn_021fe9b0
    mov r0, #1
    bl native_fn_0220b70c
    ldr r0, =0x02239c10
    mov r1, #19
    strb r1, [r0, #0xa]
ov001_02201a94_L11c:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
