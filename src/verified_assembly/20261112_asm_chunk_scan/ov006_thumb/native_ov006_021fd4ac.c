/* ov006 row 0x021fd4ac: 212 bytes.
 *
 * What it does: Moves 2-register chunks between two pointers with writeback block moves (one load, 3 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xbc -> native_data2_0221c114 (image word 0x0221c114)
 *   pool +0xc0 -> native_fn_021fc870+1 (image word 0x021fc871)
 *   pool +0xc4 -> native_fn_021fc514+1 (image word 0x021fc515)
 *   pool +0xc8 -> native_fn_021f79c8+1 (image word 0x021f79c9)
 *   pool +0xcc -> native_fn_021fc204+1 (image word 0x021fc205)
 *   pool +0xd0 -> native_fn_021fa164+1 (image word 0x021fa165)
 *   branch +0x0a -> +0xb8
 *   branch +0x14 -> +0xb8
 *   branch +0x1c -> +0xb8
 *   branch +0x44 -> +0x56
 *   branch +0x5c -> +0xb8
 *   test +0x08 cmp r0, #0x0
 *   test +0x12 cmp r0, #0x0
 *   test +0x1a cmp r0, #0x0
 *   test +0x42 cmp r1, #0x0
 *   test +0x5a cmp r0, #0x3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fd4ac; the literal pool and
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

extern void native_fn_02203188(void);
extern void native_fn_021f23c4(void);
extern void native_fn_021f2a4c(void);
extern void native_fn_021f2774(void);
extern u8 native_data2_0221c114[];
extern void native_fn_02202b24(void);
extern void native_fn_02203954(void);
extern void native_fn_021f52d8(void);
extern void native_fn_021fc870(void);
extern void ov006_main_loop_set_callback_021f52cc(void);
extern void native_fn_021fc514(void);
extern void native_fn_021f79c8(void);
extern void native_fn_021fc204(void);
extern void native_fn_021f5300(void);
extern void native_fn_021fb930(void);
extern void native_fn_021fa164(void);


asm u32 native_ov006_021fd4ac (register u32 a0)
{
    push {r3, lr}
    mov r0, #0x1
    bl native_fn_02203188
    cmp r0, #0x0
    bne ov006_021fd4ac_Lb8
    mov r0, #0x0
    bl native_fn_02203188
    cmp r0, #0x0
    bne ov006_021fd4ac_Lb8
    bl native_fn_021f23c4
    cmp r0, #0x0
    beq ov006_021fd4ac_Lb8
    bl native_fn_021f2a4c
    bl native_fn_021f2774
    ldr r0, =native_data2_0221c114
    ldr r0, [r0, #0x4]
    bl native_fn_02202b24
    mov r0, #0x1
    add r1, r0, #0x0
    bl native_fn_02203954
    mov r0, #0x0
    mov r1, #0x14
    bl native_fn_02203954
    ldr r0, =native_data2_0221c114
    ldrb r1, [r0, #0x2]
    cmp r1, #0x0
    bne ov006_021fd4ac_L56
    mov r0, #0x2
    mov r1, #0x0
    bl native_fn_021f52d8
    ldr r0, =native_fn_021fc870+1
    bl ov006_main_loop_set_callback_021f52cc
    pop {r3, pc}
ov006_021fd4ac_L56:
    mov r1, #0x1
    ldrsb r0, [r0, r1]
    cmp r0, #0x3
    bhi ov006_021fd4ac_Lb8
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    lsl r6, r0, #0
    lsl r4, r2, #0
    lsl r2, r4, #0
    lsl r0, r6, #0
    mov r0, #0x2
    bl native_fn_021f52d8
    ldr r0, =native_fn_021fc514+1
    bl ov006_main_loop_set_callback_021f52cc
    pop {r3, pc}
    mov r0, #0x2
    bl native_fn_021f52d8
    ldr r0, =native_fn_021f79c8+1
    bl ov006_main_loop_set_callback_021f52cc
    pop {r3, pc}
    mov r0, #0x2
    bl native_fn_021f52d8
    ldr r0, =native_fn_021fc204+1
    bl ov006_main_loop_set_callback_021f52cc
    pop {r3, pc}
    mov r0, #0x2
    mov r1, #0x0
    bl native_fn_021f52d8
    mov r0, #0x0
    add r1, r0, #0x0
    bl native_fn_021f5300
    mov r0, #0x1
    bl native_fn_021fb930
    ldr r0, =native_fn_021fa164+1
    bl ov006_main_loop_set_callback_021f52cc
ov006_021fd4ac_Lb8:
    pop {r3, pc}
    mov r8, r8
}
