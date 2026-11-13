#include "context.h"
void native_ov000_021f8134(void)
{
    MenuView *menu=(MenuView *)ov000_display_context_02215698();
    Point position;
    if(!native_fn_ov000_02215a7c())native_fn_ov000_021f7f9c();
    native_fn_ov000_021f8044();
    native_fn_0204b1c4(&menu->cursor,0,&position,2,2,15);
    native_fn_0204b380(&menu->cursor,0);
    if(!menu->alternate){
        RosterSlot *slot;
        native_fn_ov000_021f9148(0);
        native_fn_02062120(menu->column);
        slot=&menu->slots[menu->column];
        position.x=slot->x;position.y=slot->y;
        native_fn_0204b2d0(&menu->cursor,native_fn_0206d250(slot->resource),&position);
    }else{
        if(!native_fn_ov000_021f9118(menu->row,menu->column))native_fn_ov000_021f9118((s8)(menu->row+1),menu->column);
        native_fn_ov000_021f9484(&position,menu->row,menu->column);
        native_fn_0204b2d0(&menu->cursor,0,&position);
    }
    native_fn_ov000_021f8b40();native_fn_ov000_021f8c20();native_fn_ov000_021f8d28();
    native_fn_ov000_021f8db4(3,7,(u8)native_fn_02063b40(144));
    native_fn_ov000_021f8db4(4,8,(u8)native_fn_02063b40(75));
    native_fn_ov000_021f8db4(5,9,(u8)native_fn_02063b40(76));
    native_fn_ov000_021f8db4(6,6,(u8)native_fn_02063b40(22));
    native_fn_ov000_021f8db4(7,10,(u8)native_fn_02063b40(23));
}
