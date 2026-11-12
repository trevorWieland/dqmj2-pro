/* ov006 row 0x021feaa0: 148 bytes.
 *
 * What it does: Moves 2-register chunks between two pointers with writeback block moves (one load, 2 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x7c -> native_data_0221c144 (image word 0x0221c144)
 *   pool +0x80 -> native_fn_021fec00+1 (image word 0x021fec01)
 *   pool +0x84 -> constant 0x0000168c (image word 0x0000168c)
 *   pool +0x88 -> constant 0x00001648 (image word 0x00001648)
 *   pool +0x8c -> native_data_0220b9ac (image word 0x0220b9ac)
 *   pool +0x90 -> constant 0x00001650 (image word 0x00001650)
 *   branch +0x24 -> +0x2a
 *   back edge +0x3e -> +0x30
 *   back edge +0x4e -> +0x48
 *   branch +0x70 -> +0x76
 *   test +0x22 cmp r0, #0x2
 *   test +0x3c cmp r0, #0x2
 *   test +0x6e cmp r0, #0x0
 *   3 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021feaa0; the literal pool and
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

extern u8 native_data4_0221c144[];
extern void native_fn_02008be0(void);
extern void native_fn_021fec00(void);
extern void native_fn_02012764(void);
extern void native_fn_02012030(void);
extern u8 native_data_0220b9ac[];
extern void native_fn_020123d0(void);
extern void native_fn_021feb34(void);


asm u32 native_ov006_021feaa0 (register u32 a0)
{
    push {r4, r5, r6, lr}
    ldr r1, =native_data4_0221c144
    mov r0, #0x0
    ldr r2, [r1, #0]
    mov r1, #0x13
    lsl r1, r1, #0x8
    add r1, r2, r1
    mov r2, #0xd2
    lsl r2, r2, #0x2
    blx native_fn_02008be0
    ldr r0, =native_data4_0221c144
    ldr r1, =native_fn_021fec00+1
    ldr r0, [r0, #0]
    mov r2, #0x3
    blx native_fn_02012764
    cmp r0, #0x2
    beq ov006_021feaa0_L2a
    mov r0, #0x0
    pop {r4, r5, r6, pc}
ov006_021feaa0_L2a:
    ldr r6, =0x0000168c
    ldr r5, =native_data4_0221c144
    add r4, r6, #0x0
ov006_021feaa0_L30:
    ldr r0, [r5, #0]
    add r0, r0, r6
    blx native_fn_02012030
    ldr r2, [r5, #0]
    ldrh r0, [r2, r4]
    cmp r0, #0x2
    bne ov006_021feaa0_L30
    ldr r0, =0x00001648
    ldr r5, =native_data_0220b9ac
    add r4, r2, r0
    mov r3, #0x8
ov006_021feaa0_L48:
    ldmia r5!, {r0, r1}
    stmia r4!, {r0, r1}
    sub r3, r3, #0x1
    bne ov006_021feaa0_L48
    ldr r0, [r5, #0]
    str r0, [r4, #0]
    mov r0, #0xf
    lsl r0, r0, #0x8
    add r1, r2, r0
    ldr r0, =0x00001648
    str r1, [r2, r0]
    blx native_fn_020123d0
    ldr r1, =native_data4_0221c144
    ldr r2, [r1, #0]
    ldr r1, =0x00001650
    strh r0, [r2, r1]
    bl native_fn_021feb34
    cmp r0, #0x0
    beq ov006_021feaa0_L76
    mov r0, #0x1
    pop {r4, r5, r6, pc}
ov006_021feaa0_L76:
    mov r0, #0x0
    pop {r4, r5, r6, pc}
    mov r8, r8
}
