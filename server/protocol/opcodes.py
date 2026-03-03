# =========================
# SYSTEM
# =========================

# CLIENT → SERVER
C_PING = 1

# SERVER → CLIENT
S_PONG = 101


# =========================
# AUTH (CLIENT → SERVER)
# =========================

C_LOGIN = 10

C_REGISTER_STEP1 = 11
C_REGISTER_STEP2 = 12

# ===== CHAT =====
C_CHAT = 30
S_CHAT = 31

C_OPEN_ADMIN = 50
S_OPEN_ADMIN = 51

C_REQUEST_WARRIOR_TEMPLATES = 53
S_SEND_WARRIOR_TEMPLATES = 54
C_SAVE_WARRIOR_TEMPLATE = 55
S_SAVE_WARRIOR_TEMPLATE = 56

# =========================
# AUTH (SERVER → CLIENT)
# =========================

S_LOGIN_OK = 110
S_LOGIN_FAIL = 111

S_REGISTER_OK_STEP1 = 112
S_REGISTER_OK = 113
S_REGISTER_FAIL = 114
S_LOGIN_FAIL_MULTIPLE = 115

# =========================
# PLAYER INIT (SERVER → CLIENT)
# =========================

S_PLAYER_INIT = 130   # pacote completo do player (login ok)

C_REQUEST_WARRIOR_TEMPLATES = 53
S_SEND_WARRIOR_TEMPLATES = 54

# CONSTANTS GERAIS
# =====================================================
# LOGIN FAIL REASONS
# =====================================================

LOGIN_FAIL_INVALID = 1
LOGIN_FAIL_MULTIPLE = 2
LOGIN_FAIL_BANNED = 3
LOGIN_FAIL_SERVER = 4

# =====================================================
# REGISTER FAIL REASONS
# =====================================================

REGISTER_FAIL_INVALID = 1
REGISTER_FAIL_PASSWORD = 2
REGISTER_FAIL_LOGIN_EXISTS = 3
REGISTER_FAIL_NICKNAME_EXISTS = 4
REGISTER_FAIL_ACCOUNT_NOT_FOUND = 5
REGISTER_FAIL_INVALID_WARRIOR = 6
REGISTER_FAIL_SERVER = 99