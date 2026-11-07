#include "../../../../resource_path_api.h"
#include "context.h"
int native_main_0205c668(int id,int release)
{
    int result=0;
    if(native_fn_0205c404()==0) {
        ResourceSlot *slot=native_fn_0205c448();
        if(slot) {
            char name[16];
            u32 size;
            void *data;
            native_fn_0201d444(name,(const char*)0x20ddbcc,id);
            size=native_fn_0202a8e0(name);
            if(size) {
                data=native_fn_0202a428(size,4);
                if(data) {
                    if(native_fn_0202a818((u32)name,(u32)data,size,0)) {
                        native_fn_0205c49c(data,slot,id,0,release);
                        native_fn_0205c49c(data,slot,id,4,release);
                        native_fn_0205c49c(data,slot,id,1,release);
                        native_fn_0205c49c(data,slot,id,2,release);
                        native_fn_0205c49c(data,slot,id,3,release);
                        native_fn_0205c49c(data,slot,id,5,release);
                        slot->data=data;slot->id=id;result=1;
                    }
                    if(release)native_fn_0205c618(data,id);
                }
            }
        }
    }
    return result;
}
