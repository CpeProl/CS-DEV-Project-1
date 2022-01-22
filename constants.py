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

# Pics
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
PLAYER_VELOCITY = 1
FIRE_RATE = 500 # in ms
PLAYER_PICPATH = "JoueurOriPerma.gif"

# =========== Projectiles ============

PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 10
PROJECTILE_SPEED = 1.25

# =========== Walls ============

BLOCK_HEIGHT = 30
BLOCK_WIDTH = 30
BLOCK_PICPATH = "wall.gif"

WALL_X_SPACING = 1
WALL_Y_SPACING = 1