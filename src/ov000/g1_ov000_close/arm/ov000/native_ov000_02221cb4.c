/* ov000 row 0x02221cb4: 248 bytes.
 *
 * What it does: 61 instructions; 11 call(s) to 0x02041538, 0x02041814, 0x0207f254, +8 more; loops (back edge at +0x20); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xf4 -> constant 0x02246438 (image word 0x02246438)
 *   branch +0x10 -> +0x34
 *   branch +0x30 -> +0xec
 *   branch +0x38 -> +0x58
 *   branch +0x54 -> +0xec
 *   branch +0x5c -> +0xb0
 *   branch +0x68 -> +0xec
 *   branch +0xac -> +0xec
 *   branch +0xb4 -> +0xd4
 *   branch +0xd0 -> +0xec
 *   branch +0xd8 -> +0xec
 *   test +0x0c cmp r1, #0
 *   test +0x34 cmp r1, #2
 *   test +0x40 cmp r0, #1
 *   test +0x58 cmp r1, #5
 *   test +0x64 cmp r0, #0
 *   test +0xb0 cmp r1, #10
 *   test +0xbc cmp r0, #1
 *   test +0xd4 cmp r1, #100
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02221cb4; the literal pool and
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

extern void native_fn_02041538(void);
extern void native_fn_02041814(void);
extern void native_fn_0207f254(void);
extern void native_fn_0207e874(void);
extern void native_fn_0207f3b0(void);
extern void native_fn_02062e18(void);
extern void native_fn_0206de44(void);
extern void native_fn_0206de64(void);


asm u32 native_ov000_02221cb4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02246438
    ldrb r1, [r0, #0x4]
    cmp r1, #0
    bne ov000_02221cb4_L34
    mov r0, #0
    mov r1, #2
    mov r2, #15
    bl native_fn_02041538
    ldr r0, =0x02246438
    mov r1, #2
    strb r1, [r0, #0x4]
    b ov000_02221cb4_Lec
ov000_02221cb4_L34:
    cmp r1, #2
    bne ov000_02221cb4_L58
    bl native_fn_02041814
    cmp r0, #1
    ldrne r0, =0x02246438
    movne r1, #5
    strneb r1, [r0, #0x4]
    bl native_fn_0207f254
    b ov000_02221cb4_Lec
ov000_02221cb4_L58:
    cmp r1, #5
    bne ov000_02221cb4_Lb0
    bl native_fn_0207e874
    cmp r0, #0
    beq ov000_02221cb4_Lec
    bl native_fn_0207f3b0
    ldr r2, =0x02246438
    mov r1, r0
    ldr r0, [r2, #0xc]
    bl native_fn_02062e18
    mov r0, #1
    bl native_fn_0206de44
    mov r0, #1
    bl native_fn_0206de64
    mov r0, #1
    mov r1, #2
    mov r2, #15
    bl native_fn_02041538
    ldr r0, =0x02246438
    mov r1, #10
    strb r1, [r0, #0x4]
    b ov000_02221cb4_Lec
ov000_02221cb4_Lb0:
    cmp r1, #10
    bne ov000_02221cb4_Ld4
    bl native_fn_02041814
    cmp r0, #1
    ldrne r0, =0x02246438
    movne r1, #100
    strneb r1, [r0, #0x4]
    bl native_fn_0207f254
    b ov000_02221cb4_Lec
ov000_02221cb4_Ld4:
    cmp r1, #100
    bne ov000_02221cb4_Lec
    mov r1, #0
    strb r1, [r0, #0x4]
    mov r1, #3
    str r1, [r0, #0x18]
ov000_02221cb4_Lec:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
