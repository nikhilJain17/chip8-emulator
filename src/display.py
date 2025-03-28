import curses

def byte_to_bits(b):
    """Bits as 0 or 1 integers from most to least significant."""
    return [(b >> (7 - p) & 1) for p in range(8)]

class Display:
    def __init__(self):
        """
        Coordinate system
        
        (0,0)	(63,0)
        
        (0,31)	(63,31)

        Each coordinate in the screen is either 0 (white) or 1 (black)

        Sprites are lists of 8 bit bitmaps
        xor screen with them
        """
        curses.initscr()
        self.window = curses.newwin(34, 65, 0, 0)
        self.clear() 

    def clear(self):
        self.screen = [[0 for _ in range(32)] for _ in range(64)]
        self.window.clear()

    def draw(self, vx, vy, sprite_rows):
        # Update screen
        bit_sprite_rows = [byte_to_bits(row) for row in sprite_rows]
        collision_detected = False
        for x in range(8):
            for y in range(len(bit_sprite_rows)):
                pixel = bit_sprite_rows[y][x]
                sx, sy = vx + x, vy + y
                self.screen[sx][sy] ^= pixel
                if not collision_detected and pixel == 1 and self.screen[sx][sy] == 0:
                    collision_detected = True

        # show it
        for y in range(32):
            for x in range(64):
                if self.screen[x][y] == 0:
                    self.window.addch(y+1, x+1, " ")
                else:
                    self.window.addch(y+1, x+1, "█")
        self.window.border()
        self.window.refresh()
        return collision_detected
        