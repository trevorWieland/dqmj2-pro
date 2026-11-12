/* ov000 row 0x021ea754: 244 bytes.
 *
 * What it does: 57 instructions; 14 call(s) to 0x02044d30, 0x0201d444, 0x0201d444, +11 more; loops (back edge at +0x2c); returns through pop {r4, r5, r6, r7, r8, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block load.
 *
 *   pool +0xe4 -> native_data_0222edfc (image word 0x0222edfc)
 *   pool +0xe8 -> native_data_0222ee00 (image word 0x0222ee00)
 *   pool +0xec -> native_data_0222ee08 (image word 0x0222ee08)
 *   pool +0xf0 -> native_data_0222ee10 (image word 0x0222ee10)
 *   branch +0x28 -> +0x44
 *   branch +0x40 -> +0x78
 *   branch +0x4c -> +0x5c
 *   branch +0x58 -> +0x78
 *   branch +0x60 -> +0x70
 *   branch +0x6c -> +0x78
 *   branch +0xa8 -> +0xb8
 *   branch +0xb4 -> +0xbc
 *   test +0x18 cmp r0, #0
 *   test +0x20 cmpne r0, #63
 *   test +0x44 cmp r5, #0
 *   test +0x5c cmp r5, #1
 *   test +0x9c cmp r5, #0
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ea754; the literal pool and
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

extern void native_fn_02044d30(void);
extern u8 native_data_0222edfc[];
extern void native_fn_0201d444(void);
extern u8 native_data_0222ee00[];
extern u8 native_data_0222ee08[];
extern u8 native_data_0222ee10[];
extern void native_fn_0202a260(void);
extern void native_fn_0202a1e0(void);
extern void native_fn_020445e4(void);
extern void native_fn_0202a280(void);
extern void native_fn_02044978(void);
extern void native_fn_02044988(void);
extern void native_fn_02044890(void);
extern void native_fn_020446f8(void);


asm u32 native_ov000_021ea754 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #32
    mov r8, r0
    ldrb r0, [sp, #0x38]
    mov r7, r1
    mov r6, r2
    cmp r0, #0
    mov r5, r3
    cmpne r0, #63
    mov r4, #20
    beq ov000_021ea754_L44
    bl native_fn_02044d30
    mov r2, r0
    ldr r1, =native_data_0222edfc
    add r0, sp, #0
    bl native_fn_0201d444
    b ov000_021ea754_L78
ov000_021ea754_L44:
    cmp r5, #0
    add r0, sp, #0
    bne ov000_021ea754_L5c
    ldr r1, =native_data_0222ee00
    bl native_fn_0201d444
    b ov000_021ea754_L78
ov000_021ea754_L5c:
    cmp r5, #1
    bne ov000_021ea754_L70
    ldr r1, =native_data_0222ee08
    bl native_fn_0201d444
    b ov000_021ea754_L78
ov000_021ea754_L70:
    ldr r1, =native_data_0222ee10
    bl native_fn_0201d444
ov000_021ea754_L78:
    bl native_fn_0202a260
    mov r0, r7
    bl native_fn_0202a1e0
    add r0, sp, #0
    mov r1, r4
    mov r2, r8
    mov r3, #0
    bl native_fn_020445e4
    bl native_fn_0202a280
    cmp r5, #0
    ldmia r6, {r1, r2, r3}
    mov r0, r8
    bne ov000_021ea754_Lb8
    add r2, r2, #4096
    bl native_fn_02044978
    b ov000_021ea754_Lbc
ov000_021ea754_Lb8:
    bl native_fn_02044978
ov000_021ea754_Lbc:
    mov r0, r8
    mov r1, #0
    bl native_fn_02044988
    mov r0, r8
    bl native_fn_02044890
    mov r0, r8
    mov r1, #1
    bl native_fn_020446f8
    add sp, sp, #32
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
