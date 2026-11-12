/* ov000 row 0x021fe0d4: 276 bytes.
 *
 * What it does: 68 instructions; 12 call(s) to 0x02063bbc, 0x02048094, 0x021fe180, +9 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, r6, r7, r8, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x110 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x34 -> +0x44
 *   branch +0x4c -> +0x70
 *   back edge +0x6c -> +0x54
 *   branch +0x84 -> +0xac
 *   back edge +0xa8 -> +0x90
 *   test +0x2c cmp r0, #0
 *   test +0x68 cmp r6, #0
 *   test +0x7c cmp r8, #0
 *   test +0xa4 cmp r7, r8
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fe0d4; the literal pool and
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

extern void native_fn_02063bbc(void);
extern void native_fn_02048094(void);
extern void native_fn_02047ff0(void);
extern void native_fn_0205dc70(void);
extern void native_fn_02048034(void);
extern void native_fn_02072568(void);
extern void native_fn_0206de44(void);


asm u32 native_ov000_021fe0d4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #4
    add r3, sp, #0
    mov r2, #0
    strb r2, [r3]
    mov r1, #11
    mov r6, r0
    strb r2, [r3, #0x1]
    strb r1, [sp]
    mov r4, #1
    bl native_fn_02063bbc
    cmp r0, #0
    moveq r5, #0
    beq ov000_021fe0d4_L44
    add r0, r6, #1
    mov r0, r0, lsl #16
    mov r5, r0, lsr #16
ov000_021fe0d4_L44:
    adds r0, r6, #1
    mov r6, r0
    beq ov000_021fe0d4_L70
    ldr r2, =0x66666667
ov000_021fe0d4_L54:
    mov r3, r6
    smull r1, r6, r2, r3
    mov r1, r3, lsr #31
    adds r6, r1, r6, asr #2
    addne r4, r4, #1
    cmp r6, #0
    bne ov000_021fe0d4_L54
ov000_021fe0d4_L70:
    mov r1, #0
    bl native_fn_02048094
    rsb r8, r4, #3
    cmp r8, #0
    mov r7, #0
    ble ov000_021fe0d4_Lac
    add r6, sp, #0
    mov r4, #1
ov000_021fe0d4_L90:
    mov r0, r6
    mov r1, r4
    add r2, r7, #16
    bl native_fn_02047ff0
    add r7, r7, #1
    cmp r7, r8
    blt ov000_021fe0d4_L90
ov000_021fe0d4_Lac:
    mov r2, r5
    mov r0, #18
    mov r1, #0
    bl native_fn_0205dc70
    mov r1, #32
    bl native_fn_02048034
    mov r0, #18
    mov r1, #2
    mov r2, #0
    bl native_fn_0205dc70
    mov r1, r0
    mov r0, #0
    bl native_fn_02072568
    mov r2, r5
    mov r0, #18
    mov r1, #1
    bl native_fn_0205dc70
    mov r1, r0
    mov r0, #1
    bl native_fn_02072568
    mov r0, #1
    bl native_fn_0206de44
    mov r0, #0
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
