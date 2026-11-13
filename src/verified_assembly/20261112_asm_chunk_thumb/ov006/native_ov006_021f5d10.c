/* ov006 row 0x021f5d10: 112 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (one load, one store).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x64 -> native_data2_0221c09c (image word 0x0221c09c)
 *   pool +0x68 -> native_fn_021fc870+1 (image word 0x021fc871)
 *   pool +0x6c -> native_fn_021f6544+1 (image word 0x021f6545)
 *   branch +0x0a -> +0x62
 *   branch +0x14 -> +0x62
 *   branch +0x3c -> +0x44
 *   branch +0x40 -> +0x54
 *   test +0x08 cmp r0, #0x0
 *   test +0x12 cmp r0, #0x0
 *   test +0x3a cmp r0, #0x0
 *   test +0x3e cmp r0, #0x1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f5d10; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 112 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02203188(void);
extern void native_fn_021f2a4c(void);
extern void native_fn_021f2774(void);
extern u8 native_data2_0221c09c[];
extern void native_fn_02202b24(void);
extern void native_fn_02203954(void);
extern void native_fn_021f52d8(void);
extern void native_fn_021fc870(void);
extern void ov006_main_loop_set_callback_021f52cc(void);
extern void native_fn_021f6544(void);


asm u32 native_ov006_021f5d10 (register u32 a0)
{
    push {r3, lr}
    mov r0, #0x1
    bl native_fn_02203188
    cmp r0, #0x0
    bne ov006_021f5d10_L62
    mov r0, #0x0
    bl native_fn_02203188
    cmp r0, #0x0
    bne ov006_021f5d10_L62
    bl native_fn_021f2a4c
    bl native_fn_021f2774
    ldr r0, =native_data2_0221c09c
    ldr r0, [r0, #0x4]
    bl native_fn_02202b24
    mov r0, #0x1
    add r1, r0, #0x0
    bl native_fn_02203954
    mov r0, #0x0
    mov r1, #0x14
    bl native_fn_02203954
    ldr r0, =native_data2_0221c09c
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq ov006_021f5d10_L44
    cmp r0, #0x1
    beq ov006_021f5d10_L54
    pop {r3, pc}
ov006_021f5d10_L44:
    mov r0, #0x1
    mov r1, #0x0
    bl native_fn_021f52d8
    ldr r0, =native_fn_021fc870+1
    bl ov006_main_loop_set_callback_021f52cc
    pop {r3, pc}
ov006_021f5d10_L54:
    mov r0, #0x0
    add r1, r0, #0x0
    bl native_fn_021f52d8
    ldr r0, =native_fn_021f6544+1
    bl ov006_main_loop_set_callback_021f52cc
ov006_021f5d10_L62:
    pop {r3, pc}
}
