/* ov006 row 0x021ffe5c: 272 bytes.
 *
 * What it does: Moves 2-register chunks between two pointers with writeback block moves (one load, 3 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xd4 -> constant 0x00001ba0 (image word 0x00001ba0)
 *   pool +0xd8 -> native_data_0221c158 (image word 0x0221c158)
 *   pool +0xdc -> constant 0x00001370 (image word 0x00001370)
 *   pool +0xe0 -> constant 0x00001b88 (image word 0x00001b88)
 *   pool +0xe4 -> native_fn_0220003c+1 (image word 0x0220003d)
 *   pool +0xe8 -> constant 0x000013b8 (image word 0x000013b8)
 *   pool +0xec -> constant 0x00001374 (image word 0x00001374)
 *   pool +0xf0 -> native_data_0220ba3c (image word 0x0220ba3c)
 *   pool +0xf4 -> constant 0x0000137c (image word 0x0000137c)
 *   pool +0xf8 -> native_data_0220ba30 (image word 0x0220ba30)
 *   pool +0xfc -> constant 0x00001388 (image word 0x00001388)
 *   pool +0x100 -> constant 0x00001391 (image word 0x00001391)
 *   pool +0x104 -> native_fn_0220026c+1 (image word 0x0220026d)
 *   pool +0x108 -> constant 0x00001b90 (image word 0x00001b90)
 *   pool +0x10c -> native_data_0221c158 (image word 0x0221c158)
 *   branch +0x32 -> +0xc8
 *   back edge +0x48 -> +0x3a
 *   back edge +0x58 -> +0x52
 *   branch +0xac -> +0xc8
 *   test +0x30 cmp r0, #0x2
 *   test +0x46 cmp r0, #0x2
 *   test +0xaa cmp r0, #0x0
 *   9 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ffe5c; the literal pool and
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

extern void ov006_clear_buffer_02203c08(void);
extern u8 native_data7_0221c158[];
extern void native_fn_02007a9c(void);
extern void native_fn_0220003c(void);
extern void native_fn_02012764(void);
extern void native_fn_02012030(void);
extern u8 native_data_0220ba3c[];
extern void native_fn_020123d0(void);
extern void native_fn_02008218(void);
extern u8 native_data_0220ba30[];
extern void native_fn_02008e0c(void);
extern void native_fn_021fff6c(void);
extern void native_fn_0220026c(void);
extern void native_fn_0220490c(void);
extern u8 native_data8_0221c158[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_021ffe5c (register u32 a0)
{
    push {r3, r4, r5, r6, lr}
    sub sp, #0x54
    add r4, r0, #0x0
    ldr r0, =0x00001ba0
    mov r1, #0x20
    bl ov006_clear_buffer_02203c08
    ldr r1, =native_data7_0221c158
    str r0, [r1, #0]
    ldr r1, =0x00001370
    str r4, [r0, r1]
    blx native_fn_02007a9c
    ldr r3, =native_data7_0221c158
    ldr r2, =0x00001b88
    ldr r4, [r3, #0]
    str r0, [r4, r2]
    add r0, r2, #0x4
    str r1, [r4, r0]
    ldr r0, [r3, #0]
    ldr r1, =native_fn_0220003c+1
    mov r2, #0x3
    blx native_fn_02012764
    cmp r0, #0x2
    bne ov006_021ffe5c_Lc8
    ldr r6, =0x000013b8
    ldr r5, =native_data7_0221c158
    add r4, r6, #0x0
ov006_021ffe5c_L3a:
    ldr r0, [r5, #0]
    add r0, r0, r6
    blx native_fn_02012030
    ldr r2, [r5, #0]
    ldrh r0, [r2, r4]
    cmp r0, #0x2
    bne ov006_021ffe5c_L3a
    ldr r0, =0x00001374
    ldr r5, =native_data_0220ba3c
    add r4, r2, r0
    mov r3, #0x8
ov006_021ffe5c_L52:
    ldmia r5!, {r0, r1}
    stmia r4!, {r0, r1}
    sub r3, r3, #0x1
    bne ov006_021ffe5c_L52
    ldr r0, [r5, #0]
    str r0, [r4, #0]
    mov r0, #0xf
    lsl r0, r0, #0x8
    add r1, r2, r0
    ldr r0, =0x00001374
    str r1, [r2, r0]
    blx native_fn_020123d0
    ldr r1, =native_data7_0221c158
    ldr r2, [r1, #0]
    ldr r1, =0x0000137c
    strh r0, [r2, r1]
    add r0, sp, #0x0
    blx native_fn_02008218
    ldr r1, =native_data7_0221c158
    ldr r0, =native_data_0220ba30
    ldr r2, [r1, #0]
    ldr r1, =0x00001388
    add r1, r2, r1
    mov r2, #0x8
    blx native_fn_02008e0c
    ldr r2, =native_data7_0221c158
    ldr r1, =0x00001391
    ldr r0, [r2, #0]
    mov r3, #0x1
    strb r3, [r0, r1]
    ldr r2, [r2, #0]
    add r1, r1, #0x3
    add r1, r2, r1
    add r2, sp, #0x0
    ldrh r2, [r2, #0x1a]
    add r0, sp, #0x4
    lsl r2, r2, #0x1
    blx native_fn_02008e0c
    bl native_fn_021fff6c
    cmp r0, #0x0
    beq ov006_021ffe5c_Lc8
    mov r0, #0x0
    ldr r1, =native_fn_0220026c+1
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, =native_data7_0221c158
    add sp, #0x54
    ldr r2, [r1, #0]
    ldr r1, =0x00001b90
    str r0, [r2, r1]
    mov r0, #0x1
    pop {r3, r4, r5, r6, pc}
ov006_021ffe5c_Lc8:
    ldr r0, =native_data8_0221c158
    bl native_fn_02203c20
    mov r0, #0x0
    add sp, #0x54
    pop {r3, r4, r5, r6, pc}
}
