/* ov006 row 0x021fff94: 148 bytes.
 *
 * What it does: Writes 2 blocks of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x7c -> native_data_0221c158 (image word 0x0221c158)
 *   pool +0x80 -> constant 0x00001b94 (image word 0x00001b94)
 *   pool +0x84 -> constant 0x000013b8 (image word 0x000013b8)
 *   pool +0x88 -> native_fn_0220003c+1 (image word 0x0220003d)
 *   pool +0x8c -> constant 0x00001b90 (image word 0x00001b90)
 *   pool +0x90 -> native_data_0221c158 (image word 0x0221c158)
 *   branch +0x20 -> +0x46
 *   branch +0x2a -> +0x30
 *   back edge +0x44 -> +0x36
 *   branch +0x4e -> +0x54
 *   branch +0x5e -> +0x66
 *   back edge +0x70 -> +0x6c
 *   test +0x1e cmp r0, #0x2
 *   test +0x28 cmp r0, #0x2
 *   test +0x42 cmp r0, #0x2
 *   test +0x4c cmp r0, #0x2
 *   test +0x5c cmp r1, #0x0
 *   test +0x6e cmp r1, #0x2
 *   1 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fff94; the literal pool and
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

extern u8 native_data5_0221c158[];
extern void native_fn_02012030(void);
extern void native_fn2_0220003c(void);
extern void native_fn_020127ec(void);
extern void native_fn_02012824(void);
extern void native_fn_0220498c(void);
extern u8 native_data6_0221c158[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_021fff94 (register u32 a0)
{
    push {r4, r5, r6, lr}
    ldr r1, =native_data5_0221c158
    ldr r0, =0x00001b94
    ldr r2, [r1, #0]
    mov r3, #0x1
    strb r3, [r2, r0]
    ldr r1, [r1, #0]
    ldr r0, =0x000013b8
    add r0, r1, r0
    blx native_fn_02012030
    ldr r0, =native_data5_0221c158
    ldr r1, [r0, #0]
    ldr r0, =0x000013b8
    ldrh r0, [r1, r0]
    cmp r0, #0x2
    beq ov006_021fff94_L46
    ldr r0, =native_fn2_0220003c+1
    blx native_fn_020127ec
    cmp r0, #0x2
    beq ov006_021fff94_L30
    mov r0, #0x0
    pop {r4, r5, r6, pc}
ov006_021fff94_L30:
    ldr r6, =0x000013b8
    ldr r5, =native_data5_0221c158
    add r4, r6, #0x0
ov006_021fff94_L36:
    ldr r0, [r5, #0]
    add r0, r0, r6
    blx native_fn_02012030
    ldr r0, [r5, #0]
    ldrh r0, [r0, r4]
    cmp r0, #0x2
    bne ov006_021fff94_L36
ov006_021fff94_L46:
    ldr r0, =native_fn2_0220003c+1
    blx native_fn_02012824
    cmp r0, #0x2
    beq ov006_021fff94_L54
    mov r0, #0x0
    pop {r4, r5, r6, pc}
ov006_021fff94_L54:
    ldr r0, =native_data5_0221c158
    ldr r1, [r0, #0]
    ldr r0, =0x00001b90
    ldr r1, [r1, r0]
    cmp r1, #0x0
    beq ov006_021fff94_L66
    mov r0, #0x0
    bl native_fn_0220498c
ov006_021fff94_L66:
    ldr r0, =native_data5_0221c158
    ldr r2, [r0, #0]
    ldr r0, =0x00001b94
ov006_021fff94_L6c:
    ldrb r1, [r2, r0]
    cmp r1, #0x2
    bne ov006_021fff94_L6c
    ldr r0, =native_data6_0221c158
    bl native_fn_02203c20
    mov r0, #0x1
    pop {r4, r5, r6, pc}
}
