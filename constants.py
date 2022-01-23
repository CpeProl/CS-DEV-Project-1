# ============= GAME VIEWING =============

FPS = 60
PERIOD = int((1/FPS) *1000)

HEIGHT = 800
WIDTH = 1000

# Limits of the screen
XMIN = 0
XMAX = WIDTH
YMIN = 0
YMAX = HEIGHT

# BackGround Picture
BCKGROUND_PICPATH = 'pics/background.gif'

# ============= CONTROLS =============

MOVE_LEFT_KEY = 'o'
MOVE_UP_KEY = 'a'
MOVE_RIGHT_KEY = 'p'
MOVE_DOWN_KEY = 'q'

SHOOT_KEY = 'space'

# ============= ALIENS SQUADRONS =============

SQUADRON_X_SPACING = 5 # in pixels
SQUADRON_Y_SPACING = 5 # in pixels
ALIENS_SPEED = 0.1
SPEEDING_FACTOR = 1.05
ALIENS_SHOOT_MIN_RATE = 300 # in ms
ALIENS_SHOOT_MAX_RATE = 900 # in ms

# ============= ALIENS =============

ALIEN_WIDTH = 30
ALIEN_HEIGHT = 30
ALIENS_PICPATH = ['pics/croissant.gif',
                  'pics/extraterrestrial.gif',
                  'pics/fusee.gif',
                  'pics/spider.gif',
                  'pics/spinny.gif']

# ============= PLAYER =============

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 30
PLAYER_VELOCITY = 0.4
FIRE_RATE = 1000 # in ms
PLAYER_PICPATH = "pics/player.gif"

# =========== Projectiles ============

PROJECTILE_WIDTH = 2
PROJECTILE_HEIGHT = 8
PROJECTILE_SPEED = 0.5
PROJECTILE_PICPATH ="pics/projectile.gif"

# =========== Walls ============

BLOCK_HEIGHT = 10
BLOCK_WIDTH = 10
BLOCK_PICPATH = "wall.gif"
# Colors for the blocks
BLOCK_COLORS = ['556B2F', '808000', '6B8E23',
                '9ACD32', '32CD32', '008000']

WALL_X_SPACING = 1
WALL_Y_SPACING = 1

# =========== Credits ============

CREDITS_PICPATH = 'pics/credits.gif'