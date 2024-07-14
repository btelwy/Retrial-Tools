#ifndef COMMAND_CODE_INCLUDE_GUARD
#define COMMAND_CODE_INCLUDE_GUARD

#define SECTION_START 0x0 //rename to START_SECTION
#define NEW_LINE 0x1
#define TEXT_COLOR 0x3 //rename to SET_TEXT_COLOR
#define MUSIC 0x5
#define SOUND 0x6 //rename
#define TEXT_SPEED 0xB //rename to SET_TEXT_SPEED
#define WAIT 0xC
#define SECTION_END 0xD
#define NAME 0xE //rename to SET_NAME
#define SET_FLAG 0x10
#define SCREEN_FLASH 0x12 //rename to FLASH_SCREEN
#define SHOW_BOX 0x13
#define HIDE_BOX 0x14
#define HALT 0x15 //rename
#define SAVE_SCREEN 0x16
#define BACKGROUND 0x1B //rename
#define TEXTBOX 0x1C //rename to TEXTBOX_COMMANDS?
#define CHAR_ANIMATION 0x1E
#define MUSIC_FADE 0x22 //rename to FADE_MUSIC
#define MUSIC_RESUME 0x23 //rename to RESUME_MUSIC
#define GUILTY_RESET
#define COURT_RECORD_BUTTON 0x26
#define SHAKE 0x27 //rename to SHAKE_SCREEN
#define JUMP 0x2C //rename to JUMP_TO_SECTION
#define TEXTBOX_END 0x2D
#define TEXTBOX_END_FORCED 0x2E //rename to TEXTBOX_END_AUTOMATIC
#define TYPEWRITER 0x30 //rename to SET_TEXT_SFX
#define SPRITE_VANISH 0x31
#define VOICE_SFX 0x42 //rename to TOGGLE_TEXT_SFX
#define RESET 0x49 //rename to BEAT_GAME_RESET
#define WAIT_NO_ANIM //rename to WAIT_NO_CHAR_ANIMATION
#define CENTER_TEXT 0x5D
#define MONOCHROME 0x5F

#define PSYCHE_LOCKS 0x8F

//all functions need the same argument types

#endif