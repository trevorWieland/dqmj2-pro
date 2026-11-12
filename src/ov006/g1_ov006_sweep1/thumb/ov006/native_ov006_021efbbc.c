/* ov006 row 0x021efbbc: 156 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x88 -> native_data_02208888 (image word 0x02208888)
 *   pool +0x8c -> native_data2_0220d480 (image word 0x0220d480)
 *   pool +0x90 -> native_data2_0221aad0 (image word 0x0221aad0)
 *   pool +0x94 -> constant 0x0221af78 (image word 0x0221af78)
 *   pool +0x98 -> constant 0x0221b004 (image word 0x0221b004)
 *   back edge +0x20 -> +0x16
 *   branch +0x40 -> +0x4c
 *   branch +0x60 -> +0x6e
 *   test +0x3e cmp r1, #0x0
 *   test +0x5e cmp r1, #0x0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021efbbc; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_02208888[];
extern u8 native_data2_0220d480[];
extern void native_fn_021efa10(void);
extern u8 native_data2_0221aad0[];
extern void native_fn_021ef94c(void);


asm u32 native_ov006_021efbbc (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x10
    mov r1, #0x1
    add r4, r0, #0x0
    add r2, sp, #0x4
    lsl r1, r1, #0x8
    add r0, sp, #0x4
    strh r1, [r0, #0]
    ldr r3, =native_data_02208888
    add r2, #0x2
    mov r1, #0x7
ov006_021efbbc_L16:
    ldrb r0, [r3, #0]
    add r3, r3, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne ov006_021efbbc_L16
    ldr r0, =native_data2_0220d480
    mov r1, #0x1
    ldr r0, [r0, #0]
    add r2, sp, #0x4
    mov r3, #0x2
    bl native_fn_021efa10
    mov r1, #0x2
    add r2, sp, #0x4
    add r3, r1, #0x0
    bl native_fn_021efa10
    ldr r1, =native_data2_0221aad0
    ldr r1, [r1, #0x50]
    cmp r1, #0x0
    beq ov006_021efbbc_L4c
    mov r1, #0x5
    add r2, sp, #0x4
    mov r3, #0x2
    bl native_fn_021efa10
ov006_021efbbc_L4c:
    add r2, sp, #0x4
    mov r1, #0x3
    add r2, #0x2
    mov r3, #0x7
    bl native_fn_021efa10
    ldr r1, =native_data2_0221aad0
    add r3, r0, #0x0
    ldr r1, [r1, #0x50]
    cmp r1, #0x0
    beq ov006_021efbbc_L6e
    ldr r2, =0x0221af78
    mov r1, #0x4
    mov r3, #0x6
    bl native_fn_021efa10
    add r3, r0, #0x0
ov006_021efbbc_L6e:
    mov r0, #0x0
    str r0, [sp]
    add r0, r4, #0x0
    ldr r4, =native_data2_0220d480
    ldr r2, =0x0221b004
    ldr r4, [r4, #0]
    mov r1, #0x2
    sub r3, r3, r4
    add r3, #0x8
    bl native_fn_021ef94c
    add sp, #0x10
    pop {r4, pc}
}
