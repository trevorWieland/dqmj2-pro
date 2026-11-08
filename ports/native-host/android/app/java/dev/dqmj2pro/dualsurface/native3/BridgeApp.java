package dev.dqmj2pro.dualsurface.native3;

import android.app.ActivityManager;
import android.app.ActivityOptions;
import android.app.Application;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.hardware.display.DisplayManager;
import android.hardware.display.VirtualDisplay;
import android.media.Image;
import android.media.ImageReader;
import android.graphics.PixelFormat;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.Display;
import java.util.Arrays;
import java.util.HashSet;

public final class BridgeApp extends Application implements DisplayManager.DisplayListener {
    final Handler handler = new Handler(Looper.getMainLooper());
    final HashSet<Integer> denied = new HashSet<>();
    DisplayManager displays;
    HostActivity primary, secondary;
    int pending = -1, visible;
    boolean fallback, ticking;
    long token;
    VirtualDisplay ownedDisplay;
    ImageReader reader;
    int preferred = -1;
    static void event(String name, String value) { Log.i("J2P_HOST", name + " " + value); }
    @Override public void onCreate() {
        super.onCreate();
        displays = getSystemService(DisplayManager.class);
        displays.registerDisplayListener(this, handler);
        event("C7_SELFTEST", "exit=" + NativeBridge.init());
    }
    long nextToken() { return ++token; }
    void opened(HostActivity activity) {
        if (activity.role() == 0) primary = activity;
        else { secondary = activity; pending = -1; }
        event("ACTIVITY", "role=" + activity.role() + " display=" + activity.getDisplay().getDisplayId());
        handler.post(this::reconcile);
    }
    void closed(HostActivity activity) {
        if (activity == primary) {
            primary = null;
            if (secondary != null) secondary.finish();
            if (ownedDisplay != null) { ownedDisplay.release(); ownedDisplay = null; }
            if (reader != null) { reader.close(); reader = null; }
        }
        if (activity == secondary) { secondary = null; pending = -1; }
        handler.post(this::reconcile);
    }
    void visible(int delta) {
        visible += delta;
        if (visible > 0 && !ticking) { ticking = true; handler.post(tick); }
    }
    final Runnable tick = new Runnable() {
        long count;
        @Override public void run() {
            if (visible <= 0) { ticking = false; return; }
            NativeBridge.frame();
            if (++count % 60 == 0) report();
            handler.postDelayed(this, 33);
        }
    };
    void report() { event("STATE", NativeBridge.state()); }
    void reconcile() {
        if (primary == null || primary.isFinishing()) return;
        Display[] all = displays.getDisplays();
        Arrays.sort(all, (a, b) -> Integer.compare(a.getDisplayId(), b.getDisplayId()));
        Intent intent = new Intent(this, SecondActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        int chosen = -1;
        if (!fallback) for (Display display : all) {
            int id = display.getDisplayId();
            if (!display.isValid() || id == primary.getDisplay().getDisplayId() || denied.contains(id)) continue;
            boolean allowed = getSystemService(ActivityManager.class).isActivityStartAllowedOnDisplay(this, id, intent);
            event("DISCOVER", "id=" + id + " flags=" + display.getFlags() + " rotation=" + display.getRotation() + " allowed=" + allowed);
            if (allowed && (chosen < 0 || id == preferred)) chosen = id;
        }
        if (secondary != null && (secondary.getDisplay() == null || secondary.getDisplay().getDisplayId() != chosen)) {
            event("RETIRE", "display=" + (secondary.getDisplay() == null ? -1 : secondary.getDisplay().getDisplayId()));
            secondary.finish();
            return;
        }
        primary.displayMode(chosen < 0);
        if (chosen < 0 || secondary != null || pending >= 0) return;
        final int target = chosen;
        pending = target;
        try {
            startActivity(intent, ActivityOptions.makeBasic().setLaunchDisplayId(target).toBundle());
            event("LAUNCH", "id=" + target);
        } catch (RuntimeException error) {
            pending = -1;
            denied.add(target);
            event("LAUNCH_REFUSED", error.toString());
            handler.post(this::reconcile);
        }
        handler.postDelayed(() -> {
            if (pending == target) { pending = -1; denied.add(target); event("LAUNCH_TIMEOUT", "id=" + target); reconcile(); }
        }, 3000);
    }
    void command(String name) {
        event("COMMAND", name);
        if (name.equals("single")) { fallback = true; reconcile(); }
        else if (name.equals("dual")) { fallback = false; denied.clear(); reconcile(); }
        else if (name.equals("capture")) {
            if (primary != null) primary.capture();
            if (secondary != null) secondary.capture();
        } else if (name.equals("guard-check")) {
            if (primary != null) primary.guardCheck();
            if (secondary != null) secondary.guardCheck();
        } else if (name.equals("capture-clean")) {
            for (int slot = 0; slot < 2; ++slot) {
                java.io.File file = new java.io.File(getFilesDir(), "capture-slot-" + slot + ".png");
                if (file.exists() && !file.delete()) throw new IllegalStateException("Own capture cleanup");
                event("OWNED_CAPTURE_ABSENT", "slot=" + slot + " absent=" + !file.exists());
            }
        }
        else if (name.equals("portrait") || name.equals("landscape")) {
            int orientation = name.equals("portrait") ? ActivityInfo.SCREEN_ORIENTATION_PORTRAIT : ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE;
            if (primary != null) primary.setRequestedOrientation(orientation);
            if (secondary != null) secondary.setRequestedOrientation(orientation);
        } else if (name.equals("virtual-add")) {
            if (ownedDisplay != null) return;
            reader = ImageReader.newInstance(256, 192, PixelFormat.RGBA_8888, 2);
            reader.setOnImageAvailableListener(r -> { Image image = r.acquireLatestImage(); if (image != null) image.close(); }, handler);
            ownedDisplay = displays.createVirtualDisplay("J2P-owned-lifecycle", 256, 192, 160, reader.getSurface(), DisplayManager.VIRTUAL_DISPLAY_FLAG_OWN_CONTENT_ONLY);
            preferred = ownedDisplay.getDisplay().getDisplayId();
            fallback = false;
            event("OWNED_DISPLAY_ADD", "id=" + preferred);
            reconcile();
        } else if (name.equals("virtual-remove")) {
            if (ownedDisplay != null) { ownedDisplay.release(); ownedDisplay = null; }
            if (reader != null) { reader.close(); reader = null; }
            preferred = -1;
        }
        report();
    }
    @Override public void onDisplayAdded(int id) { denied.remove(id); event("DISPLAY_ADDED", "id=" + id); reconcile(); }
    @Override public void onDisplayRemoved(int id) { denied.remove(id); event("DISPLAY_REMOVED", "id=" + id); reconcile(); }
    @Override public void onDisplayChanged(int id) { event("DISPLAY_CHANGED", "id=" + id); reconcile(); }
}
